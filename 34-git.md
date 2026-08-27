# 34. Git & Engineering Workflow

**Previous:** [33. Backend Security](./33-security.md)

**Next:** [35. DSA Fundamentals](./35-dsa-foundations.md)

______________________________________________________________________

## Objective

By the end of this topic, you should be able to:

- Explain Git's core model and everyday workflow.
- Work safely with branches.
- Understand merge and rebase.
- Resolve merge conflicts.
- Distinguish `reset`, `revert`, and `restore`.
- Use `stash` correctly.
- Use `cherry-pick` for targeted changes.
- Understand squashing and clean commit history.
- Recover lost commits with `reflog`.
- Use `bisect` to locate regressions.
- Work effectively with pull requests.
- Perform and participate in code reviews.
- Explain practical Git workflows expected from a senior backend engineer.

______________________________________________________________________

# 1. Why Git Matters for Backend Engineers

Git is more than a tool for storing source code.

It provides:

- Version history
- Collaboration
- Branching
- Change isolation
- Code review
- Release traceability
- Regression investigation
- Recovery from mistakes

For a senior engineer, the important skill is knowing how to manipulate history safely and how Git fits into the
engineering workflow.

______________________________________________________________________

# 2. Git Mental Model

A useful simplified model is:

```text
Working Tree
    ↓
Staging Area
    ↓
Commit
    ↓
Repository
```

### Working tree

The files currently checked out on your machine.

### Staging area

The set of changes selected for the next commit.

### Commit

A snapshot representing a point in project history.

______________________________________________________________________

# 3. Repository and Commit History

A repository contains objects representing project history.

A commit records information such as:

- Snapshot/tree
- Parent commit(s)
- Author
- Committer
- Message

Commits form a history graph.

For example:

```text
A → B → C
```

A merge can create:

```text
A → B → D
     ↘ C ↗
```

Understanding the graph makes merge, rebase and recovery much easier.

______________________________________________________________________

# 4. HEAD

`HEAD` represents the commit/reference currently checked out.

Typically:

```text
HEAD
 ↓
current branch
 ↓
latest commit
```

You can inspect it with:

```bash
git status
git log --oneline
```

______________________________________________________________________

# 5. Branches

A Git branch is essentially a movable reference to a commit.

Example:

```text
A → B → C
        ↑
      main
```

Creating a feature branch:

```bash
git switch -c feature/payment-api
```

Now:

```text
A → B → C
        ↑
       main
        \
         D → E
             ↑
      feature/payment-api
```

______________________________________________________________________

# 6. Branching Strategy

A practical backend workflow might use:

```text
main
  ↓
feature/*
bugfix/*
hotfix/*
```

The exact branching model depends on the organization.

The important principles are:

- Keep branches focused.
- Avoid unnecessarily long-lived branches.
- Keep changes reviewable.
- Integrate frequently enough to reduce conflicts.

______________________________________________________________________

# 7. Feature Branch Workflow

Typical workflow:

```bash
git switch main
git pull
git switch -c feature/user-search

# work
git add .
git commit -m "Add user search"

git push -u origin feature/user-search
```

Then create a pull request.

______________________________________________________________________

# 8. Merge

Merge combines histories.

Suppose:

```text
A → B → C
     \
      D → E
```

Merging the feature branch into `main` can produce:

```text
A → B → C → M
     \     ↗
      D → E
```

`M` is a merge commit.

______________________________________________________________________

# 9. Fast-Forward Merge

If the target branch has not diverged:

```text
A → B → C
        ↑
      feature
```

A fast-forward can simply move the branch pointer:

```text
A → B → C
        ↑
       main
       feature
```

No merge commit is required.

______________________________________________________________________

# 10. Rebase

Rebase rewrites commits by replaying them on top of another base.

Before:

```text
A → B → C
     \
      D → E
```

After rebasing feature onto `C`:

```text
A → B → C → D' → E'
```

`D'` and `E'` are new commits.

______________________________________________________________________

# 11. Merge vs Rebase

### Merge

Preserves the existing branch topology.

Advantages:

- Does not rewrite existing commits.
- Preserves the true branching history.

### Rebase

