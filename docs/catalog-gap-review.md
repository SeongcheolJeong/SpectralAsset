# Catalog Gap Review

## Summary

The current generated baseline now exceeds the original `v1.0` count target through the first thirty-nine `P3` coverage-expansion batches:

- `64` traffic signs
- `34` traffic lights
- `159` roadway and roadside assets split as `39` road surfaces, `51` road markings, and `69` road-furniture assets

The remaining gaps are now mostly about later roadway breadth, deeper specialization, and measurement quality rather than headline asset count.

## Coverage Snapshot by Family

| Family | Current Count | Planned Count | Count Status | Coverage Assessment | Highest-Priority Gaps | Roadmap Phase Pressure |
| --- | --- | --- | --- | --- | --- | --- |
| `traffic_sign` | `64` | `18` | expanded | the baseline now includes heavier-weathered regulatory and construction panels plus route/service, route-shield, destination-stack, specialty service, multilingual local-service follow-up, and self-contained overhead-guide variants, and scenes place separate backs, brackets, and overhead-frame assemblies for representative sign families | measured retroreflective behavior, even deeper multilingual/local service breadth, and more gantry-scale guide assemblies | `P3` later for niche sign follow-up, `P5` for measured sheeting |
| `traffic_light` | `34` | `5` | expanded | core signal-head catalog now includes beacon-style, warning-flasher, lane-control, rail-crossing, transit-priority, bus-priority, bicycle, pedestrian-bicycle hybrid, tram-priority, pedestrian-wait, school-warning, compact lane-control, compact bus/tram-control, U-turn-arrow, and single/dual lunar-preemption edge-case heads, and scenes now place both truss and curved-mast cantilever frame/dropper support detail beyond the original starter catalog | still narrower regional specialty heads, controller nuance, and measured emitter spectra | `P3` later for support-detail or niche signal follow-up, `P5` for measured SPD |
| `road_surface` | `39` | part of the expanded post-`v1.0` roadway catalog | expanded | baseline roadway surfaces now include patched asphalt, distressed concrete, asphalt-to-concrete transition, gutter-edge transition, gravel shoulders, asphalt-to-gravel transition, construction-plate repairs, milled-overlay and trench-cut construction panels, pothole-distress, eroded shoulder edges, a crowned rural lane panel, dual-rut and washout dirt-track panels, bridge expansion-joint and bridge-approach panels, lane-drop transition panels, curb/barrier composite transitions, ramp bridge-tie and ramp-gore panels, a median-refuge nose, roundabout truck-apron, splitter-island, outer-ring-edge, and bypass-slip-lane panels, retaining-wall cut, shoulder-shelf, and abutment transitions, and deeper shoefly, staging-pad, laydown-bay, or temporary-access work-zone composites | measured surface behavior and narrower locale-specific roadway composites | `P3` later for niche roadway composites, `P5` later for measured surface behavior |
| `road_marking` | `51` | part of the expanded post-`v1.0` roadway catalog | expanded | directional arrows, edge lines, worn crossing and stop variants, yellow centerline families, turn-pocket `ONLY` stencils, school-zone and school-bus queue legends, curbside arrows, bus/bike legends, hatched median/island panels, white/yellow/bi-color raised-marker strips, boxed curbside/transit legends, red/green colored surfacing panels, curb-color segments, loading zigzag delimiters, red/green conflict-zone panels, `SLOW`/`XING` school-zone legends, white/green separator-buffer panels, and pick-up or taxi curbside boxes now exist alongside the baseline lane and stop geometry | measured retroreflective response, more localized separator patterns, and additional curbside or school-zone specialization | `P3` next for another localized reservation/school follow-up loop, `P5` for measured optics |
| `road_furniture` | `69` | part of the expanded post-`v1.0` roadway catalog | expanded | roadside, signal-support, sign-assembly, transit-stop, curbside-loading, and rail-gate context now includes guardrails, bollards, delineators, cones, barriers, barricades, utility poles, signal backplates, side-mount and overhead brackets, band-clamp hardware, cabinet variants, a junction box, service disconnects, meter pedestals, battery-backup cabinets, pull boxes, pad-mount transformers, sign backs, sign mounting brackets, a bus-stop shelter, a shelter ad panel, a stop totem, a bench, a queue rail, a bus-bay curb module, a bus-bay island nose, straight and corner curb-ramp modules, passenger-information kiosks, real-time arrival displays, loading-zone signposts, loading kiosks, a handhole cluster, protective service bollards, rail-gate mast/arm/bell/controller detail, truss and curved-mast cantilever signal-frame assets, dual/triple dropper follow-up pieces, shelter/separator/hanger-clamp follow-up hardware, cantilever anchor-cage and footing-collar detail, rail-side power-disconnect and relay-case ancillaries, plus validator-pedestal and timetable-blade transit microsupport pieces | still finer anchor hardware, shelter microsupport breadth, and measured support-material behavior | `P3` later after the next marking loop |

## Key Findings

