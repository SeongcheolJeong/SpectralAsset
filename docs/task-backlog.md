# Task Backlog

## Status Legend

- `planned`: scoped and ready, but not started
- `in_progress`: currently being worked
- `blocked`: waiting on an external dependency or unresolved issue
- `done`: completed and accepted into the active baseline

## Priority Legend

- `P0`: repository safety, governance, or blocking execution work
- `P1`: important quality or delivery work that should follow soon
- `P2`: valuable follow-up work that can wait until the higher-priority backlog is stable

## Backlog by Phase

### `P0` Repo and Docs Governance

| Task ID | Phase | Priority | Status | Title | Deliverable | Depends On | Definition of Done |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `P0-T001` | `P0` | `P0` | `done` | Initialize local git repo | local `main` branch with baseline commit | none | repository is initialized locally, baseline workspace is committed, and `node_modules/` is not tracked |
| `P0-T002` | `P0` | `P0` | `done` | Create docs index and roadmap | `docs/README.md` and `docs/roadmap.md` | `P0-T001` | both files exist and describe ownership, phases, and current truth sources |
| `P0-T003` | `P0` | `P0` | `done` | Add README links to management docs | root `README.md` management-doc section | `P0-T002` | root README links to docs index, roadmap, and task backlog |
| `P0-T004` | `P0` | `P0` | `done` | Define artifact tracking policy | `docs/git-workflow.md` tracked-vs-ignored section | `P0-T001` | tracked folders and ignored folders are explicit and match `.gitignore` policy |
| `P0-T005` | `P0` | `P0` | `done` | Document branch and commit conventions | `docs/git-workflow.md` branch and commit sections | `P0-T001` | branch format `codex/<area>-<slug>` and commit prefixes are documented |

### `P1` Source Collection and Licensing Hardening

| Task ID | Phase | Priority | Status | Title | Deliverable | Depends On | Definition of Done |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `P1-T001` | `P1` | `P1` | `done` | Resolve or document `403` source-fetch failures | updated source policy and fallback notes | `P0-T002` | each blocked source is either fetchable or documented with reason, impact, and fallback |
| `P1-T002` | `P1` | `P1` | `done` | Review source classifications and license usage | source-policy notes in docs | `P1-T001` | `redistributable`, `derived-only`, and `reference-only` usage is reviewed for current sources |
| `P1-T003` | `P1` | `P2` | `done` | Prepare first release checklist | release checklist section or file | `P0-T005`, `P4-T002` | checklist covers source, validation, known gaps, and tag readiness |
| `P1-T004` | `P1` | `P1` | `done` | Freeze selected local USGS subset into tracked raw inputs | tracked `raw/sources/usgs_splib07_selected/` subset and source-ledger entries | `P1-T002` | selected USGS files are copied into tracked `raw/`, the full local mirror stays ignored, and the ledger records local-path provenance |

### `P2` Spectral Data and Material Fidelity

| Task ID | Phase | Priority | Status | Title | Deliverable | Depends On | Definition of Done |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `P2-T001` | `P2` | `P1` | `done` | Address generator timestamp churn for tracked outputs | reproducibility policy and follow-up implementation task | `P0-T004` | timestamp-only diffs are documented, detectable, and scheduled for implementation |
| `P2-T002` | `P2` | `P1` | `done` | Split proxy-vs-measured spectral assets clearly in docs | updated asset policy and overview notes | `P0-T002` | docs make the proxy/measured boundary explicit for materials and backlog items |
| `P2-T003` | `P2` | `P2` | `done` | Prioritize measured replacement backlog | ranked measurement plan | `P1-T002`, `P2-T002` | automotive SRF, signal SPD, wet-road BRDF, and retroreflective BRDF are ranked by impact and difficulty |
| `P2-T004` | `P2` | `P1` | `done` | Promote dry road and support material baselines from USGS subset | measured dry asphalt, concrete, and galvanized material baselines | `P1-T004` | selected USGS samples drive `mat_asphalt_dry`, `mat_concrete`, and `mat_metal_galvanized` with measured provenance |
| `P2-T005` | `P2` | `P1` | `done` | Add generic RGB+NIR camera profile and scenario binding | camera profile schema, generated profile, and scenario references | `P0-T002`, `P2-T003` | one generic camera profile exists, scenarios reference it, and validation/reporting cover camera profiles |

