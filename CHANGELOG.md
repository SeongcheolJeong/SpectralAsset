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
- third `P3` traffic-light support-context batch with signal backplates, a mast hanger, and a controller cabinet
- fourth `P3` sign-assembly batch with standalone sign backs and mounting brackets
- fifth `P3` road-surface batch with patched asphalt, distressed concrete, asphalt-to-concrete transition, and gutter-transition panels
- sixth `P3` road-marking batch with worn crosswalk and stop-line variants, a yellow edge line, a merge marking, and a raised-marker strip
- seventh `P3` road-furniture batch with utility poles, smaller signal-support cabinets, a junction box, and specialty sign/signal attachment hardware
- eighth `P3` traffic-light batch with beacon-style and warning-flasher heads plus explicit per-asset state maps for the existing signal catalog
- ninth `P3` traffic-sign batch with weathered stop, speed-limit, and pedestrian-crossing variants plus English text-bearing one-way and detour panels
- tenth `P3` road-marking batch with yellow centerline families, `ONLY` and `STOP` word legends, and yellow/bi-color raised-marker variants
- eleventh `P3` road-surface batch with gravel-shoulder, asphalt-to-gravel transition, construction-plate, pothole-distress, and eroded-shoulder variants plus a compact-gravel proxy material
- twelfth `P3` traffic-light batch with lane-control and rail-crossing heads plus dedicated lane-control and rail-specific emissive profiles
- thirteenth `P3` road-furniture batch with service-disconnect, meter-pedestal, battery-backup, pull-box, and pad-mount-transformer assets
- fourteenth `P3` traffic-sign batch with priority-road, roundabout, stop-ahead, detour-right, and heavier-weathered yield/no-entry/construction variants plus a heavier sign-weathering overlay material
- fifteenth `P3` road-marking batch with bus/bike legends, hatched median/island panels, and right-turn or straight-right arrow variants
- sixteenth `P3` traffic-sign batch with hospital, parking, hotel, airport, truck-route, bypass, and centre wayfinding panels
- seventeenth `P3` road-surface batch with a crowned rural lane, two dirt-track panels, a bridge expansion-joint panel, and a lane-drop transition panel
- eighteenth `P3` traffic-light batch with transit-priority and directional-arrow signal heads plus dedicated transit-priority and directional-arrow emissive profiles
- nineteenth `P3` road-furniture batch with a bus-stop shelter, stop totem, bench, handhole cluster, and protective service-bollard pair
- twentieth `P3` road-marking batch with boxed curbside/transit legends and red/green colored lane panels plus two new colored marking materials
- twenty-first `P3` traffic-sign batch with U.S./interstate/E-route shields and stacked destination-guide panels plus scene coverage for the new route-context variants
- twenty-second `P3` road-surface batch with milled-overlay, trench-cut, bridge-approach, barrier-taper, and curb-bulbout variants plus scene coverage for the new roadway-context panels
- twenty-third `P3` traffic-light batch with bicycle, pedestrian-bicycle hybrid, and tram-priority heads plus dedicated hybrid or specialty emissive profiles
- twenty-fourth `P3` road-furniture batch with bus-bay curb and island modules, passenger-information and real-time-arrival hardware, plus loading-zone sign/kiosk detail
- twenty-fifth `P3` road-marking batch with curb-color segments, loading zigzag delimiters, red/green conflict-zone panels, and a blue marking material
- twenty-sixth `P3` traffic-sign batch with self-contained overhead destination assemblies plus California, UK motorway, and French autoroute shield follow-up variants
- twenty-seventh `P3` road-surface batch with ramp bridge-tie, ramp-gore, median-refuge-nose, and temporary crossover/barrier-chicane work-zone composite panels
- twenty-eighth `P3` traffic-light batch with school-warning, pedestrian-wait, and lunar-preemption heads plus rail-gate mast, arm, bell, and controller-cabinet context
- twenty-ninth `P3` road-furniture batch with queue rails, shelter ad panels, straight/corner curb-ramp modules, and sign/signal band-clamp hardware
- thirtieth `P3` road-marking batch with turn-pocket `ONLY` stencils, `SCHOOL` legends, `SCHOOL BUS` queue boxes, and curbside left/right arrows
- thirty-first `P3` road-surface batch with roundabout truck-apron and splitter-island panels, a retaining-wall cut transition, and deeper shoefly/staging-pad work-zone surfaces
- thirty-second `P3` traffic-sign batch with a bus-station service panel, an airport/parking destination stack, a hospital/parking overhead assembly, and Interstate-405, E20, and California-82 shield follow-up variants
- thirty-third `P3` traffic-light batch with bus-priority, U-turn-arrow, horizontal school-warning, and dual-lunar preemption heads plus cantilever frame/dropper support detail
- thirty-fourth `P3` road-furniture batch with shelter trash, route-map, and lean-rail accessories plus curb-separator flexpost/kerb modules and signal hanger-clamp pairs
- thirty-fifth `P3` road-marking batch with `SLOW`/`XING` school-zone legends, white/green separator-buffer panels, and pick-up/taxi curbside box variants
- thirty-sixth `P3` road-surface batch with roundabout outer-ring and bypass-slip-lane panels, retaining-wall shoulder-shelf and abutment transitions, plus laydown-bay and temporary-access work-zone surfaces
- thirty-seventh `P3` traffic-sign batch with `CENTRO`, `AEROPORTO`, and `METRO` service panels, a larger `CENTRO`/`HOTEL` destination stack, deeper `US 66`/`CA 17`/`A9` shield variants, and a larger overhead `AEROPORTO`/`CENTRO` split assembly
- thirty-eighth `P3` traffic-light batch with compact lane-control, compact bus/tram-priority, single-amber school-warning, and vertical dual-lunar preemption heads plus curved-mast cantilever and triple-dropper support variants

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
- existing validation scenes now place explicit traffic-light support-context assets so intersections no longer imply all signal support through poles alone
- existing validation scenes now place explicit sign backs and brackets so representative sign assemblies no longer imply all depth through the sign meshes alone
- existing validation scenes now place patched, distressed, and transition surface panels so roadway context is no longer limited to the original clean urban starter set
- existing validation scenes now place secondary road-marking assets so worn crossings/stops, a yellow edge line, a merge marking, and raised markers are exercised in scene exports
- existing validation scenes now place utility poles, smaller cabinet/junction variants, and explicit sign/signal attachment hardware so support context is deeper than the original roadside starter set
- existing validation scenes now place beacon-style and warning-flasher signal heads so the traffic-light catalog is no longer limited to the original five-head starter set
- existing validation scenes now place weathered sign variants plus English text-bearing one-way and detour panels so the sign catalog is no longer limited to symbol-only starter faces
- existing validation scenes now place yellow centerline variants, `ONLY`/`STOP` legends, and white/yellow/bi-color raised-marker strips so the road-marking catalog is no longer limited to the earlier edge-line and arrow expansion batches
- existing validation scenes now place gravel-shoulder, asphalt-to-gravel transition, construction-plate, pothole-distress, and eroded-shoulder variants so roadway context is broader than the earlier urban repair subset alone
- existing validation scenes now place lane-control and rail-crossing signal heads so the traffic-light family is broader than the earlier vehicle, pedestrian, beacon, and generic warning-flasher set
- existing validation scenes now place service-disconnect, meter-pedestal, battery-backup, pull-box, and pad-mount-transformer assets so roadside control-tail context extends beyond the earlier pole/cabinet/junction set
- existing validation scenes now place priority-road, roundabout, stop-ahead, detour-right, and heavier-weathered yield/no-entry/construction sign variants so sign depth is broader than the earlier starter weathering batch
- existing validation scenes now place bus/bike legends, hatched median/island panels, and right-turn or straight-right arrow variants so road-marking depth is broader than the earlier centerline and basic word-legend batches
- existing validation scenes now place hospital, parking, hotel, airport, truck-route, bypass, and centre panels so sign depth is broader than the earlier regulatory/weathering and detour-only wayfinding passes
- existing validation scenes now place crowned rural-lane, dirt-track, bridge-joint, and lane-drop surface panels so roadway breadth is broader than the earlier urban repair and gravel-shoulder follow-up batches
- existing validation scenes now place transit-priority and directional-arrow signal heads so traffic-light specialization is broader than the earlier lane-control and rail-crossing batches
- existing validation scenes now place a transit-stop shelter, stop totem, bench, grouped handholes, and protective service bollards so curbside context is broader than the earlier signal-control and support-hardware batches
- existing validation scenes now place boxed `BUS ONLY`, `BUS STOP`, `BIKE`, and `LOAD` legends plus red/green lane panels so road-marking context is broader than the earlier monochrome word-legend and hatched-island batches
- existing validation scenes now place U.S./interstate/E-route shields plus stacked airport/centre, hotel/park, and truck/bypass destination-guide panels so sign-route context is broader than the earlier single-destination wayfinding batches
- existing validation scenes now place milled-overlay, trench-cut, bridge-approach, barrier-taper, and curb-bulbout roadway panels so surface context is broader than the earlier repair, rural-lane, and bridge-joint batches
- existing validation scenes now place bicycle, pedestrian-bicycle hybrid, and tram-priority heads so signal context is broader than the earlier lane-control, transit-priority, and directional-arrow specialization batches
- existing validation scenes now place school-warning, pedestrian-wait, and lunar-preemption heads plus rail-gate mast/arm/bell/controller context so signal scenes are broader than the earlier specialty-head-only rail/transit batches
- existing validation scenes now place queue rails, shelter ad panels, straight/corner curb-ramp modules, and sign/signal band-clamp hardware so curbside scenes are broader than the earlier shelter-only transit and bracket-only attachment passes
- existing validation scenes now place turn-pocket `ONLY` stencils, `SCHOOL` legends, `SCHOOL BUS` queue boxes, and curbside left/right arrows so road-marking scenes are broader than the earlier boxed curbside, conflict-zone, and generic-arrow follow-up passes
- existing validation scenes now place roundabout truck-apron and splitter-island panels, a retaining-wall cut transition, and deeper shoefly/staging-pad work-zone surfaces so roadway scenes are broader than the earlier ramp-gore, median-nose, and temporary crossover/chicane follow-up passes
- existing validation scenes now place bus-station service panels, airport/parking destination stacks, a hospital/parking overhead assembly, and Interstate-405, E20, and California-82 shield follow-up variants so sign scenes are broader than the earlier overhead-destination and first route-shield follow-up batch
- existing validation scenes now place bus-priority, U-turn-arrow, horizontal school-warning, and dual-lunar preemption heads plus cantilever frame/dropper support detail so traffic-light scenes are broader than the earlier rail-gate/controller-nuance follow-up that still relied on simpler side-mount or starter mast-arm context
- existing validation scenes now place shelter trash receptacles, route-map cases, lean rails, curb-separator flexpost/kerb modules, and signal hanger-clamp pairs so roadside scenes are broader than the earlier shelter-panel, curb-ramp, and clamp-hardware follow-up batch
- existing validation scenes now place `SLOW`/`XING` school-zone legends, white/green separator-buffer panels, and pick-up/taxi curbside boxes so road-marking scenes are broader than the earlier school-bus, curbside-arrow, and generic boxed-curbside follow-up batch
- existing validation scenes now place roundabout outer-ring and bypass-slip-lane panels, retaining-wall shoulder-shelf and abutment transitions, plus laydown-bay and temporary-access work-zone surfaces so roadway scenes are broader than the earlier roundabout-apron, retaining-wall cut, and staging-pad follow-up batch
- existing validation scenes now place `CENTRO`, `AEROPORTO`, and `METRO` service panels, a larger `CENTRO`/`HOTEL` destination stack, deeper `US 66`/`CA 17`/`A9` shield variants, and a larger overhead `AEROPORTO`/`CENTRO` split assembly so sign scenes are broader than the earlier localized-service, airport/parking, and first shield-depth follow-up batch
- existing validation scenes now place compact lane-control, single-amber school-warning, compact bus/tram-priority, and vertical dual-lunar preemption heads plus a curved cantilever mast and triple-dropper subtype so traffic-light scenes are broader than the earlier full-size specialty-control and single cantilever-frame follow-up batch
- backlog focus now moves from `traffic_light` narrower regional edge-case, cantilever-subtype, and specialty-control work to `road_furniture` cantilever-footing, rail-side ancillary, and transit-stop microsupport follow-up after the latest signal batch