Creates a more linear history.

Advantages:

- Cleaner history.
- Easier linear reading/logging.

Trade-off:

> Rebase rewrites commit identities.

______________________________________________________________________

# 12. Golden Rule of Rebase

Avoid rebasing commits that other people are already relying on unless the team explicitly agrees to it.

Why?

Because rebase creates new commit identities.

If you already pushed a branch and others built work on it, rewriting the history can create unnecessary problems.

______________________________________________________________________

# 13. Interactive Rebase

Interactive rebase is useful for cleaning local commit history.

Example:

```bash
git rebase -i HEAD~4
```

You can:

```text
pick
reword
edit
squash
fixup
drop
```

before the commits become part of a shared history.

______________________________________________________________________

# 14. Squashing

Suppose a feature branch contains:

```text
Add API
Fix typo
Fix tests
Fix review comment
Final fix
```

These may be squashed into:

```text
Add user search API
```

This can make the final history easier to understand.

______________________________________________________________________

# 15. When to Squash

Squashing is useful when intermediate commits are implementation noise.

For example:

```text
fix
fix again
oops
test fix
review fix
```

can become one coherent change.

Do not squash blindly if individual commits provide meaningful historical information.

______________________________________________________________________

# 16. Merge Conflicts

A conflict occurs when Git cannot automatically reconcile changes.

Example:

```text
Branch A:
return user.name

Branch B:
return user.full_name
```

Git may require a human decision.

______________________________________________________________________

# 17. Conflict Resolution Workflow

Typical workflow:

```bash
git status
```

Open the conflicted file and resolve:

```text
<<<<<<< HEAD
current branch
=======
incoming branch
>>>>>>> other-branch
```

Then:

```bash
git add <file>
git commit
```

For a rebase:

```bash
git add <file>
git rebase --continue
```

______________________________________________________________________

# 18. Good Conflict Resolution

Do not simply choose:

```text
ours
```

or:

```text
theirs
```

without understanding the intended behavior.

Instead ask:

```text
What was each change trying to accomplish?
```

Then produce the correct combined behavior.

______________________________________________________________________

# 19. Conflict Resolution Checklist

After resolving conflicts:

```text
1. Read the resulting code.
2. Check imports.
3. Check logic.
4. Run tests.
5. Run lint/type checks where applicable.
6. Review the diff.
```

A conflict-free merge can still contain a logical bug.

______________________________________________________________________

# 20. `git reset`

`reset` moves the current branch reference and can change the staging area and working tree depending on the mode.

Important modes:

```bash
git reset --soft
git reset --mixed
git reset --hard
```

______________________________________________________________________

# 21. `git reset --soft`

Moves `HEAD` while keeping changes staged.

Example:

```bash
git reset --soft HEAD~1
```

Useful when you want to undo the last commit but keep its changes ready for another commit.

______________________________________________________________________

# 22. `git reset --mixed`

This is the default reset mode.

It moves `HEAD` and resets the staging area, while keeping working-tree changes.

Example:

```bash
git reset HEAD~1
```

The changes remain in your files but are no longer staged.

______________________________________________________________________

# 23. `git reset --hard`

Moves `HEAD` and resets both the staging area and working tree.

Example:

```bash
git reset --hard HEAD~1
```

This can discard uncommitted changes.

Use it carefully.

______________________________________________________________________

# 24. Reset vs Revert

This is an important interview question.

### Reset

Changes branch history/reference.

Commonly appropriate for local/private history.

### Revert

Creates a new commit that reverses an earlier commit.

Example:

```text
A → B → C
```

Reverting `C` produces:

```text
A → B → C → C-revert
```

The original history remains intact.

______________________________________________________________________

# 25. When to Use Revert

If a bad commit is already part of shared history:

```bash
git revert <commit>
```

is generally safer than rewriting shared history.

It preserves the public history while undoing the change.

______________________________________________________________________

# 26. `git stash`

`stash` temporarily stores working-tree changes.

Example:

```bash
git stash
```

Later:

```bash
git stash pop
```

Useful when you need to temporarily switch context without committing incomplete work.

______________________________________________________________________

# 27. Stash Workflow

