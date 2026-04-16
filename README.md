# Autonomous Driving Camera Simulation Asset Pack v1

This repository generates an engine-agnostic asset pack for autonomous driving camera simulation:

- `USD` master assets in `canonical/geometry/usd/`
- `glTF/GLB` exports in `exports/gltf/`
- spectral sidecars in `canonical/spectra/` and `canonical/materials/`
- scenario and validation scenes in `canonical/scenes/`
- validation reports in `validation/reports/`

## Build

```bash
npm install
python3 scripts/build_asset_pack.py
node scripts/validate_gltf.mjs exports/gltf validation/reports/gltf_validation.json
```

For deterministic rebuild review, the generator now preserves the previous tracked `generated_at` value by default and reuses frozen raw sources unless you explicitly refresh them. Use `BUILD_TIMESTAMP` or `SOURCE_DATE_EPOCH` only when you intentionally want to refresh timestamps, and `REFRESH_SOURCES=1` only when you intentionally want to refetch raw sources.

`python3 scripts/build_asset_pack.py` is idempotent. It will:

1. create the repository layout
2. download and checksum raw source references where practical
3. freeze the selected local USGS subset into tracked `raw/` inputs when the mirror is available
4. normalize official D65, ASTM G173, and selected USGS material inputs
5. generate measured, measured-derived, vendor-derived, and proxy spectral assets as applicable
6. emit a generic `RGB+NIR` camera profile, SVG sign templates, USD assets, GLB exports, manifests, scenario profiles, scenes, and reports
6. validate manifests, spectral coverage, and USD parsing

## Important Defaults

- Coordinate system: right-handed, `Y-up`, meters
- Master spectral grid: `350-1700 nm`, `1 nm`
- Runtime derived grid: `400-1100 nm`, `5 nm`
- Sensor branch: `RGB+NIR` silicon camera
- scenarios now bind to `canonical/camera/camera_reference_rgb_nir_v2.camera_profile.json`
- `camera_reference_rgb_nir_v1` is retained as the earlier vendor-derived baseline for comparison
- selected USGS v7 dry-material baselines are used for asphalt, concrete, and galvanized metal
- wet asphalt is currently a measured-derived material built from the measured dry asphalt baseline plus the tracked wet modifier
- vehicle and protected-turn traffic-signal emissive profiles now use vendor-derived public LED fits
- camera profiles now support either a shared optics curve or per-channel optics/filter curves
- sign sheeting, road-marking retroreflection, pedestrian/countdown emitter SPDs, and measured traffic-signal/headlamp capture still remain incomplete in this phase

## Local Source Root

- the full local USGS mirror is expected at `usgs_splib07/` by default or `USGS_SPLIB07_ROOT` if overridden
- the full mirror is intentionally ignored by git
- only the selected subset frozen into `raw/sources/usgs_splib07_selected/` is tracked

## Project Management Docs

- [docs/README.md](docs/README.md): management-doc index and update rules
- [docs/roadmap.md](docs/roadmap.md): phase-level delivery plan
- [docs/task-backlog.md](docs/task-backlog.md): live backlog and task status
- [docs/git-workflow.md](docs/git-workflow.md): local-first git workflow and tracked-artifact policy
- [docs/created-assets.md](docs/created-assets.md): explanation of what the generated asset pack contains
- [docs/file-formats.md](docs/file-formats.md): explanation of `.npz`, `.json`, `USD`, and related file types
- [docs/usgs-ingest.md](docs/usgs-ingest.md): selected USGS subset ingest and binding rules
- [docs/camera-profile.md](docs/camera-profile.md): generic camera-profile contract and current limitations

## Known Measurement Backlog

The generated reports explicitly track these gaps as `backlog_measured_required`:

- automotive RGB/NIR sensor SRF
- measured traffic-signal/headlamp SPD
- wet-road spectral BRDF
- retroreflective sheeting BRDF