### Validation

- validation summary now reports `50` assets, including `14` `road_furniture` assets and `9` `road_marking` assets after the first three `P3` expansion batches
- validation summary now reports `57` assets, including `21` `road_furniture` assets and `9` `road_marking` assets after the first four `P3` expansion batches
- validation summary now reports `61` assets, including `8` `road_surface` assets, `9` `road_marking` assets, and `21` `road_furniture` assets after the first five `P3` expansion batches
- validation summary now reports `66` assets, including `8` `road_surface` assets, `14` `road_marking` assets, and `21` `road_furniture` assets after the first six `P3` expansion batches
- validation summary now reports `72` assets, including `8` `road_surface` assets, `14` `road_marking` assets, and `27` `road_furniture` assets after the first seven `P3` expansion batches
- validation summary now reports `76` assets, including `9` `traffic_light` assets, `8` emissive profiles, and `80` GLB files after the first eight `P3` expansion batches
- validation summary now reports `82` assets, including `24` `traffic_sign` assets, `21` spectral materials, and `86` GLB files after the first nine `P3` expansion batches
- validation summary now reports `88` assets, including `20` `road_marking` assets, `21` spectral materials, and `92` GLB files after the first ten `P3` expansion batches
- validation summary now reports `93` assets, including `13` `road_surface` assets, `22` spectral materials, and `97` GLB files after the first eleven `P3` expansion batches
- validation summary now reports `97` assets, including `13` `traffic_light` assets, `11` emissive profiles, and `101` GLB files after the first twelve `P3` expansion batches
- validation summary now reports `102` assets, including `32` `road_furniture` assets, `22` spectral materials, and `106` GLB files after the first thirteen `P3` expansion batches
- validation summary now reports `109` assets, including `31` `traffic_sign` assets, `23` spectral materials, and `113` GLB files after the first fourteen `P3` expansion batches
- validation summary now reports `115` assets, including `26` `road_marking` assets, `23` spectral materials, and `119` GLB files after the first fifteen `P3` expansion batches
- validation summary now reports `122` assets, including `38` `traffic_sign` assets, `23` spectral materials, and `126` GLB files after the first sixteen `P3` expansion batches
- validation summary now reports `127` assets, including `18` `road_surface` assets, `23` spectral materials, and `131` GLB files after the first seventeen `P3` expansion batches
- validation summary now reports `131` assets, including `17` `traffic_light` assets, `13` emissive profiles, and `135` GLB files after the first eighteenth `P3` expansion batch
- validation summary now reports `136` assets, including `37` `road_furniture` assets, `13` emissive profiles, and `140` GLB files after the first nineteenth `P3` expansion batch
- validation summary now reports `142` assets, including `32` `road_marking` assets, `25` spectral materials, and `146` GLB files after the first twentieth `P3` expansion batch
- validation summary now reports `148` assets, including `44` `traffic_sign` assets, `26` spectral materials, and `152` GLB files after the first twenty-first `P3` expansion batch
- validation summary now reports `153` assets, including `23` `road_surface` assets, `26` spectral materials, and `157` GLB files after the first twenty-second `P3` expansion batch
- validation summary now reports `157` assets, including `21` `traffic_light` assets, `16` emissive profiles, and `161` GLB files after the first twenty-third `P3` expansion batch
- validation summary now reports `163` assets, including `43` `road_furniture` assets, `26` spectral materials, and `167` GLB files after the first twenty-fourth `P3` expansion batch
- validation summary now reports `169` assets, including `38` `road_marking` assets, `27` spectral materials, and `173` GLB files after the first twenty-fifth `P3` expansion batch
- validation summary now reports `175` assets, including `50` `traffic_sign` assets, `27` spectral materials, and `179` GLB files after the first twenty-sixth `P3` expansion batch
- validation summary now reports `180` assets, including `28` `road_surface` assets, `27` spectral materials, and `184` GLB files after the first twenty-seventh `P3` expansion batch
- validation summary now reports `187` assets, including `24` `traffic_light` assets, `47` `road_furniture` assets, `19` emissive profiles, and `191` GLB files after the first twenty-eighth `P3` expansion batch
- validation summary now reports `193` assets, including `53` `road_furniture` assets, `27` spectral materials, and `197` GLB files after the first twenty-ninth `P3` expansion batch
- validation summary now reports `200` assets, including `45` `road_marking` assets, `27` spectral materials, and `204` GLB files after the first thirtieth `P3` expansion batch
- validation summary now reports `205` assets, including `33` `road_surface` assets, `27` spectral materials, and `209` GLB files after the first thirty-first `P3` expansion batch
- validation summary now reports `211` assets, including `56` `traffic_sign` assets, `27` spectral materials, and `215` GLB files after the first thirty-second `P3` expansion batch
- validation summary now reports `218` assets, including `29` `traffic_light` assets, `55` `road_furniture` assets, `22` emissive profiles, and `222` GLB files after the first thirty-third `P3` expansion batch
- validation summary now reports `224` assets, including `61` `road_furniture` assets, `27` spectral materials, and `228` GLB files after the first thirty-fourth `P3` expansion batch
- validation summary now reports `230` assets, including `51` `road_marking` assets, `27` spectral materials, and `234` GLB files after the first thirty-fifth `P3` expansion batch
- validation summary now reports `236` assets, including `39` `road_surface` assets, `27` spectral materials, and `240` GLB files after the first thirty-sixth `P3` expansion batch
- validation summary now reports `244` assets, including `64` `traffic_sign` assets, `27` spectral materials, and `248` GLB files after the first thirty-seventh `P3` expansion batch
- validation summary now reports `251` assets, including `34` `traffic_light` assets, `63` `road_furniture` assets, `23` emissive profiles, and `255` GLB files after the first thirty-eighth `P3` expansion batch
- validation summary now reports `257` assets, including `69` `road_furniture` assets, `23` emissive profiles, and `261` GLB files after the first thirty-ninth `P3` expansion batch
- validation summary now reports `263` assets, including `57` `road_marking` assets, `23` emissive profiles, and `267` GLB files after the fortieth `P3` expansion batch
- validation summary now reports `269` assets, including `45` `road_surface` assets, `27` spectral materials, and `273` GLB files after the first forty-first `P3` expansion batch
- validation summary now reports `279` assets, including `74` `traffic_sign` assets, `27` spectral materials, and `283` GLB files after the first forty-second `P3` expansion batch
- validation summary now reports `286` assets, including `39` `traffic_light` assets, `24` emissive profiles, and `290` GLB files after the first forty-third `P3` expansion batch
- validation summary now includes `3` camera profiles and zero camera-profile validation errors
- material quality summary now reports `3` `measured_standard`, `1` `measured_derivative`, `23` `project_proxy`, and `0` `vendor_derived` materials
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
