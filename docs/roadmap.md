# Roadmap

## Phase Summary

| Phase | Focus | Primary Output | Depends On |
| --- | --- | --- | --- |
| `P0` | Repo and docs governance | stable docs set, git rules, baseline control | none |
| `P1` | Source collection and licensing hardening | reliable source ledger and usage policy | `P0` |
| `P2` | Spectral data and material fidelity | clearer measured/proxy separation and higher-fidelity curves | `P1` |
| `P3` | Geometry, templates, and asset coverage | broader asset catalog and asset acceptance rules | `P0`, `P2` |
| `P4` | Scenario, validation, and reproducibility | stable rebuild workflow and stronger validation gates | `P2`, `P3` |
| `P5` | Measurement replacement and release hardening | measured replacements, release checklist, tag policy | `P1`, `P2`, `P4` |

## Phase Goals

### `P0` Repo and Docs Governance

Goal:
- make the repository manageable as a long-running project
- define tracked artifacts, branch rules, commit rules, and the live backlog

Entry criteria:
- current baseline exists in the workspace

Exit criteria:
- docs set exists and is linked
- local git repo is initialized
- tracked-vs-ignored policy is documented

### `P1` Source Collection and Licensing Hardening

Goal:
- harden external-source handling and licensing records
- separate fetchable, blocked, redistributable, derived-only, and reference-only inputs

Entry criteria:
- `P0` governance docs are accepted

Exit criteria:
- 403 failures are either resolved or clearly documented with fallback handling
- source ledger classifications are reviewed
- license usage notes exist for critical source families

### `P2` Spectral Data and Material Fidelity

Goal:
- reduce ambiguity between measured truth and proxy curves
- prioritize replacement of the highest-value spectral gaps

Entry criteria:
- source policy and backlog are stable

Exit criteria:
- measured-vs-proxy asset policy is explicit
- replacement targets are prioritized
- acceptance rules exist for upgrading a proxy asset to measured status

### `P3` Geometry, Templates, and Asset Coverage

Goal:
- extend or refine the asset catalog without breaking naming or manifest contracts

Entry criteria:
- asset naming and manifest policy are stable

Exit criteria:
- asset additions follow the documented naming contract
- template and geometry coverage criteria are documented
- asset acceptance checklist exists

### `P4` Scenario, Validation, and Reproducibility

Goal:
- make rebuilds and validation trustworthy and reviewable

Entry criteria:
- material and geometry changes are under control

Exit criteria:
- validation expectations are documented per asset/scenario class
- timestamp churn is documented and triaged
- reproducibility policy is strong enough for milestone reviews

### `P5` Measurement Replacement and Release Hardening

Goal:
- replace key proxy data and prepare for formal milestone releases

Entry criteria:
- baseline governance, source policy, and validation policy are stable

Exit criteria:
- first release checklist is prepared
- tagging policy is documented
- measured replacement backlog is prioritized for release impact

## Dependencies Between Phases

- `P0` is the foundation for every later phase.
- `P1` must precede any serious licensing or source-expansion work in `P2` and `P5`.
- `P2` informs material fidelity for both `P3` asset work and `P4` validation work.
- `P3` and `P4` can overlap, but `P4` should not harden final validation gates until the catalog shape from `P3` is stable enough.
- `P5` depends on stable governance, source handling, and validation policy from earlier phases.

