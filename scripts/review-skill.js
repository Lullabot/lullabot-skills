#!/usr/bin/env node
//
// review-skill.js
//
// Advisory best-practice review for skills in this repo. Emits warnings and
// suggestions; it NEVER fails the build (always exits 0). This is the
// deterministic counterpart to the `reviewing-skills` skill, which adds the
// subjective judgment. The hard, blocking structural gate lives in
// validate-skills.js — this script does not duplicate it.
//
// Usage:
//   node scripts/review-skill.js                # review every skill
//   node scripts/review-skill.js reviewing-skills   # review one skill
//
// Checks (all non-blocking) are drawn from the vendored rubric at
//   reviewing-skills/references/skill-best-practices.md

const fs = require('fs');
const path = require('path');

const { ROOT, parseSimpleYaml, listSkillDirs } = require('./validate-skills.js');

const RUBRIC_REL = 'reviewing-skills/references/skill-best-practices.md';
const STALE_DAYS = 30;
const MAX_BODY_LINES = 500;
const MAX_NAME_LEN = 64;
const MAX_DESC_LEN = 1024;
const REF_TOC_MIN_LINES = 100;

// Severity labels used in the printed report.
const ISSUE = 'issue';
const SUGGEST = 'suggest';

function readFileSafe(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch {
    return null;
  }
}

// Split a SKILL.md into its YAML frontmatter and the markdown body that
// follows. Mirrors the delimiter handling in validate-skills.js.
function splitFrontmatter(raw) {
  if (!raw.startsWith('---\n')) return { yaml: null, body: raw };
  const end = raw.indexOf('\n---', 4);
  if (end === -1) return { yaml: null, body: raw };
  const yaml = raw.slice(4, end);
  // Body begins after the closing delimiter line.
  const afterDelim = raw.indexOf('\n', end + 1);
  const body = afterDelim === -1 ? '' : raw.slice(afterDelim + 1);
  return { yaml, body };
}

function countLines(text) {
  if (!text) return 0;
  return text.replace(/\n$/, '').split('\n').length;
}

// Markdown links to a local file (not an http(s) URL, not an anchor).
function localLinks(text) {
  const links = [];
  const re = /\]\(([^)]+)\)/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    const target = m[1].trim().split(/\s+/)[0]; // drop optional "title"
    if (/^(https?:|mailto:|#)/i.test(target)) continue;
    links.push(target);
  }
  return links;
}

// Look like a Windows path: word\word (backslash between path-ish segments).
function hasBackslashPath(text) {
  return /[A-Za-z0-9_.-]+\\[A-Za-z0-9_.-]+/.test(text);
}

function isThirdPersonViolation(desc) {
  return (
    /^\s*(i|we|you)\b/i.test(desc) ||
    /\bI can\b/i.test(desc) ||
    /\bI'll\b/i.test(desc) ||
    /\byou can\b/i.test(desc) ||
    /\bhelps you\b/i.test(desc) ||
    /\blet me\b/i.test(desc)
  );
}

function isVagueDescription(desc) {
  const vague = [/\bhelps with\b/i, /\bdoes stuff\b/i, /^\s*processes data\b/i];
  if (vague.some((re) => re.test(desc))) return true;
  return desc.trim().length < 40;
}

