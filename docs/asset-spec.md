# Asset Specification

## Asset Families and Current Catalog

Current generated catalog:

- `traffic_sign`: `56` assets
- `traffic_light`: `29` assets
- `road_surface`: `33` assets
- `road_marking`: `51` assets
- `road_furniture`: `61` assets

Current scenario and validation support:

- `4` scenario profiles
- `4` validation scenes
- `27` spectral materials
- `22` emissive profiles
- `3` camera profiles

## Naming Conventions

Use snake_case for all generated identifiers. Existing generated IDs are the contract.

Required file patterns:

- asset manifest: `<asset_id>.asset_manifest.json`
- spectral material: `<material_id>.spectral_material.json`
- emissive profile: `<profile_id>.emissive_profile.json`
- camera profile: `<camera_id>.camera_profile.json`
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
- camera profile IDs use `camera_` prefixes
- scenario IDs use `scenario_` prefixes
- atmosphere IDs use `atmosphere_` prefixes
- scene IDs use `scene_` prefixes

## Manifest Relationships

- `canonical/manifests/*.asset_manifest.json` is the top-level contract for each asset.
- asset manifests reference material IDs used by the asset geometry.
- spectral materials reference one or more curves in `canonical/spectra/`.
- traffic-light asset manifests reference emissive profile IDs via state maps.
- camera profiles reference raw/effective SRF curves and either a shared optics-transmittance curve or per-channel optics/filter curves.
- scenario profiles reference illuminants, atmosphere files, and exactly one camera profile.
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

## Source Quality States

The repository currently uses four tracked source-quality states. This split must stay explicit in docs, reviews, and future upgrades.

### `measured_standard`

These are standards or published reference datasets with direct physical meaning and strong provenance.

Examples:

- `illuminant_d65.npz`
- `illuminant_am1_5_global_tilt.npz`
- `illuminant_am1_5_direct.npz`
- `mat_asphalt_dry_reflectance.npz`
- `mat_concrete_reflectance.npz`
- `mat_metal_galvanized_reflectance.npz`

### `measured_derivative`

These are curves derived from a measured baseline plus a tracked project modifier or transformation.

Examples:

- `mat_asphalt_wet_reflectance.npz`

### `vendor_derived`

These are profiles derived from public vendor documentation rather than a directly frozen measured raw dataset.

Examples:

- `camera_reference_rgb_nir_v1.camera_profile.json`
- `camera_reference_rgb_nir_v2.camera_profile.json`
- `camera_reference_rgb_nir_v3.camera_profile.json`
- `emissive_vehicle_standard.emissive_profile.json`
- `emissive_protected_turn.emissive_profile.json`

### `project_proxy`

These are project-generated curves used to approximate material behavior where measured automotive-grade data is not yet available.

Examples:

- sign reflectance curves such as `mat_sign_stop_red_reflectance.npz`
- road and marking curves such as `mat_marking_white_reflectance.npz`
- modifier curves such as `mat_retroreflective_gain.npz`
- pedestrian and countdown emissive SPDs such as `spd_led_red.npz` and `spd_led_countdown_amber.npz`
- optics/transmittance proxies such as `mat_glass_lens_transmittance.npz`

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
- `source_quality` and `source_ids` are filled in consistently with the tracked raw-source ledger
- checklist items in [validation-checklist.md](validation-checklist.md) are either passed or consciously deferred with a written reason

## Proxy-Data Limitations

The current repository mixes open standards, frozen source references, vendor-derived profiles, and project-generated proxy data. Until measured replacements land:

- sign and marking materials remain simulation proxies rather than measured traffic-control coatings
- vehicle and protected-turn traffic-signal SPDs are vendor-derived fits rather than measured captures
- pedestrian red/walk/countdown emissive SPDs still remain proxy curves
- wet-road and retroreflective behavior remain approximation-heavy
- the generic camera profiles are vendor-derived rather than measured single-SKU automotive SRFs
- docs and backlog must continue to distinguish measured truth from proxy assets

Current policy:

- source-quality labels must be visible in docs and review context even when filenames do not include a `proxy` suffix
- measured replacements should preserve stable IDs where possible and record the fidelity change in [../CHANGELOG.md](../CHANGELOG.md)
