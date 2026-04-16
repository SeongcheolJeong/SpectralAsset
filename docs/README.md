# Project Management Docs

This directory is the management layer for the autonomous-driving camera simulation asset pack. Use it to understand scope, execution order, git rules, and open work without reverse-engineering the generated assets.

## Document Map

- [project-overview.md](project-overview.md): stable snapshot of current scope, repo state, constraints, and validation status
- [roadmap.md](roadmap.md): phase-level delivery plan from repo governance through release hardening
- [task-backlog.md](task-backlog.md): live backlog with task IDs, priorities, dependencies, and done criteria
- [asset-spec.md](asset-spec.md): naming, catalog, manifest, and asset-acceptance contract
- [source-policy.md](source-policy.md): source classifications, blocked-source handling, and licensing-use notes
- [git-workflow.md](git-workflow.md): local-first git operating rules for this repository
- [../CHANGELOG.md](../CHANGELOG.md): human-readable history of baseline and future changes

## Update Rules

- Update [project-overview.md](project-overview.md) when counts, constraints, or repo-state assumptions change.
- Update [roadmap.md](roadmap.md) only when phase boundaries, goals, or dependency order change.
- Update [task-backlog.md](task-backlog.md) for all task status changes. This is the only live task board.
- Update [asset-spec.md](asset-spec.md) before changing naming rules, manifest contracts, or asset acceptance rules.
- Update [source-policy.md](source-policy.md) when source classifications, fetch status handling, or licensing-use assumptions change.
- Update [git-workflow.md](git-workflow.md) before changing branch, merge, artifact-tracking, or release policy.
- Update [../CHANGELOG.md](../CHANGELOG.md) when work is merged to `main` or when a baseline/release-worthy milestone is created.

## Status Legend

- `planned`: scoped and ready, but not started
- `in_progress`: actively being worked
- `blocked`: cannot proceed because of an external or unresolved dependency
- `done`: completed and accepted into the current working baseline

## Where Current Truth Comes From

- [../README.md](../README.md): user-facing repo entrypoint and build/use summary
- [../deep-research-report.md](../deep-research-report.md): research context, source rationale, and measurement gaps
- [../validation/reports/validation_summary.json](../validation/reports/validation_summary.json): current asset/material/scenario counts and release-gate status
- [../validation/reports/gltf_validation.json](../validation/reports/gltf_validation.json): glTF validation coverage for generated exports
- [../raw/source_ledger.json](../raw/source_ledger.json): raw-source fetch status, checksum ledger, and current 403 failures
- [../scripts/build_asset_pack.py](../scripts/build_asset_pack.py): generator rules, catalog definitions, naming, and `generated_at` timestamp behavior