Example:

```bash
# unfinished work
git stash

git switch main
git pull

# handle urgent work

git switch feature/my-work
git stash pop
```

You can inspect stashes with:

```bash
git stash list
```

______________________________________________________________________

# 28. Stash Risks

Do not use stash as a permanent storage mechanism.

Important work should eventually become:

```text
A commit
```

or another properly backed-up form.

Stash is for temporary context switching.

______________________________________________________________________

# 29. Cherry-Pick

`cherry-pick` applies the changes introduced by a specific commit onto the current branch.

Example:

```bash
git cherry-pick abc123
```

Suppose:

```text
main:
A → B → C

feature:
A → B → C → D
```

Cherry-picking `D` onto another branch applies its changes there as a new commit.

______________________________________________________________________

# 30. When to Use Cherry-Pick

Useful for:

- Backporting a bug fix
- Applying a specific fix to a release branch
- Moving a small isolated change
- Recovering a useful commit

Be careful when the commit has dependencies on other commits.

______________________________________________________________________

# 31. Cherry-Pick Conflicts

If conflicts occur:

```bash
git status
```

Resolve the files, then:

```bash
git add <file>
git cherry-pick --continue
```

To abandon the operation:

```bash
git cherry-pick --abort
```

______________________________________________________________________

# 32. `git reflog`

`reflog` records movements of references such as `HEAD`.

It is extremely useful when you think:

> "I accidentally lost my commit."

Example:

```bash
git reflog
```

You may find an earlier `HEAD` position and recover it.

______________________________________________________________________

# 33. Recovering a Lost Commit

Suppose:

```bash
git reset --hard HEAD~3
```

accidentally removes useful commits from the visible branch history.

Check:

```bash
git reflog
```

Find the previous commit and create a recovery branch:

```bash
git switch -c recovery <commit>
```

This is one of Git's most valuable recovery techniques.

______________________________________________________________________

# 34. `git bisect`

`bisect` performs a binary search through commit history to identify which commit introduced a regression.

Start:

```bash
git bisect start
```

Mark current version as bad:

```bash
git bisect bad
```

Mark a known-good version:

```bash
git bisect good <commit>
```

Git checks out a midpoint.

You test it and mark:

```bash
git bisect good
```

or:

```bash
git bisect bad
```

Git repeats until the problematic commit is identified.

______________________________________________________________________

# 35. Why Bisect Is Powerful

Suppose there are:

```text
1,024 commits
```

A linear search could require testing hundreds of commits.

Binary search requires roughly:

```text
log2(1024) = 10
```

steps.

This is extremely useful for difficult regressions.

______________________________________________________________________

# 36. Automated Bisect

If a test can reliably identify good/bad versions, `git bisect run` can automate the search.

Conceptually:

```bash
git bisect run ./test-regression.sh
```

The command should return a status indicating whether the checked-out commit is good or bad.

______________________________________________________________________

# 37. Pull Requests

A pull request is a mechanism for proposing changes for review and integration.

A good PR should explain:

```text
What changed?
Why?
How was it tested?
Any risks?
Any migration/deployment considerations?
```

______________________________________________________________________

# 38. Good Pull Request Size

Prefer focused PRs.

Avoid combining:

```text
New API
+
Database migration
+
Large refactor
+
Formatting changes
+
Unrelated bug fixes
```

unless there is a strong reason.

Smaller focused PRs are easier to review and safer to merge.

______________________________________________________________________

# 39. PR Description

A practical structure:

```markdown
## What

Add user search endpoint.

## Why

Users need to search accounts by name/email.

## Testing

- Unit tests
- API tests

## Risks

Adds a database query and index.

## Deployment

Requires database migration.
```

______________________________________________________________________

# 40. Code Review

Code review is not just checking formatting.

Review:

### Correctness

Does the code do what it should?

### Design

Is the approach appropriate?

### Reliability

What happens when dependencies fail?

### Performance

Could this create:

```text
N+1
```

queries or expensive processing?

### Security

Are authorization, validation and sensitive data handled correctly?

### Maintainability

Will another engineer understand this code?

______________________________________________________________________

# 41. Good Review Comments

