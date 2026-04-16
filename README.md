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
3. normalize official D65 and ASTM G173 inputs
4. generate proxy spectral materials and emissive SPDs
5. emit SVG sign templates, USD assets, GLB exports, manifests, scenario profiles, scenes, and reports
6. validate manifests, spectral coverage, and USD parsing

## Important Defaults

- Coordinate system: right-handed, `Y-up`, meters
- Master spectral grid: `350-1700 nm`, `1 nm`
- Runtime derived grid: `400-1100 nm`, `5 nm`
- Sensor branch: `RGB+NIR` silicon camera
- v1 uses measured standards for daylight inputs and project-generated proxy spectra for several materials that still require measured replacement

## Project Management Docs

- [docs/README.md](docs/README.md): management-doc index and update rules
- [docs/roadmap.md](docs/roadmap.md): phase-level delivery plan
- [docs/task-backlog.md](docs/task-backlog.md): live backlog and task status
- [docs/git-workflow.md](docs/git-workflow.md): local-first git workflow and tracked-artifact policy

## Known Measurement Backlog

The generated reports explicitly track these gaps as `backlog_measured_required`:

- automotive RGB/NIR sensor SRF
- real traffic-signal/headlamp SPD
- wet-road spectral BRDF
- retroreflective sheeting BRDF
