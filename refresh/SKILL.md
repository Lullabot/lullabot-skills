---
name: refresh
description: Return a git repo to a clean, up-to-date default branch. Discards throwaway local changes, removes untracked files, checks out the default branch (main/master/develop, whatever origin says) and fast-forwards it. Stops without touching anything if it finds work that looks worth keeping, meaning real uncommitted edits or commits that exist only locally. Use when the user types /refresh, or asks to reset, clean up, or refresh a repo or checkout, or to "get back to main and pull" or start fresh from the latest default branch.
argument-hint: "[path]"
---

# Refresh a repo

The goal is a checkout on the default branch, matching origin, with a clean working tree, without ever throwing away something the user would miss. `git reset --hard` and `git clean` can't be undone, so the survey step decides everything. Be quick when the tree is clearly disposable and stop when it isn't.

## 0. Find the repo

Work in the current directory unless `$ARGUMENTS` names a path. Run `git rev-parse --show-toplevel` and use `git -C <toplevel>` for everything after that, so a `cd` in the middle can't point you at the wrong repo.

## 1. Survey (read-only)

Run these together:

```bash
git -C "$R" status --porcelain=v1 --branch
git -C "$R" diff HEAD --stat
git -C "$R" clean -nd                     # untracked files that clean -fd would delete
git -C "$R" log --oneline HEAD --not --remotes   # commits that exist nowhere on a remote
git -C "$R" stash list
ls "$(git -C "$R" rev-parse --git-dir)" | grep -E '^(MERGE_HEAD|REBASE_(HEAD|APPLY|MERGE)|rebase-(apply|merge)|CHERRY_PICK_HEAD|REVERT_HEAD|BISECT_LOG)$'
```

`HEAD --not --remotes` also covers a detached HEAD, where checking out another branch would leave local commits hard to find.

When `--stat` shows changes, read the actual diff (`git diff HEAD`, or just the files in question if it's large) and look at the untracked files before you decide. File names alone don't tell you whether an edit is trivial.

## 2. Decide: halt or proceed

**Halt** if any of these are true:

- **Uncommitted changes that look like real work.** That includes code, config, content or docs someone wrote, a new source file, or a deliberate deletion. If you can't tell, treat it as real work.
- **Local-only commits.** The log in step 1 printed anything. Checking out another branch doesn't delete them, but a branch no one pushed is easy to forget and may be the only copy of that work.
- **An operation in progress** (merge, rebase, cherry-pick, revert or bisect). A hard reset would drop that operation halfway through.

**Disposable, fine to discard:**

- Whitespace-only or line-ending-only diffs, and file mode (chmod) flips
- Lockfile or generated-file churn from an install or build (`composer.lock`, `package-lock.json`, compiled CSS/JS, `.phpunit.result.cache`)
- Editor and tool debris: `*.swp`, `.DS_Store`, `.playwright-cli/`, logs, core dumps
- Edits you or the user made earlier in this conversation and have since said to throw away

When you halt, change nothing: no stash, no commit, no partial reset. Report what you found, grouped by type, with file paths and a one-line gist of each meaningful change and the local-only commits (`sha subject`). Say what the user could do (commit, push, stash, or tell you to discard it anyway), then stop. If the user then says to discard it, go ahead with step 3. The commits need no action, because the refresh doesn't delete them.

Stashes survive a refresh. Don't halt for them, but mention them in the final report if any exist.

## 3. Refresh

```bash
git -C "$R" fetch --prune origin
```

Find the default branch from origin's HEAD:

```bash
git -C "$R" symbolic-ref --short refs/remotes/origin/HEAD   # e.g. origin/main -> main
```

If that fails (origin/HEAD was never set), run `git -C "$R" remote set-head origin --auto` and try again. If it still fails, use `gh repo view --json defaultBranchRef -q .defaultBranchRef.name` from inside the repo. Don't guess `main`. If there's no `origin` but exactly one remote, use that one. With several remotes and no `origin`, ask.

Then:

```bash
git -C "$R" reset --hard
git -C "$R" clean -fd
git -C "$R" checkout "$DEFAULT"             # creates the tracking branch if there's no local one yet
git -C "$R" merge --ff-only "origin/$DEFAULT"
```

`clean -fd` removes untracked files and directories but keeps anything gitignored (vendor/, node_modules/, .env, ddev config), which is what we want. Don't escalate to `-x`.

If `.gitmodules` exists, finish with `git -C "$R" submodule update --init --recursive`.

### When a step fails

- **Checkout refused: the branch is already checked out in another worktree.** Report which worktree has it (`git worktree list`) and stop. Don't force it.
- **Fast-forward refused: the local default branch has diverged from origin.** Step 1 would already have caught any local-only commits reachable from HEAD, so this means someone committed to the local default branch while on a different branch. Show `git log --oneline origin/$DEFAULT..$DEFAULT` and stop. Resetting to origin would throw those commits away, and that's the user's call.
- **Fetch fails** (network, auth or VPN). Say so, and don't continue with a stale checkout while presenting it as current.

## 4. Report

Keep it short:

- The branch you're on now, and `old..new` short SHAs from the fast-forward (or "already up to date")
- What got discarded, if anything: counts and a few example paths
- Anything worth knowing: stashes, other local branches with local-only commits, a changed lockfile that probably means running `composer install` or `npm ci`
