# Git for DevOps

## Mental model

Git stores a directed graph of commits. A branch is a movable name pointing to a commit; `HEAD` identifies the current checkout. The index (staging area) records the proposed next snapshot. A merge joins histories; a rebase recreates commits on a new base and therefore changes their IDs.

## Daily workflow

Inspect before changing: `git status`, `git diff`, and `git log --oneline --graph`. Stage deliberately (`git add -p` for partial changes), write focused commits, and fetch before integrating remote work. Resolve conflicts by understanding both intended changes, then run tests before completing the merge/rebase. Use `git revert` for a shared-history undo; reserve `reset` and force-push for carefully coordinated local-history changes.

## Useful tools

- `git show <commit>` inspects a change; `git blame` traces line history, not correctness.
- `git stash` temporarily shelves work; branches are usually clearer for longer tasks.
- `.gitignore` prevents untracked files from appearing, but does not remove already tracked secrets.
- Tags identify releases; signed commits/tags can add provenance when the organization verifies them.

## Safety and collaboration

Never commit credentials. If a secret was pushed, revoke/rotate it immediately; deleting a commit does not invalidate copied credentials. Protect default branches, require reviews and status checks, and use small commits to aid review and rollback. Before rewriting history, verify nobody depends on the branch.

## Practice

Create two feature branches from a shared base, make overlapping edits, resolve a conflict, and compare merge and rebase histories. Revert a bad commit without rewriting the shared branch.

## Further reading

[Pro Git book](https://git-scm.com/book/en/v2) · [Git reference](https://git-scm.com/docs)
