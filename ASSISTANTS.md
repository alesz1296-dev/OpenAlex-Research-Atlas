# Assistant Working Rules

This file defines the project Git workflow standard and operating rules for any assistant working in this repository.

## Required Startup Read

Before doing any work in this project, the assistant must read all project Markdown files in the repository root first.

Minimum required reads:

- `README.md`
- `architecture.md`
- `working-standard.md`
- `specs.md`
- `phases.md`
- `logs.md`
- `ASSISTANTS.md`

No code edits, git operations, architecture decisions, or implementation work should begin until those files have been read for the current session.

## Project Context Recovery Rule

Project Markdown files are the persistent memory of the project.

Assistants must:

- read root `.md` files to recover context
- use them before making decisions
- update them when the project meaningfully changes
- keep documentation aligned with implementation as the project evolves

## Git Workflow Standard

### Branches

Never work directly on `main`.

Create a dedicated branch for every feature, bug fix, refactor, or documentation change.

Examples:

```bash
git checkout -b feat/google-login
git checkout -b fix/login-validation
git checkout -b refactor/auth-components
git checkout -b docs/setup-guide
```

Branch naming:

- `feat/`
- `fix/`
- `refactor/`
- `docs/`
- `chore/`

### Keep Local Repository Updated

Before starting work:

```bash
git pull
```

### Review Changes

Always inspect changes before staging:

```bash
git status
git diff
```

### Stage Files Explicitly

Never stage blindly.

Preferred:

```bash
git add file1 file2
```

Avoid:

```bash
git add .
```

Use `git add .` only when changes have been reviewed and are intentionally included.

### Verify Staged Changes

Before committing:

```bash
git status
git diff --staged
```

### Commit Messages

Use Conventional Commits.

Examples:

```text
feat: add Google OAuth login
fix: resolve theme selector persistence
refactor: simplify authentication form state
docs: update setup instructions
chore: upgrade dependencies
```

Types:

- `feat:` new functionality
- `fix:` bug fix
- `refactor:` code restructuring without behavior changes
- `docs:` documentation changes
- `chore:` tooling, dependencies, configuration

Avoid:

- `update`
- `changes`
- `fix stuff`
- `misc`
- `wip`

### Push Changes

```bash
git push -u origin <branch-name>
```

### Pull Requests

All changes must reach `main` through a Pull Request.

Do not merge directly into `main`.

PR requirements:

- Build passes.
- Tests pass.
- Changes reviewed.
- Scope is focused.
- Description explains the purpose of the change.

### Branch Cleanup

After a branch has been merged:

```bash
git branch -d <branch-name>
```

### Security Rules

Never commit:

- `.env`
- `.env.local`
- API keys
- secrets
- credentials
- certificates

Always verify sensitive files are not staged.

### Commit Scope

One commit equals one logical change.

Do not mix bug fixes, new features, refactors, and documentation in a single commit whenever possible.

## Assistant Rules

The assistant must:

- Never commit automatically.
- Never push automatically.
- Never merge automatically.
- Never delete branches automatically.
- Always ask for approval before any git write operation.
- Explain proposed git actions before executing them.
- Always conclude task updates with:
  - what was completed,
  - what is pending for the current phase,
  - an overview of the changes made.

Git commands that require explicit approval:

- `git commit`
- `git push`
- `git merge`
- `git rebase`
- `git reset`
- `git branch -d`
- `git tag`

## Logging Rules

Every working session by `alesz1296-dev` must be recorded in `logs.md`.

Every user-made commit must be recorded in `logs.md`.
