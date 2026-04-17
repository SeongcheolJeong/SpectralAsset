# Catalog Gap Review

## Summary

The current generated baseline now exceeds the original `v1.0` count target through the first seven `P3` coverage-expansion batches:

- `18` traffic signs
- `5` traffic lights
- `49` roadway and roadside assets split as `8` road surfaces, `14` road markings, and `27` road-furniture assets

The remaining gaps are now mostly about traffic-light breadth, sign variation depth, and measurement quality rather than headline asset count.

## Coverage Snapshot by Family

| Family | Current Count | Planned Count | Count Status | Coverage Assessment | Highest-Priority Gaps | Roadmap Phase Pressure |
| --- | --- | --- | --- | --- | --- | --- |
| `traffic_sign` | `18` | `18` | met | broad baseline coverage across regulatory, warning, and information signs, and scenes now place separate backs and brackets for representative sign families | weathering levels, locale/text variants, additional wide or specialty sign assemblies, measured retroreflective behavior | `P3` for follow-up sign-depth variants, `P5` for measured sheeting |
| `traffic_light` | `5` | `5` | met | core signal-head catalog exists and scenes now place separate backplates, side-mount hardware, a mast hanger, junction/support cabinets, and utility-tail context as support detail | beacon-style units, flashing-warning heads, richer controller/support families beyond the current starter set, measured emitter spectra | `P3` for follow-up context breadth, `P5` for measured SPD |
| `road_surface` | `8` | part of the expanded post-`v1.0` roadway catalog | expanded | baseline paved urban surfaces now include patched asphalt, distressed concrete, asphalt-to-concrete transition, gutter-edge transition, and the original dry/wet/sidewalk starter set | gravel shoulders, construction plates, pothole-heavy distress, rural shoulder or unsealed transition variants | `P3` follow-up breadth when scenario scope expands again |
| `road_marking` | `14` | part of the expanded post-`v1.0` roadway catalog | expanded | directional arrows, edge lines, worn crossing and stop variants, a merge marking, and a raised-marker strip now exist alongside the baseline lane and stop geometry | yellow centerline families, lane-word markings, additional turn arrows, raised markers in yellow or bi-color variants, measured retroreflective response | `P3` follow-up breadth, `P5` for measured optics |
| `road_furniture` | `27` | part of the expanded post-`v1.0` roadway catalog | expanded | roadside, signal-support, and sign-assembly context now includes guardrails, bollards, delineators, cones, barriers, barricades, utility poles, signal backplates, side-mount and overhead brackets, a mast hanger, cabinet variants, a junction box, sign backs, and sign mounting brackets | utility service-detail variants, cabinet families beyond the current starter set, specialty sign assemblies, and more attachment-hardware depth | `P3` follow-up detail after signal and sign breadth |

## Key Findings

- `traffic_sign` meets the target count and now has separate sign-back and bracket assets in the baseline scenes, but it is still shallow in weathering and locale-specific variation.
- `traffic_light` has the right prefab count, and the scenes now have explicit backplates, mast-hanger context, side-mount brackets, cabinet variants, and a junction box instead of implying all support context through poles alone.
- `road_surface` is no longer limited to the clean dry/wet urban starter set: the baseline now has patched, distressed, and transition panels that make the current scenes less schematic.
- `road_marking` is no longer minimal: the generator now ships directional arrows, edge-line color variants, worn crossing and stop-line variants, a merge marking, and a raised-marker strip that make the scenes less schematic.
- `road_furniture` now covers much more of the roadside-support tail because the latest batch added utility poles, smaller cabinet/junction variants, and explicit sign/signal attachment hardware.
- `road_surface`, `road_marking`, and `road_furniture` are healthier now, so the next obvious expansion target shifts to traffic-light breadth and sign-variation depth.
- `traffic_light` still has room to grow, but the remaining gaps are now mostly signal-head variety rather than missing support-context basics.
- `traffic_sign` has better assembly depth now, so its remaining gaps are mostly variation-oriented rather than missing starter hardware.

## Priority Queue for Next Asset-Coverage Work

1. Return to `traffic_light` for beacon-style units, flashing-warning heads, and richer controller/support variants after the current support-context baseline settles.
2. Return to `traffic_sign` for localized text/font variants and weathering-depth variants once the broader roadside context is stable.
3. Return to `road_marking` for yellow centerline families, word legends, and additional raised-marker variants after the current secondary batch settles.
4. Return to `road_surface` for rural shoulders, stronger construction-zone distress, and unsealed transition variants after broader roadway context expands again.
5. Return to `road_furniture` for deeper utility service detail and specialty attachment hardware after higher-pressure signal and sign breadth is covered.

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
