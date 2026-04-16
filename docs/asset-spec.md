# Asset Specification

## Asset Families and Current Catalog

Current generated catalog:

- `traffic_sign`: `18` assets
- `traffic_light`: `5` assets
- `road_surface`: `4` assets
- `road_marking`: `4` assets
- `road_furniture`: `4` assets

Current scenario and validation support:

- `4` scenario profiles
- `4` validation scenes
- `20` spectral materials
- `4` emissive profiles

## Naming Conventions

Use snake_case for all generated identifiers. Existing generated IDs are the contract.

Required file patterns:

- asset manifest: `<asset_id>.asset_manifest.json`
- spectral material: `<material_id>.spectral_material.json`
- emissive profile: `<profile_id>.emissive_profile.json`
- scenario profile: `<scenario_id>.scenario_profile.json`
- spectra: `<curve_id>.npz`
- USD geometry: `<asset_id>.usda`
- USD export: `<asset_id>.usdc`
- GLB export: `<asset_id>.glb`
- sign template: `<asset_id>.svg`
- scene file: `<scene_id>.usda`

Naming domains:

- asset IDs use family-specific semantic names such as `sign_stop`, `signal_vehicle_vertical_3_aspect`, and `road_asphalt_dry`
- material IDs use `mat_` prefixes such as `mat_sign_stop_red`
- emissive profile IDs use `emissive_` prefixes
- scenario IDs use `scenario_` prefixes
- atmosphere IDs use `atmosphere_` prefixes
- scene IDs use `scene_` prefixes

## Manifest Relationships

- `canonical/manifests/*.asset_manifest.json` is the top-level contract for each asset.
- asset manifests reference material IDs used by the asset geometry.
- spectral materials reference one or more curves in `canonical/spectra/`.
- traffic-light asset manifests reference emissive profile IDs via state maps.
- scenario profiles reference illuminants and atmosphere files.
- scenes compose asset instances and point to geometry exports.

## Generated vs Source-of-Truth Files

Source-of-truth in-repo:

- [../scripts/build_asset_pack.py](../scripts/build_asset_pack.py): generation rules and catalog definitions
- [../schemas/](../schemas/): manifest/profile schema definitions
- [../raw/source_ledger.json](../raw/source_ledger.json): raw-source status and checksums
- [../deep-research-report.md](../deep-research-report.md): research rationale and acquisition priorities

Tracked generated outputs:

- `canonical/`
- `exports/`
- `raw/`
- `validation/`

Operational rule:

- generated outputs are version-controlled because review and milestone comparison must work from git alone
- rebuilds must still be reviewed for semantic changes versus timestamp-only churn

## Fidelity Tiers

The repository currently uses three fidelity tiers. This split must stay explicit in docs, reviews, and future upgrades.

### Tier A: Open Measured Standards

These are standards or published reference datasets with direct physical meaning and strong provenance.

Examples:

- `illuminant_d65.npz`
- `illuminant_am1_5_global_tilt.npz`
- `illuminant_am1_5_direct.npz`

### Tier B: Project Proxy Spectral Curves

These are project-generated curves used to approximate material behavior where measured automotive-grade data is not yet available.

Examples:

- sign reflectance curves such as `mat_sign_stop_red_reflectance.npz`
- road and marking curves such as `mat_asphalt_dry_reflectance.npz`
- modifier curves such as `mat_retroreflective_gain.npz`

### Tier C: Project Proxy Emissive Curves

These are project-generated SPDs used for traffic lights and similar emitters until measured replacements land.

Examples:

- `spd_led_red.npz`
- `spd_led_green.npz`
- `spd_led_countdown_amber.npz`

Upgrade rule:

- a proxy asset can be promoted to measured status only after its raw source, acquisition conditions, uncertainty, and provenance are recorded in tracked project metadata

## Validation Expectations

Every accepted asset addition should satisfy these expectations:

- naming follows the established snake_case conventions
- the asset has a manifest in `canonical/manifests/`
- referenced materials and curves resolve to existing tracked files
- USD and GLB exports are present when the asset is intended for runtime use
- semantic class, variant key, and provenance are filled in
- validation reports are updated or explicitly noted if a rebuild is deferred

Asset addition acceptance criteria:

- manifest exists and matches the naming contract
- material references resolve
- geometry/export files are generated successfully
- validation impact is reviewed
- provenance and license notes are present
- measured or proxy status is explicitly stated for any new spectral input
- checklist items in [validation-checklist.md](validation-checklist.md) are either passed or consciously deferred with a written reason

## Proxy-Data Limitations

The current repository mixes open standards, frozen source references, and project-generated proxy data. Until measured replacements land:

- some materials are simulation proxies rather than measured automotive-grade curves
- traffic-light emissive SPDs are placeholders for measured replacements
- wet-road and retroreflective behavior remain approximation-heavy
- docs and backlog must continue to distinguish measured truth from proxy assets

Current policy:

- tier labels must be visible in docs and review context even when filenames do not include a `proxy` suffix
- measured replacements should preserve stable IDs where possible and record the fidelity change in [../CHANGELOG.md](../CHANGELOG.md)
