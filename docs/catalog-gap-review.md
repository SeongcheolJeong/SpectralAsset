# Catalog Gap Review

## Summary

The current generated baseline now exceeds the original `v1.0` count target through the first two `P3` coverage-expansion batches:

- `18` traffic signs
- `5` traffic lights
- `23` roadway and roadside assets split as `4` road surfaces, `9` road markings, and `10` road-furniture assets

The remaining gaps are now mostly about traffic-light support geometry, sign assembly depth, road-surface variety, and measurement quality rather than headline asset count.

## Coverage Snapshot by Family

| Family | Current Count | Planned Count | Count Status | Coverage Assessment | Highest-Priority Gaps | Roadmap Phase Pressure |
| --- | --- | --- | --- | --- | --- | --- |
| `traffic_sign` | `18` | `18` | met | broad baseline coverage across regulatory, warning, and information signs | sign-back variants, mounting assemblies, weathering levels, locale/text variants, measured retroreflective behavior | `P3` for geometry/template depth, `P5` for measured sheeting |
| `traffic_light` | `5` | `5` | met | core signal-head catalog exists | backplates, mast-arm context, cabinet/support variants, beacon-style units, measured emitter spectra | `P3` for support geometry, `P5` for measured SPD |
| `road_surface` | `4` | part of `12` roadway assets | met | baseline paved urban surfaces are present | patched asphalt, distressed concrete, gravel or shoulder transitions, stronger state variation beyond dry/wet asphalt | `P3` when scenario breadth expands |
| `road_marking` | `9` | part of the expanded post-`v1.0` roadway catalog | expanded | directional arrows, edge lines, chevrons, and one worn lane variant now exist alongside the baseline lane and stop geometry | merge markings, yellow edge variants, worn stop/crosswalk variants, raised markers, measured retroreflective response | `P3` follow-up breadth, `P5` for measured optics |
| `road_furniture` | `10` | part of the expanded post-`v1.0` roadway catalog | expanded | first expansion batch now separates guardrail, bollards, delineators, cones, barriers, and barricades into standalone assets | utility poles, cabinet/support hardware, sign/signal attachment hardware, and more assembly-specific variants | `P3` follow-up expansion after markings and signal support geometry |

## Key Findings

- `traffic_sign` meets the target count and covers the intended Vienna-core starter set, but it is still shallow in assembly detail and aging variation.
- `traffic_light` has the right prefab count, yet most road-intersection context is still implied rather than modeled.
- `road_surface` supports the current four scenarios, but it will become thin quickly if construction, rural, or damaged-road scenes are added.
- `road_marking` is no longer minimal: the generator now ships directional arrows, edge lines, chevrons, and a worn lane variant that make the intersection scenes less schematic.
- `road_furniture` is no longer the thinnest family because the first expansion batch split multiple roadside objects into standalone assets.
- `traffic_light` is now the most obvious next expansion target because poles exist, but backplates, cabinets, and mast-arm-specific hardware are still missing.
- `traffic_sign` remains broad by count but shallow by assembly depth because sign backs, brackets, and mounting-hardware variants are still absent.

## Priority Queue for Next Asset-Coverage Work

1. Add `traffic_light` support geometry such as mast arms, backplates, cabinets, and intersection hardware.
2. Add `traffic_sign` assembly depth such as backs, brackets, and localized text/font variants.
3. Add `road_surface` distress and transition variants when scenario scope broadens beyond the current urban baseline.
4. Return to `road_marking` for merge markings, yellow edge variants, worn stop/crosswalk variants, and raised markers.
5. Return to `road_furniture` for attachment hardware, utility poles, and cabinet/support-tail variants after the higher-pressure gaps above are covered.

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
