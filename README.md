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
7. validate manifests, spectral coverage, and USD parsing

## Important Defaults

- Coordinate system: right-handed, `Y-up`, meters
- Master spectral grid: `350-1700 nm`, `1 nm`
- Runtime derived grid: `400-1100 nm`, `5 nm`
- Sensor branch: `RGB+NIR` silicon camera
- scenarios now bind to `canonical/camera/camera_reference_rgb_nir_v3.camera_profile.json`
- `camera_reference_rgb_nir_v1` is retained as the earlier vendor-derived baseline for comparison
- `camera_reference_rgb_nir_v2` is retained as the pre-`v3` vendor-derived comparison baseline
- `camera_reference_rgb_nir_v3` is the active vendor-derived public-data baseline built from `MT9M034` RGB donors and a public Balluff `IMX900` mono envelope
- the current `P3` catalog-expansion baseline now adds standalone guardrail, bollard, delineator, cone, barrier, and barricade assets under `road_furniture`
- the second `P3` expansion batch now adds directional arrows, an edge line, a chevron/gore marking, and a worn lane variant under `road_marking`
- the third `P3` expansion batch now adds signal backplates, a mast hanger, and a controller cabinet so traffic-light scenes can place support context explicitly
- the fourth `P3` expansion batch now adds standalone sign backs and mounting brackets so sign scenes can place assembly depth explicitly instead of embedding all hardware into the sign meshes
- the fifth `P3` expansion batch now adds patched, distressed, and transition road-surface panels so validation scenes are not limited to the original clean dry/wet baseline
- selected USGS v7 dry-material baselines are used for asphalt, concrete, and galvanized metal
- wet asphalt is currently a measured-derived material built from the measured dry asphalt baseline plus the tracked wet modifier
- vehicle and protected-turn traffic-signal emissive profiles now use vendor-derived public LED fits
- `urban_night` now uses public `LED-B4` headlamp and `LED-B3` streetlight priors when measured emitter data is absent
- camera profiles now support either a shared optics curve or per-channel optics/filter curves
- optional measured automotive camera SRF intake is supported from `automotive_sensor_srf_input/` or `AUTOMOTIVE_SENSOR_SRF_ROOT`, but the current baseline does not include a frozen measured source
- optional measured traffic-signal/headlamp SPD intake is supported from `traffic_signal_headlamp_spd_input/` or `TRAFFIC_SIGNAL_HEADLAMP_SPD_ROOT`, but the current baseline does not include a frozen measured source
- optional measured retroreflective sheeting input is supported from `retroreflective_sheeting_brdf_input/` or `RETROREFLECTIVE_SHEETING_BRDF_ROOT`, but the current baseline does not include a frozen measured source
- optional measured wet-road input is supported from `wet_road_spectral_brdf_input/` or `WET_ROAD_SPECTRAL_BRDF_ROOT`, but the current baseline does not include a frozen measured source
- sign sheeting, road-marking retroreflection, pedestrian/countdown emitter SPDs, and measured traffic-signal/headlamp capture still remain incomplete in this phase

## Local Source Root

- the full local USGS mirror is expected at `usgs_splib07/` by default or `USGS_SPLIB07_ROOT` if overridden
- the full mirror is intentionally ignored by git
- only the selected subset frozen into `raw/sources/usgs_splib07_selected/` is tracked
- optional measured automotive SRF input may be placed in `automotive_sensor_srf_input/` by default or `AUTOMOTIVE_SENSOR_SRF_ROOT` if overridden
- the optional measured automotive SRF input root is intentionally ignored by git
- optional measured traffic-signal/headlamp SPD input may be placed in `traffic_signal_headlamp_spd_input/` by default or `TRAFFIC_SIGNAL_HEADLAMP_SPD_ROOT` if overridden
- the optional measured traffic-signal/headlamp SPD input root is intentionally ignored by git
- optional measured retroreflective sheeting input may be placed in `retroreflective_sheeting_brdf_input/` by default or `RETROREFLECTIVE_SHEETING_BRDF_ROOT` if overridden
- the optional measured retroreflective sheeting input root is intentionally ignored by git
- optional measured wet-road input may be placed in `wet_road_spectral_brdf_input/` by default or `WET_ROAD_SPECTRAL_BRDF_ROOT` if overridden
- the optional measured wet-road input root is intentionally ignored by git

## Project Management Docs

- [docs/README.md](docs/README.md): management-doc index and update rules
- [docs/roadmap.md](docs/roadmap.md): phase-level delivery plan
- [docs/task-backlog.md](docs/task-backlog.md): live backlog and task status
- [docs/catalog-gap-review.md](docs/catalog-gap-review.md): current family-by-family coverage review and next expansion priorities
- [docs/git-workflow.md](docs/git-workflow.md): local-first git workflow and tracked-artifact policy
- [docs/created-assets.md](docs/created-assets.md): explanation of what the generated asset pack contains
- [docs/file-formats.md](docs/file-formats.md): explanation of `.npz`, `.json`, `USD`, and related file types
- [docs/pbrt-tutorial.md](docs/pbrt-tutorial.md): tutorial for using the generated assets as inputs to a `PBRT` rendering workflow
- [docs/usgs-ingest.md](docs/usgs-ingest.md): selected USGS subset ingest and binding rules
- [docs/camera-profile.md](docs/camera-profile.md): generic camera-profile contract and current limitations
- [docs/public-data-upgrade.md](docs/public-data-upgrade.md): internet-only public-data upgrade scope and limits
- [docs/automotive-srf-intake.md](docs/automotive-srf-intake.md): optional measured automotive camera-SRF intake path and input format
- [docs/emitter-spd-intake.md](docs/emitter-spd-intake.md): optional measured traffic-signal/headlamp SPD intake path and input format
- [docs/retroreflective-brdf-intake.md](docs/retroreflective-brdf-intake.md): optional measured retroreflective-sheething input path and the current shared-gain activation rules
- [docs/wet-road-brdf-intake.md](docs/wet-road-brdf-intake.md): optional measured wet-road input path and the current simplified wet-material activation rules

## Known Measurement Backlog

The generated reports explicitly track these gaps as `backlog_measured_required`:

- automotive RGB/NIR sensor SRF
- measured traffic-signal/headlamp SPD
- wet-road spectral BRDF
- retroreflective sheeting BRDF
