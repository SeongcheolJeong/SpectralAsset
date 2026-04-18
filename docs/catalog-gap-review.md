# Catalog Gap Review

## Summary

The current generated baseline now exceeds the original `v1.0` count target through the first thirty `P3` coverage-expansion batches:

- `50` traffic signs
- `21` traffic lights
- `109` roadway and roadside assets split as `28` road surfaces, `38` road markings, and `43` road-furniture assets

The remaining gaps are now mostly about later roadway breadth, deeper specialization, and measurement quality rather than headline asset count.

## Coverage Snapshot by Family

| Family | Current Count | Planned Count | Count Status | Coverage Assessment | Highest-Priority Gaps | Roadmap Phase Pressure |
| --- | --- | --- | --- | --- | --- | --- |
| `traffic_sign` | `50` | `18` | expanded | the baseline now includes heavier-weathered regulatory and construction panels plus route/service, route-shield, destination-stack, and self-contained overhead-guide variants, and scenes place separate backs, brackets, and overhead-frame assemblies for representative sign families | specialty sign assemblies, more locale-specific service panels, additional shield families, measured retroreflective behavior | `P3` later for specialty sign follow-up, `P5` for measured sheeting |
| `traffic_light` | `21` | `5` | expanded | core signal-head catalog now includes beacon-style, warning-flasher, lane-control, rail-crossing, transit-priority, bicycle, pedestrian-bicycle hybrid, and dedicated tram-priority or directional-arrow heads, and scenes place separate backplates, side-mount hardware, a mast hanger, junction/support cabinets, and utility-tail context as support detail | controller nuance, rail-gate assembly context, deeper locale-specific heads, measured emitter spectra | `P3` next for controller nuance and rail-gate context, `P5` for measured SPD |
| `road_surface` | `28` | part of the expanded post-`v1.0` roadway catalog | expanded | baseline roadway surfaces now include patched asphalt, distressed concrete, asphalt-to-concrete transition, gutter-edge transition, gravel shoulders, asphalt-to-gravel transition, construction-plate repairs, milled-overlay and trench-cut construction panels, pothole-distress, eroded shoulder edges, a crowned rural lane panel, dual-rut and washout dirt-track panels, bridge expansion-joint and bridge-approach panels, lane-drop transition panels, curb/barrier composite transitions, ramp bridge-tie and ramp-gore panels, a median-refuge nose, and temporary crossover/barrier-chicane work-zone composites | roundabout aprons, retaining-wall tie-ins, deeper rural shoulder diversity, and more temporary staging nuance | `P3` later for additional roadway composites, `P5` later for measured surface behavior |
| `road_marking` | `38` | part of the expanded post-`v1.0` roadway catalog | expanded | directional arrows, edge lines, worn crossing and stop variants, yellow centerline families, bus/bike legends, hatched median/island panels, white/yellow/bi-color raised-marker strips, boxed curbside/transit legends, red/green colored surfacing panels, curb-color segments, loading zigzag delimiters, and red/green conflict-zone panels now exist alongside the baseline lane and stop geometry | turn-pocket stencils, school-bus queue markings, curbside arrows, and measured retroreflective response | `P3` later after the next signal pass, `P5` for measured optics |
| `road_furniture` | `43` | part of the expanded post-`v1.0` roadway catalog | expanded | roadside, signal-support, sign-assembly, transit-stop, and curbside-loading context now includes guardrails, bollards, delineators, cones, barriers, barricades, utility poles, signal backplates, side-mount and overhead brackets, a mast hanger, cabinet variants, a junction box, service disconnects, meter pedestals, battery-backup cabinets, pull boxes, pad-mount transformers, sign backs, sign mounting brackets, a bus-stop shelter, a stop totem, a bench, a bus-bay curb module, a bus-bay island nose, passenger-information kiosks, real-time arrival displays, loading-zone signposts, loading kiosks, a handhole cluster, and protective service bollards | queue rails, shelter ad panels, curb-ramp modules, and more attachment-hardware depth | `P3` later after the next signal pass |

## Key Findings

- `traffic_sign` is no longer limited to the original Vienna-core starter set: the baseline now includes heavier-weathered yield, no-entry, and construction panels plus hospital, parking, hotel, airport, truck-route, bypass, centre, priority-road, roundabout, stop-ahead, detour, route-shield, stacked destination-guide, and overhead-guide variants, and the scenes place separate sign backs, brackets, and overhead-frame assemblies for representative sign families.
- `traffic_light` is no longer limited to the original five heads: the baseline now includes beacon-style, warning-flasher, lane-control, rail-crossing, transit-priority, bicycle, pedestrian-bicycle hybrid, tram-priority, and dedicated directional-arrow units, and the scenes place explicit backplates, mast-hanger context, side-mount brackets, cabinet variants, and a junction box instead of implying all support context through poles alone.
- `road_surface` is no longer limited to the clean dry/wet urban starter set: the baseline now has patched, distressed, gravel-shoulder, unsealed-transition, construction-plate, milled-overlay, trench-cut, pothole, edge-dropoff, crowned rural-lane, dirt-track, bridge-joint, bridge-approach, lane-drop, barrier-taper, curb-bulbout, ramp-bridge-tie, ramp-gore, median-refuge-nose, and temporary work-zone composite panels that make the current scenes less schematic.
- `road_marking` is no longer minimal: the generator now ships directional arrows, edge-line color variants, worn crossing and stop-line variants, yellow centerline families, bus/bike lane legends, hatched median/island panels, raised-marker variants, boxed curbside/transit legends, red/green lane panels, curb-color segments, loading zigzag delimiters, and red/green conflict-zone surfacing that make the scenes less schematic.
- `road_furniture` now covers much more of the roadside-support tail because the latest batches added utility poles, smaller cabinet/junction variants, service disconnect and metering detail, pull boxes, pad-mount transformers, explicit sign/signal attachment hardware, and now a transit-stop shelter, stop totem, bench, bus-bay curb module, island nose, passenger-information kiosk, real-time arrival display, loading-zone signpost, loading kiosk, handhole cluster, and protective service bollards.
- with the ramp-tie, median-nose, and temporary work-zone composite pass now landed, the next obvious expansion target shifts from `road_surface` toward `traffic_light` controller nuance, rail-gate assembly context, and locale-specific edge-case follow-up.
- `traffic_light` still has room to grow, but the remaining gaps are now mostly controller nuance, rail-gate assembly context, locale-specific edge cases, and measured SPD quality rather than missing starter head families.
- `traffic_sign` now has better assembly, locale, weathering, service-wayfinding, route-shield, destination-stack, and overhead-guide depth, so its remaining gaps are mostly about specialty assemblies, more localized service panels, and measured retroreflective behavior rather than missing starter hardware.

## Priority Queue for Next Asset-Coverage Work

1. Return to `traffic_light` next for controller nuance, rail-gate assembly context, or locale-specific edge-case heads after the latest roadway follow-up lands.
2. Return to `road_furniture` later for queue rails, shelter ad panels, curb-ramp modules, and more attachment-hardware depth once the next signal loop is in place.
3. Return to `road_marking` later for turn-pocket stencils, school-bus queue markings, curbside arrows, and other follow-up lane-control detail once the next signal and roadway loops land.
4. Return to `road_surface` later for roundabout aprons, retaining-wall tie-ins, and deeper temporary work-zone composites after the signal pass lands.
5. Return to `traffic_sign` later for more localized service panels, specialty assemblies, and measured retroreflective depth once the roadway-context loop deepens again.

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