Prefer:

> "Could we validate that the requesting user owns this resource before returning it?"

over:

> "This is wrong."

Good review comments explain:

```text
Problem
Reason
Suggested direction
```

______________________________________________________________________

# 42. Blocking vs Non-Blocking Review Comments

A useful distinction:

### Blocking

The change should not merge because of:

- Correctness bug
- Security issue
- Data-loss risk
- Serious reliability problem

### Non-blocking

Suggestions such as:

- Naming
- Minor refactoring
- Style
- Future improvement

Teams may use different terminology, but the distinction helps keep reviews efficient.

______________________________________________________________________

# 43. Review the Diff, Not Just the Files

Use:

```bash
git diff
git diff --staged
```

and inspect the actual changes.

Look for:

- Accidental files
- Debug statements
- Secrets
- Unrelated changes
- Missing tests
- Incorrect migrations

______________________________________________________________________

# 44. Useful Git Inspection Commands

Common commands:

```bash
git status
git log --oneline --graph --decorate
git diff
git diff --staged
git show <commit>
git blame <file>
git reflog
```

Know what each command is useful for rather than memorizing syntax alone.

______________________________________________________________________

# 45. `git blame`

`git blame` shows which commit last changed each line.

Example:

```bash
git blame app/services/user.py
```

It can help answer:

```text
Who changed this?
Which commit introduced it?
```

Use it to find historical context, not to assign personal blame.

______________________________________________________________________

# 46. `git log`

Useful forms include:

```bash
git log --oneline
git log --graph --decorate --all
git log -p
```

For debugging, the graph view is especially useful for understanding branch history.

______________________________________________________________________

# 47. Rebase Conflict Recovery

During a rebase:

```bash
git status
```

Resolve conflicts, then:

```bash
git add <files>
git rebase --continue
```

To abandon the rebase:

```bash
git rebase --abort
```

This returns the branch to its previous state.

______________________________________________________________________

# 48. Merge Conflict Recovery

During a merge, if you want to abandon the operation:

```bash
git merge --abort
```

Then investigate the changes and retry when ready.

______________________________________________________________________

# 49. Safe Force Push

After rebasing your own remote feature branch, you may need to update it:

```bash
git push --force-with-lease
```

Prefer:

```text
--force-with-lease
```

over:

```text
--force
```

because it provides an additional safety check against overwriting unexpected remote changes.

______________________________________________________________________

# 50. Force Push Risks

A force push can rewrite remote branch history.

Before doing it:

```text
Know who uses the branch.
Confirm the branch is not shared unexpectedly.
Prefer --force-with-lease.
```

Protected branches such as `main` should normally reject force pushes.

______________________________________________________________________

# 51. Merge vs Rebase Interview Example

### Question

> Your feature branch is behind `main`. Would you merge `main` into the feature branch or rebase?

### Answer

"Both can be valid. Rebase gives me a linear history but rewrites the feature commits. Merge preserves the existing
history and is safer when the branch is shared. For a private feature branch, I may rebase onto the latest `main` before
opening or updating the PR, following the team's workflow."

______________________________________________________________________

# 52. Reset vs Revert Interview Example

### Question

> You pushed a bad commit to a shared branch. Would you reset it?

### Answer

"Usually no. I would use `git revert` because it creates a new commit that reverses the bad change without rewriting
shared history. I would use reset when I am intentionally rewriting private/local history."

______________________________________________________________________

# 53. Reflog Interview Example

### Question

> You accidentally ran `git reset --hard` and lost commits. Are they gone?

### Answer

"Not necessarily. I would check `git reflog` to find the previous `HEAD` position. If the commit is still reachable
through reflog/object storage, I can create a recovery branch pointing to it."

______________________________________________________________________

# 54. Bisect Interview Example

### Question

> A regression appeared somewhere across hundreds of commits. How would you find it?

### Answer

"I would use `git bisect`. I identify a known-good and known-bad commit, let Git check out midpoint commits and run the
relevant test at each step. This performs a binary search and can identify the introducing commit efficiently."

______________________________________________________________________

# 55. Cherry-Pick Interview Example

### Question