- `traffic_sign` is no longer limited to the original Vienna-core starter set: the baseline now includes heavier-weathered yield, no-entry, and construction panels plus hospital, parking, hotel, airport, bus-station, truck-route, bypass, centre, `CENTRO`, `AEROPORTO`, `METRO`, priority-road, roundabout, stop-ahead, detour, route-shield, stacked destination-guide, and overhead-guide variants, and the scenes place separate sign backs, brackets, and overhead-frame assemblies for representative sign families.
- `traffic_light` is no longer limited to the original five heads: the baseline now includes beacon-style, warning-flasher, compact and full-size lane-control, rail-crossing, transit-priority, compact and full-size bus/tram priority, bicycle, pedestrian-bicycle hybrid, pedestrian-wait, school-warning, single/dual-lunar preemption, and dedicated directional-arrow or U-turn-arrow units, and the scenes place explicit backplates, mast-hanger context, truss and curved-mast cantilever frame/dropper context, side-mount brackets, rail-gate context, cabinet variants, and a junction box instead of implying all support context through poles alone.
- `road_surface` is no longer limited to the clean dry/wet urban starter set: the baseline now has patched, distressed, gravel-shoulder, unsealed-transition, construction-plate, milled-overlay, trench-cut, pothole, edge-dropoff, crowned rural-lane, dirt-track, bridge-joint, bridge-approach, lane-drop, barrier-taper, curb-bulbout, ramp-bridge-tie, ramp-gore, median-refuge-nose, roundabout truck-apron, splitter-island, outer-ring-edge, and bypass-slip-lane panels, retaining-wall cut, shoulder-shelf, and abutment transitions, and deeper shoefly, staging-pad, laydown-bay, or temporary-access work-zone composites that make the current scenes less schematic.
- `road_marking` is no longer minimal: the generator now ships directional arrows, edge-line color variants, worn crossing and stop-line variants, yellow centerline families, turn-pocket `ONLY` stencils, school-zone and school-bus queue markings, `SLOW` and `XING` legends, curbside arrows, bus/bike lane legends, hatched median/island panels, raised-marker variants, boxed curbside/transit legends, pick-up and taxi curbside boxes, white/green separator-buffer panels, curb-color segments, loading zigzag delimiters, and red/green conflict-zone surfacing that make the scenes less schematic.
- `road_furniture` now covers much more of the roadside-support tail because the latest batches added utility poles, smaller cabinet/junction variants, service disconnect and metering detail, pull boxes, pad-mount transformers, explicit sign/signal attachment hardware, transit-stop shelter/totem/bench detail, loading-zone curbside context, rail-gate mast/arm/bell/controller detail, queue-rail/shelter-panel/curb-ramp/clamp-hardware follow-up assets, truss and curved-mast cantilever signal-frame/dropper detail, shelter trash, route-map, lean-rail, curb-separator, hanger-clamp follow-up assets, and the newer cantilever-anchor, footing-collar, rail-power, rail-relay, validator-pedestal, and timetable-blade microsupport pieces.
- with the latest furniture loop now landed, the next obvious expansion target shifts from `road_furniture` toward another `road_marking` pass for curbside reservation, school-dropoff, and separator-arrow follow-up detail.
- `traffic_light` still has room to grow, but the remaining gaps are now mostly about still narrower regional edge cases, smaller controller-face nuance, and measured SPD quality rather than missing starter head families.
- `traffic_sign` now has better assembly, locale, weathering, service-wayfinding, route-shield, destination-stack, and overhead-guide depth, so its remaining gaps are mostly about gantry-scale follow-up, still narrower multilingual/local service breadth, and measured retroreflective behavior rather than missing starter hardware.

## Priority Queue for Next Asset-Coverage Work

1. Return to `road_marking` next for curbside reservation, school-dropoff, and separator-arrow follow-up now that the latest furniture loop has landed.
2. Return to `road_surface` later for narrower locale-specific roadway composites and measured behavior follow-up after the next marking loop lands.
3. Return to `traffic_sign` later for gantry-scale guide follow-up and still narrower multilingual/local service breadth after the next marking loop lands.
4. Return to `traffic_light` later for even narrower regional control-face edge cases after the next marking loop lands.
5. Return to `road_furniture` later for still finer anchor, shelter microsupport, and rail-side ancillary follow-up after the next marking loop lands.

## Phase Mapping

| Roadmap Phase | Recommended Coverage Work |
| --- | --- |
| `P3` | geometry and template additions for `road_furniture`, `road_marking`, `traffic_light`, and `traffic_sign` support variants |
| `P4` | scenario and validation-scene updates that exercise the new coverage rather than only adding counts |
| `P5` | measured upgrades for retroreflective and emissive behavior once the broader geometry catalog is stable |

## Scope Guardrails

- The original `v1.0` baseline remains valid, and the current catalog should be treated as a count-expanded baseline rather than a reset of the contract.
- Future count expansion should not break the naming and manifest contracts in [asset-spec.md](asset-spec.md).
- Coverage reviews should distinguish count completeness from fidelity completeness. The current pack is count-complete, but not depth-complete.
