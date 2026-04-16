# Source Policy

## Purpose

This file defines how external sources are handled in this repository: what can be frozen locally, what can be redistributed, what can only be used as a reference, and how blocked fetches are documented instead of silently dropped.

## Source Classifications

### `redistributable`

Use when the raw source can be frozen in the repository and retained as part of the tracked source ledger.

Current examples:

- `cie_d65_csv`
- `cie_d65_metadata`

Operational rule:

- keep the raw file, checksum, and source metadata in `raw/sources/<source_id>/`

### `derived-only`

Use when the source can be consumed for project work, but raw redistribution should not be assumed from the generator alone.

Current examples:

- `astm_g173_zip`

Operational rule:

- keep the local raw copy and checksum for reproducibility
- do not assume public redistribution rights for the raw source outside this repository context without checking upstream terms again

### `reference-only`

Use when the source is primarily for provenance, documentation, or human review, not for redistribution-driven asset packaging.

Current examples:

- `aeronet_quality_assurance_pdf`
- `libradtran_home`
- `osm_traffic_sign_wiki`
- `openusd_faq`
- `gltf_spec`
- `polyhaven_license`
- `ambientcg_license`
- `usgs_spectral_library_page`
- `ecostress_spectral_library_page`
- `unece_road_signs_page`
- `mapillary_sign_help`
- `mapillary_download_help`

Operational rule:

- store either the fetched page or the failure record in `raw/sources/<source_id>/`
- do not treat a reference-only page as proof that its underlying dataset can be redistributed

## Current Source Inventory

| Source ID | Classification | Current Status | Current Use | Policy Note |
| --- | --- | --- | --- | --- |
| `cie_d65_csv` | `redistributable` | `downloaded` | standard illuminant input | tracked raw file plus checksum |
| `cie_d65_metadata` | `redistributable` | `downloaded` | metadata and DOI provenance | tracked raw file plus checksum |
| `astm_g173_zip` | `derived-only` | `downloaded` | solar spectrum input | keep raw locally, do not assume unrestricted redistribution outside repo context |
| `aeronet_quality_assurance_pdf` | `reference-only` | `downloaded` | atmosphere provenance | reference/supporting documentation only |
| `libradtran_home` | `reference-only` | `downloaded` | RT model provenance | documentation reference only |
| `osm_traffic_sign_wiki` | `reference-only` | `downloaded` | sign taxonomy reference | not a shipped asset source |
| `mapillary_sign_help` | `reference-only` | `fetch_failed` | sign-taxonomy help reference | blocked by remote `403`, fallback documented below |
| `mapillary_download_help` | `reference-only` | `fetch_failed` | map-download help reference | blocked by remote `403`, fallback documented below |
| `openusd_faq` | `reference-only` | `downloaded` | USD format reference | documentation reference only |
| `gltf_spec` | `reference-only` | `downloaded` | glTF format reference | specification reference only |
| `polyhaven_license` | `reference-only` | `downloaded` | optional bootstrap-license reference | reference only until assets are actually imported |
| `ambientcg_license` | `reference-only` | `downloaded` | optional bootstrap-license reference | reference only until assets are actually imported |
| `usgs_spectral_library_page` | `reference-only` | `fetch_failed` | landing-page provenance for spectral library | blocked by remote `403`, fallback documented below |
| `ecostress_spectral_library_page` | `reference-only` | `downloaded` | landing-page provenance | reference page only |
| `unece_road_signs_page` | `reference-only` | `fetch_failed` | generic international sign-reference page | blocked by remote `403`, fallback documented below |

## Blocked `403` Sources and Fallback Handling

### `mapillary_sign_help`

- Failure mode: automated `curl` fetch returns `403`
- Impact: low to medium
  - this is a help/reference page, not a required runtime asset input
- Current fallback:
  - keep the `source.json` failure record in `raw/sources/mapillary_sign_help/`
  - rely on the OSM traffic-sign wiki plus existing asset taxonomy for the current baseline
  - if the page becomes necessary later, retrieve it manually in a browser session and freeze the manually exported HTML or notes

### `mapillary_download_help`

- Failure mode: automated `curl` fetch returns `403`
- Impact: low
  - this page documents Mapillary download workflow, but the current baseline does not depend on a shipped Mapillary ingest
- Current fallback:
  - keep the failure record in `raw/sources/mapillary_download_help/`
  - document manual browser retrieval as the fallback path if Mapillary-driven enrichment becomes active later

### `usgs_spectral_library_page`

- Failure mode: automated `curl` fetch returns `403`
- Impact: medium
  - the project cites USGS as an important spectral-library family, but the blocked page is a landing page rather than the generated canonical curve source in the current baseline
- Current fallback:
  - keep the failure record in `raw/sources/usgs_spectral_library_page/`
  - use the research report and future manual retrieval to refresh provenance if needed
  - do not claim the landing page was successfully frozen when it was not

### `unece_road_signs_page`

- Failure mode: automated `curl` fetch returns `403`
- Impact: low to medium
  - the current sign pack already uses a generic international shape/taxonomy baseline and does not depend on shipping UNECE source content
- Current fallback:
  - keep the failure record in `raw/sources/unece_road_signs_page/`
  - use documented generic international conventions plus existing repo catalog until a manual official capture is added

## Operational Rules for New Sources

- Every new source must have a `source.json` record with `id`, `url`, `classification`, `status`, and fetch timestamp.
- Successful fetches must include checksum and file size.
- Failed fetches must stay in the ledger with the failure reason instead of being removed.
- A source must not be promoted from `reference-only` to `redistributable` or `derived-only` by assumption; that change requires an explicit term review.
- If a source affects shipped generated outputs, the related policy note must be documented before the output change is merged.

## Current Decision

The blocked `403` sources are documented and no longer treated as silent failures. For the current baseline:

- they do not block the tracked generated asset pack
- they remain provenance gaps to revisit later
- their fallback path is manual capture or alternate official access when those references become necessary for an actual build step