> A production bug fix exists on `main`, but the release branch needs the same fix. What would you do?

### Answer

"If the fix is isolated and appropriate for the release branch, I would cherry-pick the fix commit onto the release
branch, resolve any conflicts, run the relevant tests and create the appropriate release PR."

______________________________________________________________________

# 56. Git Workflow for a Backend Feature

A practical workflow:

```text
Update main
 ↓
Create feature branch
 ↓
Implement
 ↓
Test
 ↓
Commit coherent changes
 ↓
Push
 ↓
Open PR
 ↓
Review
 ↓
Resolve feedback
 ↓
Rebase/merge according to team policy
 ↓
CI
 ↓
Merge
 ↓
Deploy
 ↓
Monitor
```

______________________________________________________________________

# 57. Commit Quality

Good commits should generally be:

- Focused
- Descriptive
- Reviewable
- Buildable/testable where practical

Prefer:

```text
Add pagination to user endpoint
```

over:

```text
changes
```

______________________________________________________________________

# 58. Commit Message

A useful structure:

```text
Add pagination to user endpoint
```

For more context:

```text
Add pagination to user endpoint

Limit responses to bounded page sizes and return
next-page metadata for API consumers.
```

The exact convention depends on the project.

______________________________________________________________________

# 59. Git Hooks and CI

Git hooks can automate local checks such as:

```text
Formatting
Linting
Tests
Secret detection
```

CI should provide authoritative checks because local hooks can be bypassed.

______________________________________________________________________

# 60. Protected Branches

Production branches commonly have protections such as:

```text
No direct pushes
Required PR
Required reviews
Required CI
No force push
```

This reduces accidental changes to critical branches.

______________________________________________________________________

# 61. Git Tags and Releases

Tags can identify release points.

Example:

```bash
git tag v1.4.0
```

Tags are useful for:

- Release tracking
- Deployment traceability
- Rollback references
- Version identification

______________________________________________________________________

# 62. Git and Production Debugging

Git is an important debugging tool.

When investigating a production regression:

```text
Incident
 ↓
Identify affected version
 ↓
Compare commits
 ↓
Inspect deployment diff
 ↓
git log
 ↓
git bisect if necessary
 ↓
Identify regression
```

This connects directly with the production-debugging topic.

______________________________________________________________________

# 63. Git and Security

Git workflows should also protect against accidental secret exposure.

Before committing:

```text
Check configuration
Check environment files
Check credentials
Check generated files
```

Use appropriate secret-scanning tools in local/CI workflows.

______________________________________________________________________

# 64. Common Git Mistakes

## Mistake 1 — Force-pushing shared branches

Can destroy other people's work.

## Mistake 2 — Using `reset --hard` casually

Can discard uncommitted changes.

## Mistake 3 — Rebasing shared history

Can create unnecessary coordination problems.

## Mistake 4 — Resolving conflicts mechanically

Can introduce logical bugs.

## Mistake 5 — Huge PRs

Make review and debugging difficult.

## Mistake 6 — Meaningless commit messages

Make history harder to understand.

## Mistake 7 — Committing secrets

Creates a security incident.

## Mistake 8 — Using stash as permanent storage

Stash is intended for temporary work.

______________________________________________________________________

# 65. Git Interview Questions & Answers

## Q1. What is Git?

**Answer:**

Git is a distributed version-control system that tracks project history through commits and references, enabling
branching, collaboration, review and recovery.

______________________________________________________________________

## Q2. What is a Git branch?

**Answer:**

A branch is essentially a movable reference pointing to a commit. New commits move that reference forward.

______________________________________________________________________

## Q3. What is `HEAD`?

**Answer:**

`HEAD` represents the currently checked-out commit/reference.

______________________________________________________________________

## Q4. What is the difference between working tree and staging area?

**Answer:**

The working tree contains current file changes. The staging area contains the changes selected for the next commit.

______________________________________________________________________

## Q5. What is the difference between merge and rebase?

**Answer:**

Merge combines histories and can create a merge commit. Rebase replays commits on top of another base and creates new
commit identities, producing a more linear history.

______________________________________________________________________

## Q6. When should you avoid rebase?

**Answer:**

