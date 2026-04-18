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

- `372` assets
- `27` spectral materials
- `31` emissive profiles
- `3` camera profiles
- `4` scenario profiles
- `4` validation scenes

Additional baseline facts:

- `376` GLB files currently validate with `0` errors and `0` warnings in [../validation/reports/gltf_validation.json](../validation/reports/gltf_validation.json)
- release gates currently pass for the generated baseline
- raw-source ledger currently tracks `37` source entries
- material quality summary currently reports `3` `measured_standard`, `1` `measured_derivative`, `23` `project_proxy`, and `0` `vendor_derived` materials
- emissive-profile quality summary currently reports `18` `vendor_derived` and `13` `project_proxy` profiles
- camera-profile quality summary currently reports `3` `vendor_derived` profiles, with `camera_reference_rgb_nir_v3` active in all scenarios
- `urban_night` currently uses public `LED-B4` and `LED-B3` priors for headlamp/streetlight contribution when measured emitter data is absent
- the first fifty-six `P3` coverage-expansion batches raised `traffic_sign` from `18` to `90` standalone assets, `road_furniture` from `4` to `102`, `road_marking` from `4` to `69`, `road_surface` from `4` to `57`, and `traffic_light` from `5` to `54`
- traffic-light scenes now place standalone support-context assets including backplates, a mast hanger, side-mount hardware, cabinet variants, a junction box, beacon/warning heads, and lane-control or rail-specific heads
- sign-focused scenes now place standalone sign backs and mounting brackets for representative sign families instead of implying that assembly depth only through the sign meshes
- sign-focused scenes now also exercise weathered stop, speed-limit, and pedestrian-crossing variants plus English text-bearing one-way and detour panels instead of limiting the sign family to the original symbol-only starter set
- sign-focused scenes now also exercise priority-road, roundabout, stop-ahead, detour-right, and heavier-weathered yield, no-entry, and construction variants instead of limiting deeper sign coverage to the earlier starter weathering pass
- sign-focused scenes now also exercise hospital, parking, hotel, airport, truck-route, bypass, and centre wayfinding panels instead of limiting route/service depth to the earlier starter information set
- sign-focused scenes now also exercise US-route, interstate, and E-route shields plus stacked airport/centre, hotel/park, and truck/bypass guide signs instead of limiting sign-route depth to flat single-destination wayfinding panels
- sign-focused scenes now also exercise self-contained overhead airport/centre, park-and-ride, and truck-bypass guide assemblies plus California, UK motorway, and French autoroute shield follow-up variants instead of limiting sign-route depth to roadside shields and stacked ground-mounted guide panels
- sign-focused scenes now also exercise bus-station service panels, airport/parking stacked guides, hospital/parking overhead assemblies, and Interstate-405, E20, and California-82 shield follow-up variants instead of limiting the latest sign-depth pass to the earlier overhead-destination and first shield-follow-up batch
- sign-focused scenes now also exercise `CENTRO`, `AEROPORTO`, and `METRO` service panels, a larger `CENTRO`/`HOTEL` destination stack, deeper US-66, California-17, and A9 shield variants, plus a larger overhead `AEROPORTO`/`CENTRO` split assembly instead of limiting sign follow-up depth to the earlier bus-station, airport/parking, and first shield-expansion batches
- sign-focused scenes now also exercise `CENTRUM` and `PORTO` service panels, a `METRO`/`PORT` destination stack, deeper US-50, Interstate-80, California-280, E75, and M1 shield variants, plus larger overhead `CENTRUM`/`PORT` and `METRO`/`PARK` guide assemblies instead of limiting the newest sign-depth pass to the earlier `CENTRO`/`AEROPORTO`/`METRO` and first overhead-follow-up batch
- sign-focused scenes now also exercise `FERRY`, `STAZIONE`, and `GARE` service panels, new station/ferry, terminal/metro, and bus/ferry transfer stacks, plus larger overhead `STAZIONE`/`PORTO` and `FERRY`/`TERMINAL` guide assemblies instead of limiting the newest sign-depth pass to the earlier multilingual service and second overhead-guide follow-up batches
- sign-focused scenes now also exercise tram/bus-platform wayfinding panels, taxi/loading-zone service panels, tram/taxi and platform/refuge destination stacks, plus an overhead platform/refuge guide assembly instead of limiting the newest sign-depth pass to the earlier transfer-wayfinding, multilingual-service, and overhead-guide follow-up batches
- the current validation scenes now also exercise patched, distressed, and transition road-surface panels instead of only the original clean urban baseline
- the current validation scenes now also exercise gravel-shoulder, asphalt-to-gravel transition, construction-plate, pothole-distress, and eroded-shoulder surface variants instead of limiting roadway breadth to urban repair panels alone
- the current validation scenes now also exercise crowned rural-lane, dirt-track, bridge-joint, and lane-drop surface panels instead of limiting road-surface depth to the earlier urban and gravel-shoulder follow-up batches
- the current validation scenes now also exercise milled-overlay, trench-cut, bridge-approach, barrier-taper, and curb-bulbout surface panels instead of limiting later roadway depth to the earlier repair, rural, and bridge-joint batches
- the current validation scenes now also exercise ramp bridge-tie, ramp-gore, median-refuge-nose, and temporary crossover/barrier-chicane panels instead of limiting later roadway depth to the earlier repair, bridge-approach, and curb/barrier transition batches
- the current validation scenes now also exercise lane-control and rail-crossing signal heads instead of limiting the traffic-light family to vehicle, pedestrian, beacon, and generic warning-flasher variants
- the current validation scenes now also exercise transit-priority and directional-arrow signal heads instead of limiting traffic-light specialization to the earlier lane-control and rail-crossing batches
- the current validation scenes now also exercise bicycle, pedestrian-bicycle hybrid, and tram-priority heads instead of limiting traffic-light specialization to vehicle, pedestrian, lane-control, and transit-only variants
- the current validation scenes now also exercise pedestrian-wait, school-warning, and lunar-preemption heads plus rail-gate mast/arm/bell/controller context instead of limiting the traffic-light family to signal heads without broader rail-gate or edge-case controller detail
- the current validation scenes now also exercise bus-priority, U-turn-arrow, horizontal school-warning, and dual-lunar preemption heads plus cantilever frame/dropper support detail instead of limiting the latest traffic-light depth to earlier specialty heads mounted only with side brackets, backplates, or starter mast-arm context
- the current validation scenes now also exercise compact lane-control, single-amber school-warning, compact bus/tram-priority, and vertical dual-lunar preemption heads plus a curved cantilever mast and triple-dropper subtype instead of limiting the latest traffic-light depth to the earlier full-size specialty-control and single cantilever-frame subtype pass
- the current validation scenes now also exercise vertical amber/red warning flashers, a quad-lunar preemption box head, and localized diamond-style bus/tram heads plus single and quad cantilever droppers instead of limiting the latest traffic-light depth to earlier compact specialty-control and dual-lunar edge-case passes
- the current validation scenes now also exercise compact bicycle and pedestrian-bicycle heads, a transit-priority diamond head, a dual-amber warning box, and a dual-lunar preemption box plus cantilever backspan, diagonal-brace, and mount-plate follow-up hardware instead of limiting the latest traffic-light depth to earlier compact bus/tram-control, quad-lunar, and dropper-only cantilever follow-up passes
- the current validation scenes now also exercise bus-only lane-control, bar-style transit-priority, diagonal dual-lunar preemption, compact vertical amber-warning, and compact bicycle lane-control heads plus cantilever arm-junction-box and end-cap detail instead of limiting the latest traffic-light depth to earlier compact multimodal-control, warning-box, and backspan/brace-only cantilever follow-up passes
- the current validation scenes now also exercise bicycle-only lane-control, dual-horizontal pedestrian-wait, transit-priority T-face, and bus/tram bar-style control heads plus cantilever service-conduit and splice-box detail instead of limiting the latest traffic-light depth to earlier bus-only, single-wait, and end-cap-only cantilever follow-up passes
- the current validation scenes now also exercise secondary road-marking variants including worn crossings/stops, yellow centerline families, `ONLY` and `STOP` word legends, and white/yellow/bi-color raised-marker strips
- the current validation scenes now also exercise bus/bike legends, hatched median/island panels, and right-turn or straight-right arrow variants instead of limiting road-marking depth to centerlines, merge arrows, and basic word legends alone
- the current validation scenes now also exercise utility poles, smaller cabinet/junction variants, service disconnects, meter pedestals, battery-backup cabinets, pull boxes, pad-mount transformers, and explicit sign/signal attachment hardware
- the current validation scenes now also exercise a transit-stop shelter, a stop totem, a bench, a handhole cluster, and protective service bollards instead of limiting roadside context to signal-control hardware and sign/signal supports alone
- the current validation scenes now also exercise bus-bay curb and island modules, passenger-information and real-time-arrival hardware, plus loading-zone sign/kiosk detail instead of limiting curbside context to shelter-only transit furniture and generic curbside boxes
- the current validation scenes now also exercise queue rails, shelter ad panels, straight and corner curb-ramp modules, and sign/signal band-clamp hardware instead of limiting curbside/attachment depth to shelter-only transit furniture and earlier bracket-only mounting context
- the current validation scenes now also exercise shelter trash receptacles, shelter route-map cases, lean rails, curb-separator flexpost or kerb modules, and signal hanger-clamp pairs instead of limiting the latest roadside follow-up to earlier shelter-panel, curb-ramp, and clamp-only support detail
- the current validation scenes now also exercise cantilever anchor-cage and footing-collar detail, rail power-disconnect and relay-case ancillaries, and validator-pedestal or timetable-blade transit microsupport instead of limiting the latest roadside follow-up to frame/dropper-only cantilever detail and earlier shelter/totem curbside context
- the current validation scenes now also exercise cantilever service ladders/platforms, a rail bungalow and battery box, curbside queue-stanchion or boarding-guardrail support detail, and newer `WAIT`/`QUEUE`, `VALET`/`EV ONLY`, and separator-chevron marking follow-up instead of limiting the latest curbside depth to queue-rail-only support context or earlier `NO PARK`/`PERMIT` and separator-arrow-only markings
- the current validation scenes now also exercise cantilever cable-tray and maintenance-hoist hardware, rail predictor/service-post ancillaries, and bus-stop help-point/request-pole microsupport instead of limiting the latest roadside follow-up to ladders/platforms, bungalow/battery-box detail, and validator/timetable-only curbside microsupport
- the current validation scenes now also exercise cantilever arm-junction-box and end-cap detail so the newest signal-support follow-up no longer stops at cable-tray, maintenance-hoist, or backspan/brace-only cantilever hardware
- the current validation scenes now also exercise slim/aux cantilever controller boxes, pole riser/service-loop guards, and bus-stop notice/perch follow-up pieces so roadside-support depth no longer stops at arm-junction-box/end-cap detail, cabinet-tail hardware, and help-point/request-pole-only transit microsupport
- the current validation scenes now also exercise cantilever service-conduit and splice-box detail so the newest signal-support follow-up no longer stops at controller housings, pole-tail guards, and notice/perch transit accessories alone
- the current validation scenes now also exercise shelter-power pedestals and inverter boxes, ticket-machine and platform-handrail stop utilities, plus signal-base handhole/conduit detail so roadside-support depth no longer stops at notice/perch accessories, queue support, and pole-tail-only signal-base context
- the current validation scenes now also exercise `TRAM` and `TRAM STOP` platform legends, `DELIVERY` and `NO STOP` curbside-control boxes, plus left/right `KEEP` separator panels so road-marking depth no longer stops at bus/bike legends, earlier curbside reservations, and arrow/chevron-only separator control
- the current validation scenes now also exercise boxed `BUS ONLY`, `BUS STOP`, `BIKE`, and `LOAD` legends plus red/green curbside lane panels, curb-color segments, loading zigzag delimiters, and red/green conflict-zone surfacing instead of limiting road-marking depth to unboxed word legends and monochrome striping
- the current validation scenes now also exercise turn-pocket `ONLY` stencils, `SCHOOL` legends, `SCHOOL BUS` queue boxes, and curbside left/right arrows instead of limiting the latest curbside and school-zone marking depth to boxed legends and conflict-zone surfacing alone
- the current validation scenes now also exercise `SLOW` and `XING` school-zone legends, white/green separator-buffer panels, and pick-up or taxi curbside boxes instead of limiting the latest localized marking pass to earlier school-bus, curbside-arrow, and generic colored-panel coverage
- the current validation scenes now also exercise red `NO PARK` and green `PERMIT` curbside-reservation boxes, `DROP OFF` and `KISS RIDE` school-dropoff stencils, and left/right separator-arrow panels instead of limiting the latest localized marking pass to earlier school-zone legends, queue boxes, curbside arrows, and generic separator buffers
- the current validation scenes now also exercise roundabout truck-apron, outer-ring-edge, and bypass-slip-lane panels, retaining-wall cut, shoulder-shelf, and abutment transitions, plus deeper shoefly, staging-pad, laydown-bay, and temporary-access work-zone surfaces instead of limiting later roadway depth to ramp-gore, median-nose, and earlier crossover/chicane composites alone
- the current validation scenes now also exercise bus-bay pullout, service-lane apron, curbside drop-off, alley-access, slip-lane pedestrian-island, and mountable-apron corner panels instead of limiting curbside roadway breadth to earlier gutter, curb-bulbout, and roundabout/bypass composites alone
- the current validation scenes now also exercise floating bus-stop islands, transfer platforms, transit-platform bulbouts and median islands, curbside loading/enforcement bays, separator-island taper/refuge/boarding-refuge/bus-bay-taper panels, and left-hand contraflow or detour-staging work-zone surfaces instead of limiting later roadway breadth to earlier curbside-access, mountable-apron, and generic staging-only composites

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