### `P3` Geometry, Templates, and Asset Coverage

| Task ID | Phase | Priority | Status | Title | Deliverable | Depends On | Definition of Done |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `P3-T001` | `P3` | `P1` | `done` | Define acceptance criteria for asset additions | acceptance rules in `docs/asset-spec.md` | `P0-T002` | new asset additions have naming, manifest, validation, and provenance criteria |
| `P3-T002` | `P3` | `P2` | `done` | Review catalog coverage against roadmap phases | gap summary by asset family | `P3-T001` | missing or weak asset families are documented by priority |

### `P4` Scenario, Validation, and Reproducibility

| Task ID | Phase | Priority | Status | Title | Deliverable | Depends On | Definition of Done |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `P4-T001` | `P4` | `P1` | `done` | Harden rebuild review policy for generated outputs | rebuild review checklist in git workflow | `P2-T001` | semantic vs timestamp-only rebuild changes can be reviewed consistently |
| `P4-T002` | `P4` | `P1` | `done` | Define milestone validation checklist | documented milestone validation gates | `P3-T001` | milestone review includes schema, export, visual, semantic, and backlog checks |

### `P5` Measurement Replacement and Release Hardening

| Task ID | Phase | Priority | Status | Title | Deliverable | Depends On | Definition of Done |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `P5-T001` | `P5` | `P2` | `done` | Document release/tag policy for first formal milestone | tag and release section in git workflow | `P1-T003`, `P4-T002` | first release rules are documented without assuming a remote host |
| `P5-T002` | `P5` | `P1` | `done` | Implement measured automotive SRF intake and activation gate | generator/schema support for frozen measured camera SRF input | `P2-T005`, `P2-T003` | local measured camera input can be frozen into tracked `raw/`, measured camera profiles validate cleanly, and scenarios only activate the measured profile when that source exists |
| `P5-T003` | `P5` | `P1` | `blocked` | Freeze a real measured automotive SRF source and promote it to active use | frozen measured raw source plus active measured camera profile | `P5-T002` | a real measured automotive SRF dataset is present, frozen in `raw/`, and becomes the active scenario-bound camera profile |
| `P5-T004` | `P5` | `P1` | `done` | Implement measured traffic-signal/headlamp SPD intake and activation gate | generator support for frozen measured emitter SPD input | `P2-T003` | local measured emitter input can be frozen into tracked `raw/`, measured traffic-signal SPDs validate cleanly, and active signal curves only switch when that source exists |
| `P5-T005` | `P5` | `P1` | `blocked` | Freeze a real measured traffic-signal/headlamp SPD source and promote it to active use | frozen measured emitter raw source plus active measured signal curves | `P5-T004` | a real measured emitter SPD dataset is present, frozen in `raw/`, and becomes the active source for vehicle/protected-turn signal profiles |
| `P5-T006` | `P5` | `P1` | `done` | Implement measured retroreflective sheeting intake and activation gate | generator support for frozen measured retroreflective input | `P2-T003` | local measured retroreflective input can be frozen into tracked `raw/`, measured gain curves validate cleanly, and the shared retroreflective modifier only switches when that source exists |
| `P5-T007` | `P5` | `P1` | `blocked` | Freeze a real measured retroreflective source and promote it to the current shared modifier path | frozen measured retroreflective raw source plus active measured modifier curve | `P5-T006` | a real measured retroreflective dataset is present, frozen in `raw/`, and becomes the active shared retroreflective gain curve while the full BRDF backlog remains explicitly open |

## Blocked Items

- `P5-T003` is blocked until a real measured automotive camera SRF dataset is provided in the local measured-intake format.
- `P5-T005` is blocked until a real measured traffic-signal/headlamp SPD dataset is provided in the local measured-intake format.
- `P5-T007` is blocked until a real measured retroreflective sheeting dataset is provided in the local measured-intake format.
- External `403` source pages still exist, but they are now documented with fallback handling in `docs/source-policy.md`.

## Deferred Items

- wet-road spectral BRDF acquisition, ranked fourth in [measurement-priorities.md](measurement-priorities.md)
- measured promotion of sign-sheeting and road-marking materials remains deferred because the frozen USGS plastics and pigments are reference-only in this repository phase
- asset-family expansion beyond the current `v1.0` count-complete baseline, prioritized in [catalog-gap-review.md](catalog-gap-review.md)