Avoid rewriting commits that other developers are already depending on unless the team explicitly coordinates the
history rewrite.

______________________________________________________________________

## Q7. What is a fast-forward merge?

**Answer:**

It occurs when the target branch has not diverged, allowing Git to simply move the branch pointer forward without
creating a merge commit.

______________________________________________________________________

## Q8. What is `git reset`?

**Answer:**

Reset moves the current branch reference and, depending on the mode, can also modify the staging area and working tree.

______________________________________________________________________

## Q9. Explain `--soft`, `--mixed` and `--hard`.

**Answer:**

`--soft` moves `HEAD` while preserving changes staged. `--mixed` moves `HEAD` and resets the index while preserving
working-tree changes. `--hard` also resets the working tree and can discard uncommitted changes.

______________________________________________________________________

## Q10. What is `git revert`?

**Answer:**

Revert creates a new commit that reverses the changes introduced by an earlier commit.

______________________________________________________________________

## Q11. Reset vs revert?

**Answer:**

Reset rewrites/moves local history references and is generally suited to private history. Revert preserves shared
history by adding an inverse commit.

______________________________________________________________________

## Q12. What is `git stash`?

**Answer:**

Stash temporarily stores working-tree/index changes so you can switch context without committing unfinished work.

______________________________________________________________________

## Q13. What is cherry-pick?

**Answer:**

Cherry-pick applies the changes from a specific commit onto the current branch as a new commit.

______________________________________________________________________

## Q14. What is reflog?

**Answer:**

Reflog records movements of references such as `HEAD`, making it useful for recovering commits after operations such as
accidental resets or rebases.

______________________________________________________________________

## Q15. Can reflog recover every lost commit forever?

**Answer:**

No. Reflog entries expire and unreachable objects can eventually be garbage-collected. Recovery should therefore be
attempted promptly.

______________________________________________________________________

## Q16. What is `git bisect`?

**Answer:**

It performs a binary search through commit history to identify the commit that introduced a regression.

______________________________________________________________________

## Q17. What is interactive rebase?

**Answer:**

It allows you to edit a sequence of commits, including reordering, rewording, squashing, fixing up or dropping commits.

______________________________________________________________________

## Q18. What is squashing?

**Answer:**

Squashing combines multiple commits into fewer commits, often to create a cleaner and more coherent final history.

______________________________________________________________________

## Q19. How do you resolve a merge conflict?

**Answer:**

I inspect the conflicting changes, understand the intent of both sides, edit the files into the correct final state,
stage the resolved files and complete the merge. Then I run tests and inspect the final diff.

______________________________________________________________________

## Q20. What is `--force-with-lease`?

**Answer:**

It force-updates a remote branch while checking that the remote reference is still what the local Git client expects. It
is safer than an unconditional `--force`.

______________________________________________________________________

## Q21. What is a pull request?

**Answer:**

A pull request proposes a set of changes for review, automated validation and eventual integration into another branch.

______________________________________________________________________

## Q22. What makes a good pull request?

**Answer:**

It is focused, explains the problem and solution, includes relevant tests, highlights risks and provides
deployment/migration information where necessary.

______________________________________________________________________

## Q23. What do you look for during code review?

**Answer:**

Correctness, security, authorization, performance, failure handling, data consistency, maintainability, testing and
operational impact.

______________________________________________________________________

## Q24. How would you review a database-heavy backend PR?

**Answer:**

I would inspect query behavior, indexes, transaction boundaries, N+1 risks, connection usage, locking, migration safety
and rollback considerations in addition to normal code correctness.

______________________________________________________________________

## Q25. How can Git help debug a production regression?

**Answer:**

Use deployment/version information to identify the relevant commits, inspect history and diffs, and use `git bisect`
when the introducing change is unknown.

______________________________________________________________________

## Q26. How do you recover from an accidental hard reset?

**Answer:**

Check `git reflog`, identify the previous commit/HEAD position and create a recovery branch or reset the branch back to
the recovered commit.

______________________________________________________________________

## Q27. Why are focused commits useful?

**Answer:**

They make history easier to understand, simplify code review, make targeted reverts/cherry-picks easier and improve
debugging with tools such as `git bisect`.

