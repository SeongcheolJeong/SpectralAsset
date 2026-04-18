# Project Overview

## Project Goal and Scope

This repository builds an engine-agnostic asset pack for autonomous-driving camera simulation. The current scope covers:

- traffic signs, traffic lights, road surfaces, road markings, and roadside furniture
- spectral materials, emissive profiles, and generic camera profiles for camera-oriented simulation
- USD authoring assets, GLB runtime exports, scenario profiles, and validation scenes
- reproducible generation from scripts and a frozen raw-source ledger

This repository is not yet targeting release automation or measured replacement of all proxy spectra.

## Current Repository State

- Local git bootstrap is in place with `main` as the default branch.
- GitHub remote `origin` is configured and `main` tracks `origin/main`.
- Generated assets, exports, raw-source artifacts, and validation reports are intentionally tracked in version control.
- `node_modules/` is dependency-only and must remain untracked.

## Current Generated Baseline Summary

Current truth from [../validation/reports/validation_summary.json](../validation/reports/validation_summary.json):

- `193` assets
- `27` spectral materials
- `19` emissive profiles
- `3` camera profiles
- `4` scenario profiles
- `4` validation scenes

Additional baseline facts:

- `197` GLB files currently validate with `0` errors and `0` warnings in [../validation/reports/gltf_validation.json](../validation/reports/gltf_validation.json)
- release gates currently pass for the generated baseline
- raw-source ledger currently tracks `37` source entries
- material quality summary currently reports `3` `measured_standard`, `1` `measured_derivative`, `23` `project_proxy`, and `0` `vendor_derived` materials
- emissive-profile quality summary currently reports `13` `vendor_derived` and `6` `project_proxy` profiles
- camera-profile quality summary currently reports `3` `vendor_derived` profiles, with `camera_reference_rgb_nir_v3` active in all scenarios
- `urban_night` currently uses public `LED-B4` and `LED-B3` priors for headlamp/streetlight contribution when measured emitter data is absent
- the first twenty-nine `P3` coverage-expansion batches raised `traffic_sign` from `18` to `50` standalone assets, `road_furniture` from `4` to `53`, `road_marking` from `4` to `38`, `road_surface` from `4` to `28`, and `traffic_light` from `5` to `24`
- traffic-light scenes now place standalone support-context assets including backplates, a mast hanger, side-mount hardware, cabinet variants, a junction box, beacon/warning heads, and lane-control or rail-specific heads
- sign-focused scenes now place standalone sign backs and mounting brackets for representative sign families instead of implying that assembly depth only through the sign meshes
- sign-focused scenes now also exercise weathered stop, speed-limit, and pedestrian-crossing variants plus English text-bearing one-way and detour panels instead of limiting the sign family to the original symbol-only starter set
- sign-focused scenes now also exercise priority-road, roundabout, stop-ahead, detour-right, and heavier-weathered yield, no-entry, and construction variants instead of limiting deeper sign coverage to the earlier starter weathering pass
- sign-focused scenes now also exercise hospital, parking, hotel, airport, truck-route, bypass, and centre wayfinding panels instead of limiting route/service depth to the earlier starter information set
- sign-focused scenes now also exercise US-route, interstate, and E-route shields plus stacked airport/centre, hotel/park, and truck/bypass guide signs instead of limiting sign-route depth to flat single-destination wayfinding panels
- sign-focused scenes now also exercise self-contained overhead airport/centre, park-and-ride, and truck-bypass guide assemblies plus California, UK motorway, and French autoroute shield follow-up variants instead of limiting sign-route depth to roadside shields and stacked ground-mounted guide panels
- the current validation scenes now also exercise patched, distressed, and transition road-surface panels instead of only the original clean urban baseline
- the current validation scenes now also exercise gravel-shoulder, asphalt-to-gravel transition, construction-plate, pothole-distress, and eroded-shoulder surface variants instead of limiting roadway breadth to urban repair panels alone
- the current validation scenes now also exercise crowned rural-lane, dirt-track, bridge-joint, and lane-drop surface panels instead of limiting road-surface depth to the earlier urban and gravel-shoulder follow-up batches
- the current validation scenes now also exercise milled-overlay, trench-cut, bridge-approach, barrier-taper, and curb-bulbout surface panels instead of limiting later roadway depth to the earlier repair, rural, and bridge-joint batches
- the current validation scenes now also exercise ramp bridge-tie, ramp-gore, median-refuge-nose, and temporary crossover/barrier-chicane panels instead of limiting later roadway depth to the earlier repair, bridge-approach, and curb/barrier transition batches
- the current validation scenes now also exercise lane-control and rail-crossing signal heads instead of limiting the traffic-light family to vehicle, pedestrian, beacon, and generic warning-flasher variants
- the current validation scenes now also exercise transit-priority and directional-arrow signal heads instead of limiting traffic-light specialization to the earlier lane-control and rail-crossing batches
- the current validation scenes now also exercise bicycle, pedestrian-bicycle hybrid, and tram-priority heads instead of limiting traffic-light specialization to vehicle, pedestrian, lane-control, and transit-only variants
- the current validation scenes now also exercise pedestrian-wait, school-warning, and lunar-preemption heads plus rail-gate mast/arm/bell/controller context instead of limiting the traffic-light family to signal heads without broader rail-gate or edge-case controller detail
- the current validation scenes now also exercise secondary road-marking variants including worn crossings/stops, yellow centerline families, `ONLY` and `STOP` word legends, and white/yellow/bi-color raised-marker strips
- the current validation scenes now also exercise bus/bike legends, hatched median/island panels, and right-turn or straight-right arrow variants instead of limiting road-marking depth to centerlines, merge arrows, and basic word legends alone
- the current validation scenes now also exercise utility poles, smaller cabinet/junction variants, service disconnects, meter pedestals, battery-backup cabinets, pull boxes, pad-mount transformers, and explicit sign/signal attachment hardware
- the current validation scenes now also exercise a transit-stop shelter, a stop totem, a bench, a handhole cluster, and protective service bollards instead of limiting roadside context to signal-control hardware and sign/signal supports alone
- the current validation scenes now also exercise bus-bay curb and island modules, passenger-information and real-time-arrival hardware, plus loading-zone sign/kiosk detail instead of limiting curbside context to shelter-only transit furniture and generic curbside boxes
- the current validation scenes now also exercise queue rails, shelter ad panels, straight and corner curb-ramp modules, and sign/signal band-clamp hardware instead of limiting curbside/attachment depth to shelter-only transit furniture and earlier bracket-only mounting context
- the current validation scenes now also exercise boxed `BUS ONLY`, `BUS STOP`, `BIKE`, and `LOAD` legends plus red/green curbside lane panels, curb-color segments, loading zigzag delimiters, and red/green conflict-zone surfacing instead of limiting road-marking depth to unboxed word legends and monochrome striping

