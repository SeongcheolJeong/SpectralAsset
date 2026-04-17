# Catalog Gap Review

## Summary

The current generated baseline now exceeds the original `v1.0` count target through the first five `P3` coverage-expansion batches:

- `18` traffic signs
- `5` traffic lights
- `38` roadway and roadside assets split as `8` road surfaces, `9` road markings, and `21` road-furniture assets

The remaining gaps are now mostly about secondary marking/furniture variants, locale or aging sign variants, and measurement quality rather than headline asset count.

## Coverage Snapshot by Family

| Family | Current Count | Planned Count | Count Status | Coverage Assessment | Highest-Priority Gaps | Roadmap Phase Pressure |
| --- | --- | --- | --- | --- | --- | --- |
| `traffic_sign` | `18` | `18` | met | broad baseline coverage across regulatory, warning, and information signs, and scenes now place separate backs and brackets for representative sign families | weathering levels, locale/text variants, additional wide or specialty sign assemblies, measured retroreflective behavior | `P3` for follow-up sign-depth variants, `P5` for measured sheeting |
| `traffic_light` | `5` | `5` | met | core signal-head catalog exists and scenes now place separate backplates, a mast hanger, and a controller cabinet as support context | beacon-style units, cabinet/support variants beyond the current starter set, measured emitter spectra | `P3` for follow-up context breadth, `P5` for measured SPD |
| `road_surface` | `8` | part of the expanded post-`v1.0` roadway catalog | expanded | baseline paved urban surfaces now include patched asphalt, distressed concrete, asphalt-to-concrete transition, gutter-edge transition, and the original dry/wet/sidewalk starter set | gravel shoulders, construction plates, pothole-heavy distress, rural shoulder or unsealed transition variants | `P3` follow-up breadth when scenario scope expands again |
| `road_marking` | `9` | part of the expanded post-`v1.0` roadway catalog | expanded | directional arrows, edge lines, chevrons, and one worn lane variant now exist alongside the baseline lane and stop geometry | merge markings, yellow edge variants, worn stop/crosswalk variants, raised markers, measured retroreflective response | `P3` follow-up breadth, `P5` for measured optics |
| `road_furniture` | `21` | part of the expanded post-`v1.0` roadway catalog | expanded | roadside, signal-support, and sign-assembly context now includes guardrails, bollards, delineators, cones, barriers, barricades, signal backplates, a mast hanger, a controller cabinet, sign backs, and sign mounting brackets | utility poles, cabinet variants, specialty sign assemblies, and more attachment-hardware variants | `P3` follow-up expansion after road-surface breadth |

## Key Findings

- `traffic_sign` meets the target count and now has separate sign-back and bracket assets in the baseline scenes, but it is still shallow in weathering and locale-specific variation.
- `traffic_light` has the right prefab count, and the scenes now have explicit backplates, mast-hanger context, and a controller cabinet instead of implying all support context through poles alone.
- `road_surface` is no longer limited to the clean dry/wet urban starter set: the baseline now has patched, distressed, and transition panels that make the current scenes less schematic.
- `road_marking` is no longer minimal: the generator now ships directional arrows, edge lines, chevrons, and a worn lane variant that make the intersection scenes less schematic.
- `road_furniture` is no longer the thinnest family because the first expansion batch split multiple roadside objects into standalone assets.
- `road_surface` is healthier now, so the next obvious expansion target shifts back to secondary marking breadth and roadside-tail variants.
- `traffic_light` still has room to grow, but the highest-pressure missing support-context items are no longer missing from the baseline.
- `traffic_sign` has better assembly depth now, so its remaining gaps are mostly variation-oriented rather than missing starter hardware.

## Priority Queue for Next Asset-Coverage Work

1. Return to `road_marking` for merge markings, yellow edge variants, worn stop/crosswalk variants, and raised markers.
2. Return to `road_furniture` for utility poles, cabinet/support-tail variants, and specialty sign/signal attachment hardware.
3. Return to `traffic_sign` for localized text/font variants and weathering-depth variants once the broader roadside context is stable.
4. Return to `traffic_light` for beacon-style units and richer controller/support variants after the higher-pressure marking and roadside gaps are covered.
5. Return to `road_surface` for rural shoulders, stronger construction-zone distress, and unsealed transition variants after broader roadway context expands again.

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
