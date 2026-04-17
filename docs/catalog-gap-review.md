# Catalog Gap Review

## Summary

The current generated baseline now exceeds the original `v1.0` count target through the first eleven `P3` coverage-expansion batches:

- `24` traffic signs
- `9` traffic lights
- `60` roadway and roadside assets split as `13` road surfaces, `20` road markings, and `27` road-furniture assets

The remaining gaps are now mostly about later roadway breadth, deeper specialization, and measurement quality rather than headline asset count.

## Coverage Snapshot by Family

| Family | Current Count | Planned Count | Count Status | Coverage Assessment | Highest-Priority Gaps | Roadmap Phase Pressure |
| --- | --- | --- | --- | --- | --- | --- |
| `traffic_sign` | `24` | `18` | expanded | the baseline now includes starter weathered variants plus English text-bearing one-way and detour panels, and scenes place separate backs and brackets for representative sign families | deeper locale families, stronger weathering diversity, specialty sign assemblies, measured retroreflective behavior | `P3` for deeper sign specialization, `P5` for measured sheeting |
| `traffic_light` | `9` | `5` | expanded | core signal-head catalog now includes beacon-style and warning-flasher heads, and scenes place separate backplates, side-mount hardware, a mast hanger, junction/support cabinets, and utility-tail context as support detail | lane-control or rail-specific heads, richer controller/support families beyond the current starter set, measured emitter spectra | `P3` for follow-up signal specialization, `P5` for measured SPD |
| `road_surface` | `13` | part of the expanded post-`v1.0` roadway catalog | expanded | baseline roadway surfaces now include patched asphalt, distressed concrete, asphalt-to-concrete transition, gutter-edge transition, gravel shoulders, asphalt-to-gravel transition, construction-plate repairs, pothole-distress, eroded shoulder edges, and the original dry/wet/sidewalk starter set | lane-drop transitions, crowned rural lane panels, dirt-track variants, bridge-deck joints, and heavier construction staging | `P3` follow-up breadth when scenario scope expands again |
| `road_marking` | `20` | part of the expanded post-`v1.0` roadway catalog | expanded | directional arrows, edge lines, worn crossing and stop variants, yellow centerline families, `STOP`/`ONLY` word legends, and white/yellow/bi-color raised-marker strips now exist alongside the baseline lane and stop geometry | additional turn arrows, bus or bike lane legends, hatched median/island markings, measured retroreflective response | `P3` follow-up specialization, `P5` for measured optics |
| `road_furniture` | `27` | part of the expanded post-`v1.0` roadway catalog | expanded | roadside, signal-support, and sign-assembly context now includes guardrails, bollards, delineators, cones, barriers, barricades, utility poles, signal backplates, side-mount and overhead brackets, a mast hanger, cabinet variants, a junction box, sign backs, and sign mounting brackets | utility service-detail variants, cabinet families beyond the current starter set, specialty sign assemblies, and more attachment-hardware depth | `P3` follow-up detail after signal and sign breadth |

## Key Findings

- `traffic_sign` is no longer limited to the original Vienna-core starter set: the baseline now includes weathered stop, speed-limit, and pedestrian-crossing variants plus English text-bearing one-way and detour panels, and the scenes place separate sign backs and brackets for representative sign families.
- `traffic_light` is no longer limited to the original five heads: the baseline now includes beacon-style and warning-flasher units, and the scenes place explicit backplates, mast-hanger context, side-mount brackets, cabinet variants, and a junction box instead of implying all support context through poles alone.
- `road_surface` is no longer limited to the clean dry/wet urban starter set: the baseline now has patched, distressed, gravel-shoulder, unsealed-transition, construction-plate, pothole, and edge-dropoff panels that make the current scenes less schematic.
- `road_marking` is no longer minimal: the generator now ships directional arrows, edge-line color variants, worn crossing and stop-line variants, yellow centerline families, `STOP`/`ONLY` word legends, and raised-marker variants that make the scenes less schematic.
- `road_furniture` now covers much more of the roadside-support tail because the latest batch added utility poles, smaller cabinet/junction variants, and explicit sign/signal attachment hardware.
- `road_surface` now has a stronger roadway-breadth starter set, so the next obvious expansion target shifts from general roadway breadth back to specialized `traffic_light` heads.
- `traffic_light` still has room to grow, but the remaining gaps are now mostly specialized signal-head families rather than missing support-context basics.
- `traffic_sign` now has better assembly and variation depth, so its remaining gaps are mostly about breadth of locale families and more specialized weathering states rather than missing starter hardware.

## Priority Queue for Next Asset-Coverage Work

1. Return to `traffic_light` for lane-control or rail-specific heads now that the higher-pressure roadway breadth batch is in place.
2. Return to `road_furniture` for deeper utility service detail and specialty attachment hardware after the next signal-head batch.
3. Return to `traffic_sign` for broader locale families and heavier weathering diversity after the next signal-head batch.
4. Return to `road_marking` later for bus/bike legends, hatched medians, and more specialized directional variants after the broader roadway backlog settles.
5. Return to `road_surface` after that for crowned rural lane panels, dirt-track variants, and bridge/joint specialty panels rather than the just-completed shoulder-and-distress batch.

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
