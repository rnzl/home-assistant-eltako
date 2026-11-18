---
name: eltako-git-workflow
description: "Use when creating or switching Git branches, preparing commits, opening pull requests, merging changes, or preparing releases and tags."
---

# Git workflow

1. Inspect the current branch and worktree before Git operations. Preserve
   unrelated changes; do not stash, discard, or include them without approval.
2. Keep `main` releasable. For new work, use a short-lived `feature/...` or
   `fix/...` branch based on an up-to-date `main`. If existing work or uncommitted
   changes make switching unsafe or ambiguous, ask before proceeding.
3. Keep commits focused and run the relevant checks before proposing a PR. Stage
   only files belonging to the requested work.
4. Open a PR targeting `main`; check the actual CI results before proposing a
   merge. If checks are pending, skipped, or failing, report their status.
5. Commit directly to `main`, rewrite history, force-push, or merge only with
   explicit user approval. Do not bypass required checks.
6. After a successful merge, delete the short-lived branch with user approval.

## Releases

1. Merge finished work into `main` after required CI checks pass.
2. Update the version and changelog in a PR, then merge it into `main`.
3. With explicit user approval, tag that commit and publish a GitHub release.
4. Verify that the release workflow builds and tests the package, including
   macOS, before package publication. Report pending or failed checks.
5. Use a temporary release branch only when an older version needs maintenance
   while development continues on `main`.

These are agent guidelines, not enforcement. GitHub branch protection must be
configured separately to enforce required checks and protect `main`.