## Repository Structure

- `canonical/`: source-of-truth generated assets, materials, spectra, camera profiles, manifests, templates, scenarios, atmospheres, and scenes
- `exports/`: generated runtime exports in `usd/` and `gltf/`
- `raw/`: source ledger plus frozen raw inputs or fetch records
- `schemas/`: JSON schema definitions for manifest/profile types
- `scripts/`: asset-pack generator and glTF validator wrapper
- `validation/`: generated reports summarizing coverage and checks
- `docs/`: management docs for roadmap, backlog, asset policy, source handling, and git workflow

## Known Constraints

- Several external reference pages still fail automated fetch with `403` and only have failure records in the source ledger.
- The full local `usgs_splib07/` mirror is intentionally not tracked; only the selected frozen subset in `raw/sources/usgs_splib07_selected/` is part of the repository baseline.
- Many spectral assets are still proxy curves, even though dry asphalt, concrete, and galvanized metal now use measured USGS-derived baselines.
- Vehicle and protected-turn traffic-signal SPDs still use vendor-derived public fits; pedestrian/countdown emitters remain proxy.
- `camera_reference_rgb_nir_v3` is now the active generic reference camera, but it remains a public-data vendor-derived profile rather than a measured automotive SRF.
- the official `onsemi_mt9m034_pdf` URL still blocks automated GET with `403`, so the repository freezes a local copy of that PDF into tracked `raw/`
- the generator now freezes public EMVA, Balluff, CIE, and FHWA references into tracked `raw/` when available
- the generator supports optional local measured intake roots for automotive SRF, traffic-signal/headlamp SPD, retroreflective sheeting, and wet-road data, but no frozen measured source is currently present for any of those tracks
- the current retroreflective material contract still uses a shared spectral gain modifier, not a full angle-aware BRDF
- the current wet-road material contract still uses a simplified wet reflectance plus overlay model, not a full angle-aware wet-road BRDF
- generated files still include `generated_at` metadata, but the generator and validator preserve the previous value by default so clean rebuilds do not churn timestamps unless explicitly overridden
- remote hosting is active through GitHub, but release automation and measured-data automation are still manual

## Known Measurement Gaps

Current backlog items from [../validation/reports/measurement_backlog.json](../validation/reports/measurement_backlog.json):

- automotive RGB/NIR sensor spectral response
- measured traffic signal and headlamp SPD replacement data
- wet-road spectral BRDF
- retroreflective sheeting BRDF

The automotive sensor backlog item remains open even though `camera_reference_rgb_nir_v3` is now active; the repository still lacks measured automotive SRF data.
The traffic-signal/headlamp backlog item remains open even though vehicle and protected-turn signal profiles use vendor-derived public LED fits and `urban_night` now uses public headlamp/streetlight priors; the repository still lacks measured capture data.
The retroreflective backlog item also remains open even though measured-intake support exists for the current shared gain modifier; the repository still lacks a frozen measured source and does not yet support a full angle-aware BRDF contract.
The wet-road backlog item also remains open even though measured-intake support exists for the current simplified wet-material path; the repository still lacks a frozen measured source and does not yet support a full angle-aware wet-road BRDF contract.

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
Public-data upgrade scope and limits are documented in [public-data-upgrade.md](public-data-upgrade.md).
