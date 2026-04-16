# Changelog

## Unreleased

### Added

- project-management doc set under `docs/`
- local-first git workflow definition
- phase roadmap and task backlog for long-running work
- source-policy documentation for source classifications and blocked-source handling
- milestone validation checklist and first release checklist
- measured-replacement priority doc for the four remaining proxy-to-measured backlog items
- catalog gap review for family-by-family asset coverage depth
- selected USGS v7 subset ingest documentation and generic camera-profile documentation

### Changed

- repository governance now treats generated assets, exports, raw-source records, and validation outputs as tracked artifacts
- blocked `403` source pages are explicitly documented with impact and fallback handling instead of remaining only as ledger failures
- rebuild tooling now preserves prior tracked timestamps by default to reduce non-semantic diff churn
- build tooling now reuses frozen raw sources by default and requires explicit opt-in for source refreshes
- backlog governance now ranks measurement backlog items and documents that the current catalog is count-complete but not depth-complete
- build tooling now freezes a selected local USGS v7 subset into tracked `raw/` inputs instead of relying on the full local mirror
- scenarios now reference a generic `RGB+NIR` camera profile
- dry asphalt, concrete, and galvanized metal are now measured USGS-derived baselines, and wet asphalt is a measured-derived material

### Validation

- validation summary now includes `1` camera profile and zero camera-profile validation errors
- material quality summary now reports `3` `measured_standard`, `1` `measured_derivative`, `16` `project_proxy`, and `0` `vendor_derived` materials

## Baseline

### Added

- engine-agnostic autonomous-driving camera simulation asset-pack baseline
- tracked `canonical/`, `exports/`, `raw/`, `validation/`, `schemas/`, and generator scripts
- local repository baseline for future milestone work

### Validation

- baseline reports show `35` assets, `20` spectral materials, `4` emissive profiles, and `4` scenario profiles
- current GLB validation covers `39` files with `0` errors and `0` warnings
- current release-gate summary passes

### Known Gaps

- `403` fetch failures remain for several external reference pages
- generated outputs still contain `generated_at` metadata, but default tooling now preserves prior values and explicit refreshes remain review-sensitive
- automotive sensor SRF, signal/headlamp SPD, wet-road BRDF, and retroreflective BRDF remain measurement backlog items