______________________________________________________________________

## Q28. Why should secrets never be committed?

**Answer:**

Git history can retain the secret even after it is removed from the latest version. A committed credential should be
treated as exposed and rotated/revoked.

______________________________________________________________________

## Q29. What would you do if you committed a secret locally but haven't pushed?

**Answer:**

Remove it from the commit/history as appropriate, ensure the secret is not retained in another tracked form and use
proper secret management. If the secret was actually exposed outside the trusted environment, rotate it.

______________________________________________________________________

## Q30. What would you do if the secret was pushed to a shared repository?

**Answer:**

Treat it as compromised: rotate/revoke it immediately, assess exposure, remove the secret from the repository/history
using the team's approved procedure and improve secret-scanning/prevention controls.

______________________________________________________________________

## Q31. Merge or rebase before a PR?

**Answer:**

Either can be correct depending on team policy. For a private feature branch, I may rebase onto the latest target branch
to keep history clean. For shared branches, I avoid rewriting history and use the team's agreed merge strategy.

______________________________________________________________________

## Q32. Why can a clean Git history matter for a backend team?

**Answer:**

It improves traceability and makes debugging, rollback, code archaeology, cherry-picking and regression investigation
easier.

______________________________________________________________________

## Q33. What is the difference between `git diff` and `git diff --staged`?

**Answer:**

`git diff` shows unstaged working-tree changes. `git diff --staged` shows changes currently staged for the next commit.

______________________________________________________________________

## Q34. What is `git blame` used for?

**Answer:**

It identifies the commit associated with each line, which can help locate historical context and investigate why a line
exists. It should not be used as a tool for assigning personal blame.

______________________________________________________________________

## Q35. Give a senior-level Git workflow answer.

**Answer:**

"I prefer small, focused feature branches and coherent commits. I keep branches synchronized with the target branch
using the team's agreed merge/rebase strategy, run tests and checks before opening a PR, and keep PRs small enough for
meaningful review. For history manipulation I distinguish private from shared history: reset/rebase are useful for
private work, while revert is safer for shared history. I also use reflog for recovery and bisect for difficult
regressions. In code review I look beyond style at correctness, security, database behavior, performance, failure
handling and operational impact."

______________________________________________________________________

# 66. Scenario-Based Practice

## Scenario 1 — Bad Commit Already on Main

A deployment introduced a serious bug.

### Question

Would you reset `main`?

### Answer

Usually no. Since `main` is shared history, use a revert commit or the team's approved rollback process. Then
investigate the original change.

______________________________________________________________________

## Scenario 2 — Lost Commits

You accidentally run:

```bash
git reset --hard HEAD~5
```

### Question

What do you do?

### Answer

Immediately inspect:

```bash
git reflog
```

Find the previous `HEAD` and recover the desired commit through a branch or reset.

______________________________________________________________________

## Scenario 3 — Regression Across 500 Commits

### Question

How do you find the offending commit?

### Answer

Use:

```bash
git bisect
```

with a reliable regression test.

______________________________________________________________________

## Scenario 4 — Release Branch Needs One Production Fix

### Question

How do you move only that fix?

### Answer

If the commit is isolated and compatible:

```bash
git cherry-pick <commit>
```

Then test the release branch.

______________________________________________________________________

## Scenario 5 — Feature Branch Has 15 Messy Commits

History:

```text
fix
fix
oops
test
review
fix
final
```

### Question

What can you do?

### Answer

Use interactive rebase to reorder, squash and reword commits before integrating them, assuming the branch is private or
history rewriting is coordinated.

______________________________________________________________________

## Scenario 6 — Merge Conflict

A conflict occurs in authentication code.

### Question

Would you select "ours" automatically?

### Answer

No. Authentication is security-sensitive. Understand the intent of both changes, produce the correct combined
implementation and run the relevant tests.

______________________________________________________________________

## Scenario 7 — Force Push

You rebased your private feature branch and need to update the remote.

### Answer

Use:

```bash
git push --force-with-lease
```

rather than unconditional `--force`, after confirming the branch is not unexpectedly shared.

