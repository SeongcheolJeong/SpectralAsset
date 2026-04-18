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
- the sixth `P3` expansion batch now adds merge, worn crossing/stop, yellow edge, and raised-marker assets so the road-marking catalog is no longer limited to the original arrow-and-lane subset
- the seventh `P3` expansion batch now adds utility poles, smaller signal-support cabinets, junction boxes, and explicit sign/signal attachment hardware so roadside support context is deeper than the original starter set
- the eighth `P3` expansion batch now adds beacon-style and warning-flasher signal heads with explicit state maps so the traffic-light family is broader than the original five-head baseline
- the ninth `P3` expansion batch now adds weathered stop, speed-limit, and pedestrian-crossing signs plus English text-bearing one-way and detour variants so the sign family is no longer limited to symbol-only starter panels
- the tenth `P3` expansion batch now adds yellow centerline families, `ONLY` and `STOP` lane legends, and yellow/bi-color raised-marker variants so the road-marking family is no longer limited to the earlier arrow-and-edge starter set
- the eleventh `P3` expansion batch now adds gravel-shoulder, asphalt-to-gravel transition, construction-plate, pothole-distress, and eroded-shoulder road-surface variants so roadway breadth extends beyond the earlier urban repair/transition set
- the twelfth `P3` expansion batch now adds lane-control and rail-crossing signal heads plus dedicated lane-control and rail-specific emissive profiles so the traffic-light family extends beyond vehicle, pedestrian, beacon, and generic flasher heads
- the thirteenth `P3` expansion batch now adds service-disconnect, meter-pedestal, battery-backup, pull-box, and pad-mount-transformer assets so roadside control-tail detail extends beyond the earlier pole/cabinet/junction starter set
- the fourteenth `P3` expansion batch now adds priority-road, roundabout, stop-ahead, detour-right, and heavy-weathered sign variants plus a stronger heavy-weathering overlay material so the sign family has broader locale and weathering depth
- the fifteenth `P3` expansion batch now adds bus/bike legends, hatched median/island panels, and right-turn or straight-right arrow variants so the road-marking family has broader lane-use and channelization depth
- the sixteenth `P3` expansion batch now adds hospital, parking, hotel, airport, truck-route, bypass, and centre wayfinding panels so the sign family has broader route/service depth
- the seventeenth `P3` expansion batch now adds a crowned rural lane, two dirt-track panels, a bridge expansion-joint panel, and a lane-drop transition panel so the road-surface family extends beyond the earlier urban repair and gravel-shoulder breadth pass
- the eighteenth `P3` expansion batch now adds transit-priority and directional-arrow signal heads so the traffic-light family extends beyond the earlier beacon, lane-control, rail-crossing, and warning-flasher specialization passes
- the nineteenth `P3` expansion batch now adds a bus-stop shelter, stop totem, bench, handhole cluster, and protective service-bollard pair so roadside context reaches curbside transit-stop and utility-service detail
- the twentieth `P3` expansion batch now adds boxed curbside/transit legends and red/green colored lane panels so the road-marking family now covers boxed `BUS ONLY`, `BUS STOP`, `BIKE`, and `LOAD` treatments plus colored transit/bike surfacing
- the twenty-first `P3` expansion batch now adds U.S., interstate, and E-route shields plus stacked destination-guide panels so the sign family now covers route-marker and multi-destination guidance depth beyond the earlier single-destination service/wayfinding pass
- the twenty-second `P3` expansion batch now adds milled-overlay, trench-cut, bridge-approach, barrier-taper, and curb-bulbout road-surface panels so the roadway family now covers heavier construction staging and curb/barrier transition composites beyond the earlier repair and rural-follow-up passes
- the twenty-third `P3` expansion batch now adds bicycle, pedestrian-bicycle hybrid, and tram-priority signal heads so the traffic-light family now covers more locale-specific control variants beyond the earlier lane-control, transit-priority, and directional-arrow passes
- the twenty-fourth `P3` expansion batch now adds bus-bay curb and island modules, passenger-information and real-time-arrival hardware, plus loading-zone sign/kiosk detail so curbside transit/loading scenes no longer stop at shelter-only context
- the twenty-fifth `P3` expansion batch now adds curb-color segments, loading zigzag delimiters, and red/green conflict-zone panels so curbside/loading scenes no longer stop at boxed legends and simple colored lane fills
- the twenty-sixth `P3` expansion batch now adds self-contained overhead destination assemblies plus California, UK motorway, and French autoroute shield follow-up variants so the sign family no longer stops at roadside route shields and stacked ground-mounted guide panels
- the twenty-seventh `P3` expansion batch now adds ramp bridge-tie panels, ramp-gore and median-refuge noses, plus temporary crossover/barrier-chicane work-zone composites so the road-surface family no longer stops at repair, bridge-approach, and curb/barrier transition panels
- the twenty-eighth `P3` expansion batch now adds school-warning, pedestrian-wait, and lunar-preemption heads plus rail-gate mast, arm, bell, and controller-cabinet context so the traffic-light family no longer stops at standalone rail/transit/bicycle specialty heads without broader crossing-gate or edge-case controller detail
- the twenty-ninth `P3` expansion batch now adds queue rails, shelter ad panels, curb-ramp modules, and sign/signal band-clamp hardware so curbside transit and attachment-depth scenes no longer stop at shelter-only furniture and earlier bracket-only mounting context
- the thirtieth `P3` expansion batch now adds turn-pocket `ONLY` stencils, `SCHOOL` legends, `SCHOOL BUS` queue boxes, and curbside left/right arrows so the road-marking family no longer stops at boxed curbside legends, conflict-zone panels, and generic directional arrows
- the thirty-first `P3` expansion batch now adds roundabout truck-apron and splitter-island panels, a retaining-wall cut transition, and deeper shoefly/staging-pad work-zone surfaces so the road-surface family no longer stops at ramp-gore, median-nose, and earlier crossover/chicane composites
- the thirty-second `P3` expansion batch now adds a bus-station service panel, an airport/parking stacked guide, a hospital/parking overhead assembly, and Interstate-405, E20, and California-82 shield follow-up signs so the sign family no longer stops at the earlier overhead-destination and first shield-follow-up pass
- the thirty-third `P3` expansion batch now adds bus-priority, U-turn-arrow, horizontal school-warning, and dual-lunar preemption signal heads plus cantilever frame/dropper support detail so the traffic-light family no longer stops at rail-gate/controller nuance without broader cantilever-crossing and locale-specific specialty follow-up
- the thirty-fourth `P3` expansion batch now adds shelter trash, route-map, and lean-rail accessories plus curb-separator flexpost/kerb modules and signal hanger-clamp pairs so roadside-support depth no longer stops at shelter panels, curb ramps, and broader bracket-only attachment context
- the thirty-fifth `P3` expansion batch now adds `SLOW`/`XING` school-zone legends, white/green separator-buffer panels, and pick-up/taxi curbside boxes so the road-marking family no longer stops at school-bus queues, curbside arrows, and generic boxed curbside legends
- the thirty-sixth `P3` expansion batch now adds roundabout outer-ring and bypass-slip-lane panels, retaining-wall shoulder-shelf and abutment transitions, plus laydown-bay and temporary-access work-zone surfaces so roadway depth no longer stops at the earlier roundabout-apron, retaining-wall cut, and staging-pad follow-up set
- the thirty-seventh `P3` expansion batch now adds `CENTRO`, `AEROPORTO`, and `METRO` service panels, a larger `CENTRO`/`HOTEL` destination stack, deeper `US 66`, `CA 17`, and `A9` shield variants, plus a larger overhead `AEROPORTO`/`CENTRO` split assembly so sign depth no longer stops at the earlier localized service, route-shield, and overhead-guide follow-up set
- the thirty-eighth `P3` expansion batch now adds compact lane-control, compact bus/tram-priority, single-amber school-warning, and vertical dual-lunar preemption heads plus a curved cantilever mast and triple-dropper subtype so traffic-light depth no longer stops at the earlier full-size specialty-control set and single cantilever-frame subtype
- the thirty-ninth `P3` expansion batch now adds cantilever anchor-cage and footing-collar detail, rail power-disconnect and relay-case ancillaries, and validator-pedestal/timetable-blade transit microsupport so roadside-support depth no longer stops at frame/dropper-only cantilever detail and earlier shelter/totem curbside context
- the fortieth `P3` expansion batch now adds red `NO PARK` and green `PERMIT` curbside-reservation boxes, `DROP OFF` and `KISS RIDE` school-dropoff stencils, and left/right separator-arrow panels so the road-marking family no longer stops at earlier school-zone legends, queue boxes, curbside arrows, and generic separator buffers
- the forty-first `P3` expansion batch now adds bus-bay pullout, service-lane apron, curbside drop-off, alley-access, slip-lane pedestrian-island, and mountable-apron-corner road-surface panels so curbside roadway breadth no longer stops at earlier gutter, curb-bulbout, roundabout, and temporary-access composites
- the forty-second `P3` expansion batch now adds `CENTRUM` and `PORTO` service panels, a `METRO`/`PORT` destination stack, deeper `US 50`, `I-80`, `CA 280`, `E75`, and `M1` shield variants, plus larger `CENTRUM`/`PORT` and `METRO`/`PARK` overhead assemblies so sign depth no longer stops at the earlier `CENTRO`/`AEROPORTO`/`METRO`, first overhead-follow-up, and first shield-continuation passes
- the forty-third `P3` expansion batch now adds vertical amber/red warning flashers, a quad-lunar preemption box head, localized diamond-style bus/tram specialty-control heads, and single/quad cantilever dropper follow-up assets so traffic-light depth no longer stops at the earlier compact specialty-control and dual-lunar edge-case passes
- the forty-fourth `P3` expansion batch now adds cantilever service ladders/platforms, a rail bungalow and battery box, plus curbside queue-stanchion and boarding-guardrail support detail so roadside-support depth no longer stops at anchor/footing rail-ancillary follow-up and earlier queue-rail-only curbside context
- the forty-fifth `P3` expansion batch now adds `WAIT`/`QUEUE`, `VALET`/`EV ONLY`, and separator-chevron marking follow-up so curbside queue/reservation and separator guidance depth no longer stops at `NO PARK`, `PERMIT`, school-dropoff, and separator-arrow-only variants
- the forty-sixth `P3` expansion batch now adds floating bus-stop islands, transfer platforms, separator-island taper/refuge panels, and left-hand contraflow or detour-staging roadway follow-up so surface breadth no longer stops at curbside aprons, slip-lane islands, and generic work-zone staging composites
- the forty-seventh `P3` expansion batch now adds `FERRY`, `STAZIONE`, and `GARE` service panels, station/ferry, terminal/metro, and bus/ferry destination stacks, plus larger `STAZIONE`/`PORTO` and `FERRY`/`TERMINAL` overhead guide assemblies so sign depth no longer stops at the earlier gantry-scale multilingual and shield-continuation follow-up batch
- the forty-eighth `P3` expansion batch now adds compact bicycle and pedestrian-bicycle specialty heads, a transit-priority diamond head, dual-amber warning and dual-lunar preemption box heads, plus cantilever backspan, diagonal-brace, and mount-plate follow-up hardware so traffic-light depth no longer stops at the earlier compact bus/tram-control, quad-lunar, and dropper-only cantilever follow-up batch
- the forty-ninth `P3` expansion batch now adds cantilever cable-tray and maintenance-hoist detail, rail predictor/service-post ancillaries, and bus-stop help-point/request-pole microsupport so roadside-support depth no longer stops at ladders/platforms, bungalow/battery-box detail, and validator/timetable-only transit microsupport
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
