---
description: Resolve composer.lock merge conflicts when merging main into the current branch.
---
# Resolve composer.lock Merge Conflicts

You are resolving composer.lock merge conflicts following the Lullabot guide:
https://www.lullabot.com/articles/easy-guide-resolving-composerlock-conflicts

## Step 1: Check current state

Determine if a merge is currently in progress or needs to be started.

```bash
git status
```

- If there's a merge in progress with conflicts, continue to Step 2.
- If there's no merge in progress, start one with `git merge main` and then continue.
- If the merge completes without conflicts, inform the user and stop.

## Step 2: Verify composer.lock is conflicted

Check that `composer.lock` is among the conflicted files. If `composer.json` is also conflicted, warn the user — that requires manual resolution of `composer.json` first before this process can work.

## Step 3: Identify what composer changes this branch introduced

Run:

```bash
git diff main...HEAD -- composer.json
```

Note all added, removed, or changed packages. You'll need to replay these changes in Step 6.

## Step 4: Accept main's composer.lock

```bash
git checkout --theirs -- composer.lock
```

## Step 5: Resolve any other conflicted files

Check if there are other conflicted files beyond `composer.lock`. If so, inform the user and help resolve them before continuing.

## Step 6: Replay the branch's composer changes

Based on the diff from Step 3, re-run the original composer commands to apply this branch's changes on top of main's lock file:

- For **added** packages: `ddev composer require <package>:<constraint>`
- For **removed** packages: `ddev composer remove <package>`
- For **changed version constraints**: `ddev composer require <package>:<new-constraint>`
- If **no composer.json changes** exist on this branch: `ddev composer install`

This regenerates `composer.lock` with the correct `content-hash`.

## Step 7: Stage and commit

```bash
git add composer.json composer.lock
git commit
```

## Important notes

- Never manually edit `composer.lock` — always let Composer regenerate it.
- If `composer.json` itself has conflicts, those must be resolved manually first.
- Always re-run the original composer commands rather than using `composer update` broadly, to avoid unintended dependency changes.
