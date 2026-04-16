# Catalog Gap Review

## Summary

The current generated baseline meets the planned `v1.0` count targets:

- `18` traffic signs
- `5` traffic lights
- `12` roadway and roadside assets split as `4` road surfaces, `4` road markings, and `4` road-furniture assets

The remaining gaps are mostly about coverage depth, support geometry, and measurement quality rather than headline asset count.

## Coverage Snapshot by Family

| Family | Current Count | Planned Count | Count Status | Coverage Assessment | Highest-Priority Gaps | Roadmap Phase Pressure |
| --- | --- | --- | --- | --- | --- | --- |
| `traffic_sign` | `18` | `18` | met | broad baseline coverage across regulatory, warning, and information signs | sign-back variants, mounting assemblies, weathering levels, locale/text variants, measured retroreflective behavior | `P3` for geometry/template depth, `P5` for measured sheeting |
| `traffic_light` | `5` | `5` | met | core signal-head catalog exists | backplates, mast-arm context, cabinet/support variants, beacon-style units, measured emitter spectra | `P3` for support geometry, `P5` for measured SPD |
| `road_surface` | `4` | part of `12` roadway assets | met | baseline paved urban surfaces are present | patched asphalt, distressed concrete, gravel or shoulder transitions, stronger state variation beyond dry/wet asphalt | `P3` when scenario breadth expands |
| `road_marking` | `4` | part of `12` roadway assets | met | baseline lane and stop geometry is present | arrows, chevrons, merge/gore markings, edge lines, worn variants, raised markers, measured retroreflective response | `P3` for geometry breadth, `P5` for measured optics |
| `road_furniture` | `4` | part of `12` roadway assets | met | weakest family by depth; current count is helped by treating `road.curb` as furniture-adjacent coverage | cones, barriers, delineators, bollards separated from guardrail, posts, utility poles, signal/sign attachment hardware | `P3` immediate expansion priority |

## Key Findings

- `traffic_sign` meets the target count and covers the intended Vienna-core starter set, but it is still shallow in assembly detail and aging variation.
- `traffic_light` has the right prefab count, yet most road-intersection context is still implied rather than modeled.
- `road_surface` supports the current four scenarios, but it will become thin quickly if construction, rural, or damaged-road scenes are added.
- `road_marking` is adequate for lane-following and stop-line scenes, but it lacks the directional and worn variants needed for denser intersection layouts.
- `road_furniture` is the most obvious expansion target because the family currently compresses several distinct roadside objects into a small set.

## Priority Queue for Next Asset-Coverage Work

1. Expand `road_furniture` first with separated bollards, barriers, delineators, and attachment hardware.
2. Expand `road_marking` next with directional arrows, chevrons, edge lines, and worn variants.
3. Add `traffic_light` support geometry such as mast arms, backplates, and intersection hardware.
4. Add `traffic_sign` assembly depth such as backs, brackets, and localized text/font variants.
5. Add `road_surface` distress and transition variants when scenario scope broadens beyond the current urban baseline.

## Phase Mapping

| Roadmap Phase | Recommended Coverage Work |
| --- | --- |
| `P3` | geometry and template additions for `road_furniture`, `road_marking`, `traffic_light`, and `traffic_sign` support variants |
| `P4` | scenario and validation-scene updates that exercise the new coverage rather than only adding counts |
| `P5` | measured upgrades for retroreflective and emissive behavior once the broader geometry catalog is stable |

## Scope Guardrails

- The current catalog should still be treated as a valid `v1.0` baseline because the planned family counts are met.
- Future count expansion should not break the naming and manifest contracts in [asset-spec.md](asset-spec.md).
- Coverage reviews should distinguish count completeness from fidelity completeness. The current pack is count-complete, but not depth-complete.
