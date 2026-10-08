---
name: resolve-composer-conflicts
description: Resolve composer.lock merge conflicts when merging main into the current branch.
---
# Resolve composer.lock Merge Conflicts

## Requirements

Git, a working PHP/Composer environment, and a repository containing `composer.json` and `composer.lock`. The examples use an initialized, running DDEV project (`ddev composer`); use plain `composer` only when the project documents an equivalent PHP/extensions environment. The target `main` branch must be available locally. Package replay may need network access and private registry credentials supplied through the project’s secure configuration. Write access to the working tree is required; committing is a separate authorized step.

## Safety and review

Before commands run outside a secure sandbox, a human must read and understand them, including Composer plugins/scripts and upstream dependency identity. A DDEV container alone is not evidence of secure isolation. Review the merge target, existing local changes, package operations, and credential/network exposure; package replay can install code and change files beyond the lock file. Use a disposable environment where possible and least privilege; never expose registry credentials or private package information to public models.

Preserve unrelated work and explain the exact lock-file replacement before applying it. Stage only verified files. A human must inspect the resulting manifest/lock diff, run the project’s appropriate checks, and approve the result before committing, sharing, or handing generated changes to a reviewer. This skill does not authorize a push. Record relevant AI assistance and unavailable checks. MCP repository mutations, if used instead of Git, also require human review.

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

Confirm this is a normal merge of `main` into the current branch, not a rebase or a reversed merge. During that normal merge, `--theirs` is main’s version. Stop and inspect the merge stages if the operation differs; do not discard branch changes by guessing.

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

## Step 7: Review, stage, and commit

Run `ddev composer validate` (or the project’s equivalent) and inspect the resulting manifest/lock diff. A human must review the result before committing; commit only when requested or already authorized. Report unresolved checks rather than treating regeneration as validation.

```bash
git add composer.json composer.lock
git commit
```

## Important notes

- Never manually edit `composer.lock` — always let Composer regenerate it.
- If `composer.json` itself has conflicts, those must be resolved manually first.
- Always re-run the original composer commands rather than using `composer update` broadly, to avoid unintended dependency changes.
