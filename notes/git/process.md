# Git team change lifecycle

## 1. Start from a known base

```bash
git status --short --branch
git fetch origin --prune
git switch main
git pull --ff-only
git switch -c feature/short-description
```

Confirm no unrelated work is in the tree before branching. Use issue/incident context to state the change's intent and acceptance criteria.

## 2. Make and inspect a focused change

Edit only the needed files; run formatter/linter/tests. Inspect both unstaged and staged content:

```bash
git diff --check
git diff
git add -p
git diff --cached
git status --short
```

Search staged changes for credentials and generated artifacts. `.gitignore` does not untrack committed files. Never include private keys, tokens, customer data, or local state.

## 3. Commit, publish, review

Use an imperative, scoped commit message that explains why. Push a feature branch, open a PR, describe behavior/risk/validation/rollback, and wait for required reviews and current CI. Address review comments with follow-up commits or carefully coordinated amend before the branch is shared.

## 4. Conflict/recovery

Fetch before integrating. For a conflict, identify base/ours/theirs, combine intended behavior, run the relevant tests, and inspect the final diff. Use `revert` for a shared bad commit; reserve reset/rebase for unshared work. Force push only when explicitly coordinated and protected by team policy.

## 5. Secret incident

Immediately revoke/rotate exposed credentials, scope impact from audit logs, notify security, remove the secret from active code/history as directed, and enable scanning/prevention. History rewrite is secondary; clones/caches may retain old objects.

## 6. Release and cleanup

Merge only after gates pass; tag/release the reviewed commit and record artifact digest. Delete merged branches per policy. Verify main is green and deploy outcome is healthy; use a revert/redeploy for rollback, not an unreviewed history rewrite.
