# Catalog Gap Review

## Summary

The current generated baseline now exceeds the original `v1.0` count target through the first sixteen `P3` coverage-expansion batches:

- `38` traffic signs
- `13` traffic lights
- `71` roadway and roadside assets split as `14` road surfaces, `26` road markings, and `31` road-furniture assets

The remaining gaps are now mostly about later roadway breadth, deeper specialization, and measurement quality rather than headline asset count.

## Coverage Snapshot by Family

| Family | Current Count | Planned Count | Count Status | Coverage Assessment | Highest-Priority Gaps | Roadmap Phase Pressure |
| --- | --- | --- | --- | --- | --- | --- |
| `traffic_sign` | `38` | `18` | expanded | the baseline now includes heavier-weathered regulatory and construction panels plus route/service and locale-oriented hospital, parking, hotel, airport, truck-route, bypass, centre, priority-road, roundabout, stop-ahead, and detour variants, and scenes place separate backs and brackets for representative sign families | route shields, larger destination stacks, specialty sign assemblies, measured retroreflective behavior | `P3` for follow-up sign specialization, `P5` for measured sheeting |
| `traffic_light` | `13` | `5` | expanded | core signal-head catalog now includes beacon-style, warning-flasher, lane-control, and rail-crossing heads, and scenes place separate backplates, side-mount hardware, a mast hanger, junction/support cabinets, and utility-tail context as support detail | richer controller/support families beyond the current starter set, transit-priority or specialty arrow families, measured emitter spectra | `P3` for follow-up signal specialization, `P5` for measured SPD |
| `road_surface` | `14` | part of the expanded post-`v1.0` roadway catalog | expanded | baseline roadway surfaces now include patched asphalt, distressed concrete, asphalt-to-concrete transition, gutter-edge transition, gravel shoulders, asphalt-to-gravel transition, construction-plate repairs, pothole-distress, eroded shoulder edges, and the original dry/wet/sidewalk starter set | lane-drop transitions, crowned rural lane panels, dirt-track variants, bridge-deck joints, and heavier construction staging | `P3` follow-up breadth when scenario scope expands again |
| `road_marking` | `26` | part of the expanded post-`v1.0` roadway catalog | expanded | directional arrows, edge lines, worn crossing and stop variants, yellow centerline families, bus/bike legends, hatched median/island panels, and white/yellow/bi-color raised-marker strips now exist alongside the baseline lane and stop geometry | boxed lane legends, colored bike/transit surfacing, specialty channelization, measured retroreflective response | `P3` follow-up specialization, `P5` for measured optics |
| `road_furniture` | `31` | part of the expanded post-`v1.0` roadway catalog | expanded | roadside, signal-support, and sign-assembly context now includes guardrails, bollards, delineators, cones, barriers, barricades, utility poles, signal backplates, side-mount and overhead brackets, a mast hanger, cabinet variants, a junction box, service disconnects, meter pedestals, battery-backup cabinets, pull boxes, pad-mount transformers, sign backs, and sign mounting brackets | deeper sign-service assemblies, transit-stop or roadside service detail, and more attachment-hardware depth | `P3` follow-up detail after signal and sign breadth |

## Key Findings

- `traffic_sign` is no longer limited to the original Vienna-core starter set: the baseline now includes heavier-weathered yield, no-entry, and construction panels plus hospital, parking, hotel, airport, truck-route, bypass, centre, priority-road, roundabout, stop-ahead, and detour variants, and the scenes place separate sign backs and brackets for representative sign families.
- `traffic_light` is no longer limited to the original five heads: the baseline now includes beacon-style, warning-flasher, lane-control, and rail-crossing units, and the scenes place explicit backplates, mast-hanger context, side-mount brackets, cabinet variants, and a junction box instead of implying all support context through poles alone.
- `road_surface` is no longer limited to the clean dry/wet urban starter set: the baseline now has patched, distressed, gravel-shoulder, unsealed-transition, construction-plate, pothole, and edge-dropoff panels that make the current scenes less schematic.
- `road_marking` is no longer minimal: the generator now ships directional arrows, edge-line color variants, worn crossing and stop-line variants, yellow centerline families, bus/bike lane legends, hatched median/island panels, and raised-marker variants that make the scenes less schematic.
- `road_furniture` now covers much more of the roadside-support tail because the latest batches added utility poles, smaller cabinet/junction variants, service disconnect and metering detail, pull boxes, pad-mount transformers, and explicit sign/signal attachment hardware.
- `traffic_sign` now has broader route/service and wayfinding depth too, so the next obvious expansion target shifts from sign panels back to `road_surface` follow-up breadth.
- `traffic_light` still has room to grow, but the remaining gaps are now mostly transit-priority, lane-use nuance, and measured SPD quality rather than missing starter head families.
- `traffic_sign` now has better assembly, locale, weathering, and service-wayfinding depth, so its remaining gaps are mostly about route shields, larger destination stacks, and measured retroreflective behavior rather than missing starter hardware.

## Priority Queue for Next Asset-Coverage Work

1. Return to `road_surface` for crowned rural lane panels, dirt-track variants, and bridge/joint specialty panels now that the wayfinding sign batch is in place.
2. Return to `traffic_light` later for transit-priority or more locale-specific specialty heads after the support-detail backlog settles.
3. Return to `road_furniture` after that for niche service-assembly or roadside utility detail rather than the just-completed control-tail batch.
4. Return to `road_marking` after that for boxed transit legends, colored bike/transit surfacing, or more specialized channelization rather than the just-completed bus/bike and hatched-island batch.
5. Return to `traffic_sign` after that for route shields and larger destination stacks rather than the just-completed service-wayfinding panel batch.

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
