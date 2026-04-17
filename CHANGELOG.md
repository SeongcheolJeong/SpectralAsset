# Changelog

## Unreleased

### Added

- project-management doc set under `docs/`
- local-first git workflow definition
- phase roadmap and task backlog for long-running work
- explanation docs for generated assets and file formats
- `PBRT` tutorial for converting generated assets, spectra, and scenarios into a practical render workflow
- measured automotive camera-SRF intake documentation and local input format
- measured traffic-signal/headlamp SPD intake documentation and local input format
- measured retroreflective intake documentation and local input format
- measured wet-road intake documentation and local input format
- source-policy documentation for source classifications and blocked-source handling
- milestone validation checklist and first release checklist
- measured-replacement priority doc for the four remaining proxy-to-measured backlog items
- catalog gap review for family-by-family asset coverage depth
- selected USGS v7 subset ingest documentation and generic camera-profile documentation
- internet-only public-data upgrade documentation
- first `P3` road-furniture expansion batch with standalone guardrail, bollard, delineator, traffic-cone, water-barrier, and barricade assets
- second `P3` road-marking expansion batch with directional arrows, an edge line, a chevron/gore marking, and a worn lane variant

### Changed

- repository governance now treats generated assets, exports, raw-source records, and validation outputs as tracked artifacts
- blocked `403` source pages are explicitly documented with impact and fallback handling instead of remaining only as ledger failures
- rebuild tooling now preserves prior tracked timestamps by default to reduce non-semantic diff churn
- build tooling now reuses frozen raw sources by default and requires explicit opt-in for source refreshes
- backlog governance now ranks measurement backlog items and documents that the current catalog is count-complete but not depth-complete
- build tooling now freezes a selected local USGS v7 subset into tracked `raw/` inputs instead of relying on the full local mirror
- scenarios now reference a generic `RGB+NIR` camera profile
- dry asphalt, concrete, and galvanized metal are now measured USGS-derived baselines, and wet asphalt is a measured-derived material
- vehicle and protected-turn traffic-signal emissive profiles now use vendor-derived public LED fits from tracked ams-OSRAM datasheets
- urban night illuminant generation now reuses the same vendor-derived signal color fits instead of the older hard-coded proxy peaks
- camera generation now retains `camera_reference_rgb_nir_v1` and `camera_reference_rgb_nir_v2` as vendor-derived comparison baselines
- scenarios now reference `camera_reference_rgb_nir_v3`, while `camera_reference_rgb_nir_v2` remains available as the pre-`v3` comparison baseline
- the ON Semiconductor `MT9M034` donor PDF is now frozen from a local copy into tracked `raw/` instead of remaining only as a `fetch_failed` source-ledger entry
- camera-profile generation now supports an optional frozen measured automotive SRF source with a measured-system activation gate, while keeping the strongest available vendor-derived profile active when no measured source is present
- emissive-profile generation now supports an optional frozen measured traffic-signal/headlamp SPD source with a measured activation gate, while keeping vendor-derived signal SPDs active when no measured source is present
- measured emitter intake now accepts headlamp-only or streetlight-only datasets for `urban_night` augmentation without requiring measured traffic-signal red/yellow/green curves
- material generation now supports an optional frozen measured retroreflective source with a shared-gain activation gate, while keeping the proxy retroreflective modifier active when no measured source is present
- material generation now supports an optional frozen measured wet-road source with a simplified wet-material activation gate, while keeping the measured-derived wet asphalt fallback active when no measured source is present
- camera generation now emits `camera_reference_rgb_nir_v3` and promotes it to the active generic camera when no measured automotive SRF source is present
- urban night illuminant generation now uses public `LED-B4` and `LED-B3` priors for headlamp/streetlight contribution when measured emitter data is absent
- raw-source freezing now tracks public EMVA, Balluff, CIE, and FHWA references for the internet-only public-data upgrade phase
- existing validation scenes now place selected road-furniture expansion assets so the new coverage is exercised in generated scene exports
- existing validation scenes now place selected directional and worn road-marking assets so the expanded marking catalog is exercised in scene exports
- backlog focus now moves from blocked measurement work to `P3` coverage expansion, with traffic-light support geometry now next in queue

### Validation

- validation summary now reports `46` assets, including `10` `road_furniture` assets and `9` `road_marking` assets after the first two `P3` expansion batches
- validation summary now includes `3` camera profiles and zero camera-profile validation errors
- material quality summary now reports `3` `measured_standard`, `1` `measured_derivative`, `16` `project_proxy`, and `0` `vendor_derived` materials
- emissive profile quality summary now distinguishes vendor-derived vehicle/protected-turn profiles from remaining proxy pedestrian/countdown profiles
- validation summary now distinguishes the active camera profile, per-scenario camera bindings, donor reference metadata for camera profiles, and public-data activation for `urban_night`

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
