# Git Workflow

## Repository Initialization

Local-first bootstrap uses this flow:

```bash
git init -b main
git add .
git commit -m "chore(repo): initialize local repository with current asset-pack baseline"
```

Working branches are created from `main`:

```bash
git switch -c codex/<area>-<slug>
```

Examples:

- `codex/docs-bootstrap`
- `codex/source-hardening`
- `codex/material-fidelity`

## What Is Tracked vs Ignored

Tracked artifacts:

- `canonical/`
- `exports/`
- `raw/`
- `validation/`
- `schemas/`
- `scripts/`
- `package.json`
- `package-lock.json`
- project docs and research markdown files

Ignored artifacts:

- `node_modules/`
- `__pycache__/`
- `*.pyc`
- `.DS_Store`
- local throwaway temp files not intended as source of truth

Policy:

- generated assets and reports are intentionally tracked
- dependency directories are not tracked
- `package-lock.json` is tracked to keep the validator/runtime environment reproducible

## Branch Strategy

- default branch: `main`
- working branches: `codex/<area>-<slug>`
- keep branches narrow to one deliverable or one tightly related set of changes
- rebase or fast-forward from `main` before merging if drift appears

## Commit Message Convention

Allowed prefixes:

- `chore`
- `docs`
- `feat`
- `fix`
- `build`
- `data`
- `validate`

Format:

```text
<prefix>(<scope>): <summary>
```

Examples:

- `docs(project): add roadmap backlog asset spec and git workflow`
- `docs(readme): link management docs from repository entrypoints`
- `data(source): update source ledger classifications`

## Merge Policy

- prefer `--ff-only` merges into `main`
- avoid merge commits for routine local-first work
- do not amend published history unless explicitly required
- review generated-output diffs before merging, especially when many files changed

Recommended local merge flow:

```bash
git switch main
git merge --ff-only codex/<area>-<slug>
```

## Rebuild Policy for Generated Outputs

Generated folders are tracked, so rebuilds must be reviewed carefully.

Rules:

- do not commit rebuild output blindly
- identify whether diffs are semantic or only metadata churn
- treat `generated_at` changes by themselves as non-semantic churn
- if a rebuild changes only timestamps, do not commit it unless the commit purpose is an explicit baseline refresh
- if a rebuild changes assets semantically, update docs and validation context with the reason

Current known issue:

- [../scripts/build_asset_pack.py](../scripts/build_asset_pack.py) embeds `generated_at` timestamps in many tracked files, so clean rebuilds can produce noisy diffs

## Release/Tag Policy

- no release tags are created during the local bootstrap phase
- first formal milestone tags should be annotated and follow `v0.x.y`
- only tag after validation, source-policy review, and known-gap review are complete

## Future Remote-Hosting Notes

- remote hosting is deferred for now
- when a remote is added later, keep `main` as the protected/default branch
- mirror the existing branch naming and commit conventions
- add PR/review templates only after the local workflow is stable

