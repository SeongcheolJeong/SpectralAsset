# Milestone Validation Checklist

Use this checklist before merging a milestone-sized change to `main` or before cutting a local release tag.

## Schema and Metadata

- asset manifests resolve and remain in the expected filename format
- spectral material references point to existing tracked curves
- emissive and scenario profiles resolve correctly
- provenance and license fields remain populated for newly changed assets

## Build and Export

- `python3 scripts/build_asset_pack.py` completes successfully
- `node scripts/validate_gltf.mjs exports/gltf validation/reports/gltf_validation.json` completes successfully
- USD exports remain readable
- tracked generated outputs changed only where expected

## Spectral and Material Fidelity

- measured vs proxy status is clear for every newly introduced spectral input
- any fidelity-tier change is reflected in docs and changelog
- proxy curves introduced for simulation convenience are explicitly marked as such in review notes or docs

## Geometry and Asset Acceptance

- naming remains snake_case and consistent with current contracts
- new asset additions satisfy the acceptance criteria in [asset-spec.md](asset-spec.md)
- semantic class and variant key are present for changed assets

## Validation Reports

- `validation/reports/validation_summary.json` still reflects the intended baseline
- glTF validation remains clean or any exception is documented
- visual, semantic, and backlog implications are reviewed for milestone changes

## Rebuild Review

- rebuild diffs were checked for semantic changes versus metadata-only churn
- `generated_at` diffs were not committed blindly
- if timestamps changed intentionally, the reason is documented in the commit or changelog

## Known Gaps Review

- measurement backlog items are still accurate
- blocked-source documentation is still accurate
- no doc claims measured replacements or remote-hosting setup that does not exist

