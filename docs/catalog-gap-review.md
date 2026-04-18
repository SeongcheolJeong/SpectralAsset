# Catalog Gap Review

## Summary

The current generated baseline now exceeds the original `v1.0` count target through the first twenty `P3` coverage-expansion batches:

- `38` traffic signs
- `17` traffic lights
- `87` roadway and roadside assets split as `18` road surfaces, `32` road markings, and `37` road-furniture assets

The remaining gaps are now mostly about later roadway breadth, deeper specialization, and measurement quality rather than headline asset count.

## Coverage Snapshot by Family

| Family | Current Count | Planned Count | Count Status | Coverage Assessment | Highest-Priority Gaps | Roadmap Phase Pressure |
| --- | --- | --- | --- | --- | --- | --- |
| `traffic_sign` | `38` | `18` | expanded | the baseline now includes heavier-weathered regulatory and construction panels plus route/service and locale-oriented hospital, parking, hotel, airport, truck-route, bypass, centre, priority-road, roundabout, stop-ahead, and detour variants, and scenes place separate backs and brackets for representative sign families | route shields, larger destination stacks, specialty sign assemblies, measured retroreflective behavior | `P3` for follow-up sign specialization, `P5` for measured sheeting |
| `traffic_light` | `17` | `5` | expanded | core signal-head catalog now includes beacon-style, warning-flasher, lane-control, rail-crossing, transit-priority, and dedicated directional-arrow heads, and scenes place separate backplates, side-mount hardware, a mast hanger, junction/support cabinets, and utility-tail context as support detail | pedestrian-hybrid or locale-specific specialty heads, deeper controller/support families, measured emitter spectra | `P3` for later follow-up signal specialization, `P5` for measured SPD |
| `road_surface` | `18` | part of the expanded post-`v1.0` roadway catalog | expanded | baseline roadway surfaces now include patched asphalt, distressed concrete, asphalt-to-concrete transition, gutter-edge transition, gravel shoulders, asphalt-to-gravel transition, construction-plate repairs, pothole-distress, eroded shoulder edges, a crowned rural lane panel, dual-rut and washout dirt-track panels, a bridge expansion-joint panel, and a lane-drop transition panel | heavier construction staging, bridge approaches, barrier/curb transitions, and deeper rural shoulder diversity | `P3` follow-up breadth after traffic-light specialization cycles back |
| `road_marking` | `32` | part of the expanded post-`v1.0` roadway catalog | expanded | directional arrows, edge lines, worn crossing and stop variants, yellow centerline families, bus/bike legends, hatched median/island panels, white/yellow/bi-color raised-marker strips, boxed curbside/transit legends, and red/green colored surfacing panels now exist alongside the baseline lane and stop geometry | turn-pocket stencils, colored conflict-zone surfacing, curb-color/loading delimiters, measured retroreflective response | `P3` follow-up specialization, `P5` for measured optics |
| `road_furniture` | `37` | part of the expanded post-`v1.0` roadway catalog | expanded | roadside, signal-support, sign-assembly, and transit-stop context now includes guardrails, bollards, delineators, cones, barriers, barricades, utility poles, signal backplates, side-mount and overhead brackets, a mast hanger, cabinet variants, a junction box, service disconnects, meter pedestals, battery-backup cabinets, pull boxes, pad-mount transformers, sign backs, sign mounting brackets, a bus-stop shelter, a stop totem, a bench, a handhole cluster, and protective service bollards | bus-bay curb detail, curbside passenger-loading hardware, and more attachment-hardware depth | `P3` follow-up detail after the transit-stop/service pass |

## Key Findings

- `traffic_sign` is no longer limited to the original Vienna-core starter set: the baseline now includes heavier-weathered yield, no-entry, and construction panels plus hospital, parking, hotel, airport, truck-route, bypass, centre, priority-road, roundabout, stop-ahead, and detour variants, and the scenes place separate sign backs and brackets for representative sign families.
- `traffic_light` is no longer limited to the original five heads: the baseline now includes beacon-style, warning-flasher, lane-control, rail-crossing, transit-priority, and dedicated directional-arrow units, and the scenes place explicit backplates, mast-hanger context, side-mount brackets, cabinet variants, and a junction box instead of implying all support context through poles alone.
- `road_surface` is no longer limited to the clean dry/wet urban starter set: the baseline now has patched, distressed, gravel-shoulder, unsealed-transition, construction-plate, pothole, edge-dropoff, crowned rural-lane, dirt-track, bridge-joint, and lane-drop panels that make the current scenes less schematic.
- `road_marking` is no longer minimal: the generator now ships directional arrows, edge-line color variants, worn crossing and stop-line variants, yellow centerline families, bus/bike lane legends, hatched median/island panels, raised-marker variants, boxed curbside/transit legends, and red/green lane panels that make the scenes less schematic.
- `road_furniture` now covers much more of the roadside-support tail because the latest batches added utility poles, smaller cabinet/junction variants, service disconnect and metering detail, pull boxes, pad-mount transformers, explicit sign/signal attachment hardware, and now a transit-stop shelter, stop totem, bench, handhole cluster, and protective service bollards.
- with curbside/transit legend boxes and colored surfacing now present, the next obvious expansion target shifts away from markings and toward `traffic_sign` route shields and larger destination-guide stacks.
- `traffic_light` still has room to grow, but the remaining gaps are now mostly pedestrian-hybrid or locale-specific specialty heads, controller nuance, and measured SPD quality rather than missing starter head families.
- `traffic_sign` now has better assembly, locale, weathering, and service-wayfinding depth, so its remaining gaps are mostly about route shields, larger destination stacks, and measured retroreflective behavior rather than missing starter hardware.

## Priority Queue for Next Asset-Coverage Work

1. Return to `traffic_sign` for route shields and larger destination stacks beyond the current service-wayfinding panel batch.
2. Return to `road_surface` after that for heavier construction staging, bridge approaches, and curb/barrier transition composites now that curbside/transit-lane markings are in place.
3. Return to `traffic_light` later for pedestrian-hybrid or locale-specific specialty heads after the route-context loop deepens.
4. Return to `road_furniture` later for bus-bay curb modules, passenger-information hardware, and deeper loading-zone detail once the sign and marking loops establish that curbside context.
5. Return to `road_marking` later for turn-pocket stencils, conflict-zone surfacing, and curb-color/loading delimiters after the route-shield sign pass lands.

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
