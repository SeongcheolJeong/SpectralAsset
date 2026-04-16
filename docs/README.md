# Project Management Docs

This directory is the management layer for the autonomous-driving camera simulation asset pack. Use it to understand scope, execution order, git rules, and open work without reverse-engineering the generated assets.

## Document Map

- [project-overview.md](project-overview.md): stable snapshot of current scope, repo state, constraints, and validation status
- [roadmap.md](roadmap.md): phase-level delivery plan from repo governance through release hardening
- [task-backlog.md](task-backlog.md): live backlog with task IDs, priorities, dependencies, and done criteria
- [asset-spec.md](asset-spec.md): naming, catalog, manifest, and asset-acceptance contract
- [measurement-priorities.md](measurement-priorities.md): ranked plan for replacing the current highest-value proxy measurement gaps
- [catalog-gap-review.md](catalog-gap-review.md): family-by-family review of current asset coverage and the next expansion priorities
- [camera-profile.md](camera-profile.md): generic `RGB+NIR` camera-profile contract and current vendor-derived limits
- [created-assets.md](created-assets.md): explanation of what the generated asset pack actually creates and how those files relate
- [file-formats.md](file-formats.md): explanation of `.npz`, `.json`, `USD`, and related generated file types
- [pbrt-tutorial.md](pbrt-tutorial.md): workflow for converting the generated assets into a practical `PBRT` rendering pipeline
- [usgs-ingest.md](usgs-ingest.md): selected USGS v7 subset ingest, active bindings, and reference-only safeguards
- [source-policy.md](source-policy.md): source classifications, blocked-source handling, and licensing-use notes
- [validation-checklist.md](validation-checklist.md): milestone validation gates for generated assets and scenes
- [release-checklist.md](release-checklist.md): first local-release readiness checklist
- [git-workflow.md](git-workflow.md): local-first git operating rules for this repository
- [../CHANGELOG.md](../CHANGELOG.md): human-readable history of baseline and future changes

## Update Rules

- Update [project-overview.md](project-overview.md) when counts, constraints, or repo-state assumptions change.
- Update [roadmap.md](roadmap.md) only when phase boundaries, goals, or dependency order change.
- Update [task-backlog.md](task-backlog.md) for all task status changes. This is the only live task board.
- Update [asset-spec.md](asset-spec.md) before changing naming rules, manifest contracts, or asset acceptance rules.
- Update [measurement-priorities.md](measurement-priorities.md) when the measured-replacement order or acquisition assumptions change.
- Update [catalog-gap-review.md](catalog-gap-review.md) when family counts, coverage weaknesses, or expansion priorities change.
- Update [camera-profile.md](camera-profile.md) when camera-profile fields, source-quality assumptions, or scenario binding rules change.
- Update [created-assets.md](created-assets.md) when generated asset categories, counts, or file relationships change materially.
- Update [file-formats.md](file-formats.md) when the repository adds a new primary generated format or changes the role of an existing one.
- Update [pbrt-tutorial.md](pbrt-tutorial.md) when the recommended `PBRT` conversion path, active camera profile, or primary source asset paths change.
- Update [usgs-ingest.md](usgs-ingest.md) when the selected subset, binding policy, or local-source handling changes.
- Update [source-policy.md](source-policy.md) when source classifications, fetch status handling, or licensing-use assumptions change.
- Update [validation-checklist.md](validation-checklist.md) when milestone validation gates or pass criteria change.
- Update [release-checklist.md](release-checklist.md) when release readiness rules or release inputs change.
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