______________________________________________________________________

## Scenario 8 — Large PR

A PR contains:

```text
API feature
DB migration
Refactoring
Formatting
Unrelated bug fix
```

### Question

What would you suggest?

### Answer

Split unrelated changes into focused PRs where practical. This reduces review complexity and makes rollback/debugging
easier.

______________________________________________________________________

# 67. Practical Command Cheat Sheet

### Status

```bash
git status
```

### Create branch

```bash
git switch -c feature/name
```

### Switch branch

```bash
git switch main
```

### Stage

```bash
git add <file>
```

### Commit

```bash
git commit -m "Meaningful message"
```

### Log

```bash
git log --oneline --graph --decorate --all
```

### Diff

```bash
git diff
git diff --staged
```

### Merge

```bash
git merge <branch>
```

### Rebase

```bash
git rebase <branch>
```

### Interactive rebase

```bash
git rebase -i HEAD~N
```

### Revert

```bash
git revert <commit>
```

### Reset

```bash
git reset --soft HEAD~1
git reset HEAD~1
git reset --hard HEAD~1
```

### Stash

```bash
git stash
git stash list
git stash pop
```

### Cherry-pick

```bash
git cherry-pick <commit>
```

### Reflog

```bash
git reflog
```

### Bisect

```bash
git bisect start
git bisect bad
git bisect good <commit>
```

### Abort operations

```bash
git merge --abort
git rebase --abort
git cherry-pick --abort
```

______________________________________________________________________

# 68. Final Interview Readiness Checklist

Before moving to DSA, make sure you can:

- [ ] Explain Git's working tree, staging area and commits.
- [ ] Explain `HEAD`.
- [ ] Explain branches.
- [ ] Create and manage feature branches.
- [ ] Explain merge.
- [ ] Explain fast-forward merge.
- [ ] Explain rebase.
- [ ] Compare merge and rebase.
- [ ] Explain why rebasing shared history is risky.
- [ ] Resolve merge conflicts.
- [ ] Resolve rebase conflicts.
- [ ] Explain `reset`.
- [ ] Explain `--soft`.
- [ ] Explain `--mixed`.
- [ ] Explain `--hard`.
- [ ] Compare reset and revert.
- [ ] Explain stash.
- [ ] Explain cherry-pick.
- [ ] Resolve cherry-pick conflicts.
- [ ] Explain squashing.
- [ ] Use interactive rebase.
- [ ] Explain reflog.
- [ ] Recover accidentally lost commits.
- [ ] Explain `git bisect`.
- [ ] Use automated bisect.
- [ ] Explain pull requests.
- [ ] Create focused PRs.
- [ ] Review backend code.
- [ ] Review security implications.
- [ ] Review database/performance implications.
- [ ] Use `git diff`.
- [ ] Use `git log`.
- [ ] Use `git blame`.
- [ ] Understand `--force-with-lease`.
- [ ] Explain protected branches.
- [ ] Explain tags/releases.
- [ ] Explain Git's role in production debugging.
- [ ] Explain Git's role in security.
- [ ] Answer senior-level workflow questions.

______________________________________________________________________

# 69. Final Takeaways

For a 5+ year backend engineer, Git knowledge should go beyond:

```text
clone
add
commit
push
pull
```

You should be comfortable reasoning about:

```text
History
Branches
Integration
Conflict resolution
Recovery
Regression investigation
Code review
Release workflow
```

The most important distinctions to remember are:

| Situation | Typical Tool |
|---|---|
| Undo private commit/history | `reset` |
| Undo shared commit | `revert` |
| Clean private commits | interactive `rebase` |
| Temporarily save work | `stash` |
| Move one commit | `cherry-pick` |
| Recover lost history | `reflog` |
| Find regression | `bisect` |
| Combine branch histories | `merge` |
| Update private branch onto new base | `rebase` |

The senior-level principle is:

> **Use Git history deliberately. Preserve shared history, rewrite private history when useful, and make every change easy to review, recover and debug.**

______________________________________________________________________

**Previous:** [33. Backend Security](./33-security.md)

**Next:** [35. DSA Fundamentals](./35-dsa-foundations.md)
