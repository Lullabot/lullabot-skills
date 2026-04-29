#!/usr/bin/env python3
"""
Extract and cluster Claude Code session data for time logging.

Scans ~/.claude/history.jsonl and session JSONL files to produce a compact
JSON summary of active work segments grouped by project.

Usage:
    python3 session-summary.py [YYYY-MM-DD]

If no date is provided, defaults to today.

Output: JSON to stdout with per-project active minutes and segments.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("America/Los_Angeles")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CLAUDE_DIR = Path.home() / ".claude"
HISTORY_FILE = CLAUDE_DIR / "history.jsonl"
PROJECTS_DIR = CLAUDE_DIR / "projects"

# Gap threshold: if more than this many minutes pass between consecutive
# user messages, treat them as separate active segments.
GAP_THRESHOLD_MINUTES = 5

# Minimum segment duration in minutes (even a single prompt counts as some work)
MIN_SEGMENT_MINUTES = 2

# Minimum project total to report (skip trivial drive-by sessions)
MIN_PROJECT_MINUTES = 5

# ---------------------------------------------------------------------------
# Project mapping from .env
# ---------------------------------------------------------------------------

def load_env():
    """Load project configuration from automation/.env"""
    env_path = Path.home() / "repos" / "Hivemind" / "automation" / "scripts" / ".env"
    env = {}
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    env[key.strip()] = val.strip()
    return env


def build_path_to_project_map(env):
    """
    Build a mapping from session directory path fragments to project keys.
    Returns list of (pattern, project_key) tuples, ordered longest-first
    so more specific paths match before general ones.
    """
    projects_str = env.get("PROJECTS", "")
    project_keys = [p.strip() for p in projects_str.split(",") if p.strip()]

    mappings = []
    for key in project_keys:
        dir_name = env.get(f"{key}_DIR", key)
        # Agent directory pattern
        mappings.append((f"Hivemind-agents-{dir_name}", key))
        # Also match code subdirectories
        github_repo = env.get(f"{key}_GITHUB_REPO", "")
        if github_repo:
            repo_name = github_repo.split("/")[-1]
            mappings.append((repo_name, key))

    # Hivemind root is internal work (dashboard, automation, planning)
    # User can reassign at review time
    mappings.append(("Hivemind", "_INTERNAL"))

    # Sort by pattern length descending (most specific first)
    mappings.sort(key=lambda x: len(x[0]), reverse=True)
    return mappings


def resolve_project(session_path, mappings):
    """Given a session directory path, resolve to a project key."""
    for pattern, project_key in mappings:
        if pattern in session_path:
            return project_key
    return "UNKNOWN"


# ---------------------------------------------------------------------------
# Session data extraction
# ---------------------------------------------------------------------------

def get_history_entries(target_date):
    """
    Extract user prompts from history.jsonl for the target date.
    Returns list of (datetime, project_path, prompt_text).
    """
    entries = []
    if not HISTORY_FILE.exists():
        return entries

    with open(HISTORY_FILE) as f:
        for line in f:
            try:
                d = json.loads(line)
                ts_ms = d.get("timestamp", 0)
                dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
                # Compare in local timezone
                local_dt = dt.astimezone(LOCAL_TZ)
                if local_dt.strftime("%Y-%m-%d") == target_date:
                    project = d.get("project", "")
                    display = d.get("display", "")
                    entries.append((local_dt, project, display))
            except (json.JSONDecodeError, ValueError, OSError):
                continue

    return entries


def get_session_timestamps(target_date):
    """
    Scan all session JSONL files modified on target_date for message timestamps.
    Returns dict: {session_dir: [(datetime, msg_type, snippet), ...]}
    """
    sessions = {}

    for proj_dir in PROJECTS_DIR.iterdir():
        if not proj_dir.is_dir():
            continue

        proj_name = proj_dir.name

        for jsonl_file in proj_dir.glob("*.jsonl"):
            # Quick filter: check file modification date
            try:
                mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime)
                if mtime.strftime("%Y-%m-%d") != target_date:
                    continue
            except OSError:
                continue

            timestamps = []
            with open(jsonl_file) as f:
                for line in f:
                    try:
                        d = json.loads(line)
                        ts = d.get("timestamp", "")
                        if not ts:
                            # Check snapshot timestamp
                            snap = d.get("snapshot", {})
                            if isinstance(snap, dict):
                                ts = snap.get("timestamp", "")
                            if not ts:
                                continue

                        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        # Convert to local time and filter by local date
                        local_dt = dt.astimezone(LOCAL_TZ)
                        if local_dt.strftime("%Y-%m-%d") != target_date:
                            continue

                        msg_type = d.get("type", "unknown")

                        # Track user messages (with snippets) and assistant/tool
                        # activity (without snippets) to keep segments alive
                        # during autonomous tool work.
                        if msg_type == "user":
                            # Extract prompt snippet
                            snippet = ""
                            msg = d.get("message", {})
                            if isinstance(msg, dict):
                                content = msg.get("content", "")
                                if isinstance(content, list):
                                    for c in content:
                                        if isinstance(c, dict) and c.get("type") == "text":
                                            snippet = c["text"][:80]
                                            break
                                elif isinstance(content, str):
                                    snippet = content[:80]
                            timestamps.append((local_dt, "user", snippet))
                        elif msg_type in ("assistant", "tool_result", "tool_use"):
                            # Activity signal — keeps segment alive but no snippet
                            timestamps.append((local_dt, "activity", ""))

                    except (json.JSONDecodeError, ValueError):
                        continue

            if timestamps:
                key = proj_name
                if key not in sessions:
                    sessions[key] = []
                sessions[key].extend(timestamps)

    return sessions


# ---------------------------------------------------------------------------
# Active segment clustering
# ---------------------------------------------------------------------------

def cluster_into_segments(timestamps, gap_minutes=GAP_THRESHOLD_MINUTES):
    """
    Given sorted list of (datetime, type, snippet) tuples, cluster into
    active segments. A new segment starts when the gap between consecutive
    messages (user OR activity) exceeds gap_minutes. Activity signals
    (assistant/tool work) keep segments alive without contributing snippets.

    Returns list of segments: [(start_dt, end_dt, [snippets])]
    """
    if not timestamps:
        return []

    timestamps.sort(key=lambda x: x[0])
    segments = []
    seg_start = timestamps[0][0]
    seg_end = timestamps[0][0]
    seg_snippets = [timestamps[0][2]] if timestamps[0][2] else []

    for i in range(1, len(timestamps)):
        dt, msg_type, snippet = timestamps[i]
        gap = (dt - seg_end).total_seconds() / 60

        if gap > gap_minutes:
            # Close current segment
            segments.append((seg_start, seg_end, seg_snippets))
            # Start new segment
            seg_start = dt
            seg_end = dt
            seg_snippets = [snippet] if snippet else []
        else:
            seg_end = dt
            if snippet and msg_type == "user":
                seg_snippets.append(snippet)

    # Close final segment
    segments.append((seg_start, seg_end, seg_snippets))
    return segments


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    target_date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")

    env = load_env()
    path_mappings = build_path_to_project_map(env)

    # Gather timestamps from session JSONL files
    session_data = get_session_timestamps(target_date)

    # Group by project
    project_timestamps = defaultdict(list)
    for session_dir, timestamps in session_data.items():
        project_key = resolve_project(session_dir, path_mappings)
        project_timestamps[project_key].extend(timestamps)

    # Also incorporate history.jsonl for completeness (catches prompts
    # that might not have full JSONL files yet, like the current session)
    history_entries = get_history_entries(target_date)
    for dt, project_path, display in history_entries:
        # Resolve project from the path
        # Extract the meaningful part of the path
        path_fragment = project_path.replace("/Users/sirkitree/repos/", "").replace("/", "-")
        project_key = resolve_project(path_fragment, path_mappings)
        # Add as a timestamp entry (avoid duplicates by using history as supplement)
        project_timestamps[project_key].append((dt, "user", display[:80]))

    # Deduplicate timestamps within each project (within 3 seconds = same message)
    for key in project_timestamps:
        timestamps = sorted(project_timestamps[key], key=lambda x: x[0])
        deduped = []
        for ts in timestamps:
            if not deduped or (ts[0] - deduped[-1][0]).total_seconds() > 3:
                deduped.append(ts)
        project_timestamps[key] = deduped

    # Cluster into segments per project
    output = {
        "date": target_date,
        "gap_threshold_minutes": GAP_THRESHOLD_MINUTES,
        "projects": {},
        "total_minutes": 0,
    }

    for project_key, timestamps in sorted(project_timestamps.items()):
        segments = cluster_into_segments(timestamps)

        # Calculate total active minutes
        total_minutes = 0
        segment_list = []
        for seg_start, seg_end, snippets in segments:
            duration = max(
                MIN_SEGMENT_MINUTES,
                (seg_end - seg_start).total_seconds() / 60 + MIN_SEGMENT_MINUTES,
            )
            total_minutes += duration

            # Clean up snippets: remove empty, /clear, /exit, duplicates
            clean_snippets = []
            seen = set()
            for s in snippets:
                s = s.strip()
                if not s or s.startswith("/clear") or s.startswith("/exit"):
                    continue
                if s.startswith("<command"):
                    # Extract command name
                    if "command-name>" in s:
                        parts = s.split("command-name>")
                        if len(parts) > 1:
                            s = "/" + parts[1].split("<")[0]
                    else:
                        continue
                short = s[:60]
                if short not in seen:
                    seen.add(short)
                    clean_snippets.append(short)

            segment_list.append({
                "start": seg_start.strftime("%H:%M"),
                "end": seg_end.strftime("%H:%M"),
                "duration_minutes": round(duration),
                "prompts": clean_snippets[:5],  # Keep top 5 for brevity
            })

        # Round total to nearest 15 minutes
        rounded_minutes = max(15, round(total_minutes / 15) * 15)

        if rounded_minutes >= MIN_PROJECT_MINUTES:
            if project_key == "_INTERNAL":
                display_name = "Internal (Hivemind/Dashboard)"
            elif project_key == "UNKNOWN":
                display_name = "Unknown"
            else:
                display_name = env.get(f"{project_key}_DISPLAY_NAME", project_key)
            output["projects"][project_key] = {
                "display_name": display_name,
                "raw_minutes": round(total_minutes),
                "rounded_minutes": rounded_minutes,
                "segments": segment_list,
                "noko_project_id": env.get(f"{project_key}_PROJECT_ID", ""),
            }
            output["total_minutes"] += rounded_minutes

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