// Review a single skill directory. Returns { name, findings: [{severity, msg}] }.
function reviewSkill(skillName) {
  const skillDir = path.join(ROOT, skillName);
  const findings = [];
  const add = (severity, msg) => findings.push({ severity, msg });

  const skillMdPath = path.join(skillDir, 'SKILL.md');
  const raw = readFileSafe(skillMdPath);
  if (raw === null) {
    // Structural problem — validate-skills.js owns the hard error. Note and move on.
    add(ISSUE, 'SKILL.md not found (see validate-skills.js for the blocking check).');
    return { name: skillName, findings };
  }

  const { yaml, body } = splitFrontmatter(raw);
  const fm = yaml ? safeYaml(yaml) : {};

  // --- Body length ---
  const bodyLines = countLines(body);
  if (bodyLines > MAX_BODY_LINES) {
    add(
      ISSUE,
      `SKILL.md body is ${bodyLines} lines (> ${MAX_BODY_LINES}). Split detail into separate files (progressive disclosure).`
    );
  }

  // --- name ---
  const name = fm.name || '';
  if (name) {
    if (name.length > MAX_NAME_LEN) add(ISSUE, `name is ${name.length} chars (> ${MAX_NAME_LEN}).`);
    if (!/^[a-z0-9-]+$/.test(name)) add(ISSUE, `name "${name}" must be lowercase letters, numbers, and hyphens only.`);
    if (/anthropic|claude/i.test(name)) add(ISSUE, `name "${name}" contains a reserved word (anthropic/claude).`);
  }

  // --- description ---
  const desc = fm.description || '';
  if (desc) {
    if (desc.length > MAX_DESC_LEN) add(ISSUE, `description is ${desc.length} chars (> ${MAX_DESC_LEN}).`);
    if (isThirdPersonViolation(desc)) {
      add(ISSUE, 'description should be written in the third person (avoid "I"/"you"/"helps you").');
    }
    if (isVagueDescription(desc)) {
      add(SUGGEST, 'description looks vague — name the file types, tasks, and triggers so Claude knows when to use it.');
    }
    if (!/\buse when\b|\btriggers?\b|\bwhen the user\b|\bwhen working\b|\bwhen asked\b/i.test(desc)) {
      add(SUGGEST, 'description does not state *when* to use the skill — add trigger conditions ("Use when…").');
    }
  }

  // Naming *style* (gerund vs. noun-phrase) is a judgment call the rubric
  // leaves open — it belongs to the reviewing-skills skill, not this linter.

  // --- backslash paths in SKILL.md ---
  if (hasBackslashPath(stripCodeFences(body))) {
    add(SUGGEST, 'SKILL.md appears to contain a Windows-style path — use forward slashes (scripts/helper.py).');
  }

  // --- companion .md files: nested refs, ToC, backslash paths ---
  for (const refRel of listMarkdownFiles(skillDir)) {
    const refAbs = path.join(skillDir, refRel);
    const refRaw = readFileSafe(refAbs);
    if (refRaw === null) continue;

    const refLines = countLines(refRaw);
    const links = localLinks(refRaw).filter((t) => /\.md(#|$)/i.test(t));
    if (links.length) {
      add(
        ISSUE,
        `${refRel} links to other markdown files (${links.join(', ')}). Keep references one level deep from SKILL.md.`
      );
    }
    if (refLines > REF_TOC_MIN_LINES && !hasTableOfContents(refRaw)) {
      add(SUGGEST, `${refRel} is ${refLines} lines but has no table of contents — add a "## Contents" near the top.`);
    }
    if (hasBackslashPath(stripCodeFences(refRaw))) {
      add(SUGGEST, `${refRel} appears to contain a Windows-style path — use forward slashes.`);
    }
  }

  return { name: skillName, findings };
}

function safeYaml(yaml) {
  try {
    return parseSimpleYaml(yaml, 'SKILL.md');
  } catch {
    return {};
  }
}

// Remove fenced code blocks so prose-level checks don't trip on code.
function stripCodeFences(text) {
  return text.replace(/```[\s\S]*?```/g, '').replace(/`[^`]*`/g, '');
}

function hasTableOfContents(text) {
  const head = text.split('\n').slice(0, 40).join('\n');
  return /^#{1,3}\s+(contents|table of contents)\b/im.test(head);
}

// Companion markdown files in a skill dir that participate in progressive
// disclosure — i.e. detail files SKILL.md links to. Excludes SKILL.md itself
// and any README.md (those are GitHub/dir documentation, not skill references).
// Walked recursively as paths relative to the skill dir.
function listMarkdownFiles(skillDir) {
  const out = [];
  function walk(dir, prefix) {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const e of entries) {
      const rel = prefix ? `${prefix}/${e.name}` : e.name;
      if (e.isDirectory()) {
        walk(path.join(dir, e.name), rel);
      } else if (e.isFile() && e.name.endsWith('.md') && rel !== 'SKILL.md' && e.name !== 'README.md') {
        out.push(rel);
      }
    }
  }
  walk(skillDir, '');
  return out;
}

// Global: is the vendored rubric stale? Compares last_synced to today.
function checkRubricStaleness() {
  const raw = readFileSafe(path.join(ROOT, RUBRIC_REL));
  if (raw === null) return null;
  const m = raw.match(/last_synced:\s*(\d{4}-\d{2}-\d{2})/);
  if (!m) return { severity: SUGGEST, msg: `${RUBRIC_REL} has no last_synced stamp.` };
  const synced = new Date(`${m[1]}T00:00:00Z`);
  const ageDays = Math.floor((Date.now() - synced.getTime()) / 86400000);
  if (ageDays > STALE_DAYS) {
    return {
      severity: SUGGEST,
      msg: `best-practices rubric last synced ${m[1]} (${ageDays} days ago). Run scripts/sync-best-practices.sh to refresh.`,
    };
  }
  return null;
}

function marker(severity) {
  return severity === ISSUE ? 'issue   ' : 'suggest ';
}

function main() {
  const arg = process.argv[2];
  let targets;
  if (arg) {
    const name = path.basename(arg.replace(/\/+$/, ''));
    targets = [name];
  } else {
    targets = listSkillDirs();
  }

  const results = targets.map(reviewSkill);
  const stale = checkRubricStaleness();

  let issueCount = 0;
  let suggestCount = 0;

  for (const { name, findings } of results) {
    if (findings.length === 0) {
      console.log(`\n${name}: no best-practice findings.`);
      continue;
    }
    console.log(`\n${name}:`);
    for (const f of findings) {
      if (f.severity === ISSUE) issueCount++;
      else suggestCount++;
      console.log(`  ${marker(f.severity)}- ${f.msg}`);
    }
  }

  if (stale) {
    suggestCount++;
    console.log('\nmaintenance:');
    console.log(`  ${marker(stale.severity)}- ${stale.msg}`);
  }

  console.log(
    `\nReviewed ${results.length} skill(s): ${issueCount} issue(s), ${suggestCount} suggestion(s). Advisory only — nothing blocks.`
  );

  // Advisory by design: never fail the build.
  process.exit(0);
}

if (require.main === module) main();

module.exports = { reviewSkill, checkRubricStaleness };
