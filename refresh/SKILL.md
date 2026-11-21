---
name: refresh
description: Return a git repo to a clean, up-to-date default branch. Discards throwaway local changes, removes untracked files, checks out the default branch (main/master/develop, whatever origin says) and fast-forwards it. Stops without touching anything if it finds work that looks worth keeping, meaning real uncommitted edits or commits that exist only locally. Use when the user types /refresh, or asks to reset, clean up, or refresh a repo or checkout, or to "get back to main and pull" or start fresh from the latest default branch.
argument-hint: "[path]"
---

# Refresh a repo

## Requirements

Git and a shell with local repository access; authenticated network access to the selected remote for fetch. Optional GitHub CLI (`gh`) can discover the default branch when the remote HEAD is unavailable. Submodule initialization needs access to each configured remote. No MCP server is required.

## Safety and review

This workflow can permanently discard tracked and untracked work. Before reset or clean, a human reviews the exact repository/worktree, diff, full deletion preview, current and target branch commits, and commands outside a verified secure sandbox. A request to refresh does not establish that unknown files are disposable. Halt on valuable or uncertain work; get explicit authorization for the listed discard scope and repeat the survey if state changes. Keep ignored data, nested repositories, other worktrees, and submodule changes intact; never escalate to `clean -x`, double-force cleaning, or resetting to a remote to bypass divergence. Fetch and submodule URLs can expose credentials or run project hooks/config; review their destinations and dependencies. A human checks the final state and redacts private paths/remotes before sharing the report.

Outside a verified secure sandbox, a human must read and understand unreviewed shell commands and generated code before execution. Always review MCP data-changing operations if an MCP alternative is used. Use least privilege; tool installation requires Security Team review and verification of upstream identity. Personal information requires approved tooling integrated with its source system; confidential information requires specifically approved tools; non-public information requires tools that neither train on nor retain it. Never send sensitive non-public data to public AI models. Stop when eligibility is unknown. An AI check does not replace human self-review before sharing, publishing, or handing work to another reviewer.


The goal is a checkout on the default branch, matching origin, with a clean working tree, without ever throwing away something the user would miss. `git reset --hard` and `git clean` can't be undone, so the survey step decides everything. Be quick when the tree is clearly disposable and stop when it isn't.

## 0. Identify the checkout and remote

Use the current directory unless the user's request names a path. Resolve the repository with `git rev-parse --show-toplevel` and set `R` to that absolute path; use `git -C "$R"` thereafter. Inspect `git remote -v` and `git worktree list`. Select `REMOTE=origin` when present; if it is absent and there is exactly one remote use that name throughout. With multiple possible remotes, ask which target the user intends. Do not print credential-bearing remote URLs in the final report.

## 1. Survey without changing files

```bash
git -C "$R" status --porcelain=v1 --branch
git -C "$R" diff HEAD --stat
git -C "$R" clean -nd
git -C "$R" log --oneline HEAD --not --remotes
git -C "$R" stash list
git -C "$R" submodule status --recursive
```

Inspect operation markers using `git -C "$R" rev-parse --git-path <marker>` for MERGE_HEAD, REBASE_HEAD, CHERRY_PICK_HEAD, REVERT_HEAD, BISECT_LOG, rebase-apply, and rebase-merge. This works for linked worktrees as well as ordinary checkouts. Read actual diffs and untracked file contents when needed; filenames alone cannot establish disposability. Inspect initialized submodules for local changes/commits before any submodule update. Do not expose private source or credentials to ineligible AI tooling.

## 2. Halt on work or uncertainty

Stop before fetch/reset/clean if there is meaningful uncommitted work, local-only commits reachable from HEAD, a merge/rebase/cherry-pick/revert/bisect in progress, or changed submodules. Detached HEAD commits receive the same protection. Report paths, a brief description, and commit IDs, then let the user decide whether to commit, stash, or authorize a specific discard.

Potentially disposable items include whitespace-only changes or build/editor debris **only after reviewing their contents and confirming they can be regenerated**. Lockfiles, generated assets, logs, and browser recordings can contain valuable work or private data; their names are not permission to delete them. Explicit earlier discard instructions apply only to the named changes, not later edits.

Stashes survive this workflow; mention them but do not drop them. If the user authorizes discarding local-only commits, preserve their branch/ref or create an agreed backup ref before any branch movement; a hard reset alone does not delete current branch commits, but later updates can make them hard to recover.

## 3. Fetch and inspect the target before discarding

After a safe survey, fetch the chosen remote:

```bash
git -C "$R" fetch --prune "$REMOTE"
git -C "$R" symbolic-ref --short "refs/remotes/$REMOTE/HEAD"
```

Extract `DEFAULT` from the returned remote HEAD. If missing, query `git -C "$R" ls-remote --symref "$REMOTE" HEAD`; optional `gh repo view --json defaultBranchRef -q .defaultBranchRef.name` must run in the confirmed project with the intended GitHub remote. Do not guess a branch. Stop if fetch/discovery fails.

Before reset or clean, inspect the **target local default branch**, even when currently on a feature branch. If it exists, run `git -C "$R" log --oneline "$REMOTE/$DEFAULT..$DEFAULT"`; halt on any commit, since fast-forwarding would discard/diverge from work not seen in the HEAD survey. Confirm it is not checked out in another worktree. Re-run status/diff/deletion preview after fetch and stop if the discard scope changed.

A human reviews the exact tracked discard and untracked deletion list and the commands before execution outside a verified secure sandbox. Preserve any work not explicitly within that scope. Run reset only when all tracked changes are authorized for discard. Clean only the reviewed untracked paths, using pathspecs instead of deleting everything by default:

```bash
git -C "$R" reset --hard HEAD                  # only the reviewed tracked discard scope
git -C "$R" clean -nd -- <approved-untracked-paths>
git -C "$R" clean -fd -- <approved-untracked-paths>
git -C "$R" checkout "$DEFAULT"
git -C "$R" merge --ff-only "$REMOTE/$DEFAULT"
```

Skip reset/clean when there is nothing authorized to discard. If the local default branch does not exist, create it explicitly with `git -C "$R" checkout -b "$DEFAULT" --track "$REMOTE/$DEFAULT"`. Never force checkout, reset to a remote to bypass divergence, remove ignored files (`-x`), or delete nested repositories (double-force cleaning).

If `.gitmodules` exists, review its remote URLs and initialized submodule state first, then run `git -C "$R" submodule update --init --recursive` only for a clean, authorized scope. Stop on submodule work rather than overwriting it.

### Failure handling

Stop at the first failed step and report the actual partial state. A branch held in another worktree must not be forced. A non-fast-forward merge requires human resolution; do not discard commits. A failed fetch must not be reported as an up-to-date checkout. Changes concurrent with the survey require a new review of the affected scope.

## 4. Report

Report the current branch, old/new short SHAs (or already up to date), and the exact paths discarded. Mention retained stashes, protected local work, submodule limitations, or missing authentication. A human reviews this report before sharing it beyond the requester; redact private paths and remote details as needed.
