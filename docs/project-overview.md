# Project Overview

## Project Goal and Scope

This repository builds an engine-agnostic asset pack for autonomous-driving camera simulation. The current scope covers:

- traffic signs, traffic lights, road surfaces, road markings, and roadside furniture
- spectral materials, emissive profiles, and a generic camera profile for camera-oriented simulation
- USD authoring assets, GLB runtime exports, scenario profiles, and validation scenes
- reproducible generation from scripts and a frozen raw-source ledger

This repository is not yet targeting remote hosting, release automation, or measured replacement of all proxy spectra.

## Current Repository State

- Local git bootstrap is now in place with `main` as the default branch.
- No remote repository is configured yet.
- Generated assets, exports, raw-source artifacts, and validation reports are intentionally tracked in version control.
- `node_modules/` is dependency-only and must remain untracked.

## Current Generated Baseline Summary

Current truth from [../validation/reports/validation_summary.json](../validation/reports/validation_summary.json):

- `35` assets
- `20` spectral materials
- `4` emissive profiles
- `1` camera profile
- `4` scenario profiles
- `4` validation scenes

Additional baseline facts:

- `39` GLB files currently validate with `0` errors and `0` warnings in [../validation/reports/gltf_validation.json](../validation/reports/gltf_validation.json)
- release gates currently pass for the generated baseline
- raw-source ledger currently tracks `28` source entries
- material quality summary currently reports `3` `measured_standard`, `1` `measured_derivative`, `16` `project_proxy`, and `0` `vendor_derived` materials

## Repository Structure

- `canonical/`: source-of-truth generated assets, materials, spectra, camera profiles, manifests, templates, scenarios, atmospheres, and scenes
- `exports/`: generated runtime exports in `usd/` and `gltf/`
- `raw/`: source ledger plus frozen raw inputs or fetch records
- `schemas/`: JSON schema definitions for manifest/profile types
- `scripts/`: asset-pack generator and glTF validator wrapper
- `validation/`: generated reports summarizing coverage and checks
- `docs/`: management docs for roadmap, backlog, asset policy, source handling, and git workflow

## Known Constraints

- Several external reference pages currently fail automated fetch with `403` and only have failure records in the source ledger.
- The full local `usgs_splib07/` mirror is intentionally not tracked; only the selected frozen subset in `raw/sources/usgs_splib07_selected/` is part of the repository baseline.
- Many spectral assets are still proxy curves, even though dry asphalt, concrete, and galvanized metal now use measured USGS-derived baselines.
- Generated files still include `generated_at` metadata, but the generator and validator now preserve the previous value by default so clean rebuilds do not churn timestamps unless explicitly overridden.
- The repository is local-first only; remote collaboration rules are documented but not yet activated.

## Known Measurement Gaps

Current backlog items from [../validation/reports/measurement_backlog.json](../validation/reports/measurement_backlog.json):

- automotive RGB/NIR sensor spectral response
- traffic signal and headlamp SPD replacement data
- wet-road spectral BRDF
- retroreflective sheeting BRDF

Current priority order for these measured replacements is documented in [measurement-priorities.md](measurement-priorities.md).

## Current Validation Status

Current truth from [../validation/reports/validation_summary.json](../validation/reports/validation_summary.json):

- asset validation: pass
- material validation: pass
- emissive profile validation: pass
- camera profile validation: pass
- scenario validation: pass
- USD export validation: pass
- scale validation: pass
- semantic validation: pass
- wet-road proxy validation: pass
- release-gate summary: pass

Current source-fetch failures from [../raw/source_ledger.json](../raw/source_ledger.json):

- `mapillary_sign_help`: `403`
- `mapillary_download_help`: `403`
- `usgs_spectral_library_page`: `403`
- `unece_road_signs_page`: `403`

Fallback handling for these blocked sources is documented in [source-policy.md](source-policy.md).
Milestone validation gates are documented in [validation-checklist.md](validation-checklist.md).
Family-by-family catalog depth gaps are documented in [catalog-gap-review.md](catalog-gap-review.md).
USGS subset ingest rules are documented in [usgs-ingest.md](usgs-ingest.md).
Camera-profile contract details are documented in [camera-profile.md](camera-profile.md).
