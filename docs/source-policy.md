# Source Policy

## Purpose

This file defines how external sources are handled in this repository: what can be frozen locally, what can be redistributed, what can only be used as a reference, and how blocked fetches are documented instead of silently dropped.

## Source Classifications

### `redistributable`

Use when the raw source can be frozen in the repository and retained as part of the tracked source ledger.

Current examples:

- `cie_d65_csv`
- `cie_d65_metadata`
- selected `usgs_splib07` local subset entries under `raw/sources/usgs_splib07_selected/`

Operational rule:

- keep the raw file, checksum, and source metadata in `raw/sources/<source_id>/`
- local-path subsets must also record the original local source path and copy timestamp

## Source Origins

Ledger entries may originate from either:

- `url`: downloaded from a remote source into `raw/sources/<source_id>/`
- `local_path`: copied from a local source root into tracked `raw/`

Current local-path usage:

- `usgs_splib07/` is treated as an ignored local source root
- only the selected subset frozen into `raw/sources/usgs_splib07_selected/` is tracked
- `automotive_sensor_srf_input/` may be used as an ignored local intake root for measured camera SRF data, but only the frozen copy in `raw/sources/automotive_sensor_srf_measured/` is tracked
- `traffic_signal_headlamp_spd_input/` may be used as an ignored local intake root for measured emitter SPD data, but only the frozen copy in `raw/sources/traffic_signal_headlamp_spd_measured/` is tracked

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
- `onsemi_mt9m034_pdf`
- `osram_lr_q976_01_pdf`
- `osram_ly_q976_01_pdf`
- `osram_ltrb_rasf_01_pdf`
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
| `basler_color_emva_knowledge` | `reference-only` | `downloaded` | camera-profile vendor-derived context | public documentation used for generic camera-profile derivation |
| `sony_imx900_product_page` | `reference-only` | `downloaded` | camera-profile vendor-derived context | public Sony sensor page for NIR-sensitive profile assumptions |
| `sony_isx016_pdf` | `reference-only` | `downloaded` | camera-profile vendor-derived context | official Sony PDF with NIR sensitivity claim |
| `onsemi_mt9m034_pdf` | `reference-only` | `copied_from_local` | camera-profile donor QE reference | official ON Semiconductor MT9M034 datasheet frozen from a local copy because automated GET from the public URL returns `403` |
| `osram_lr_q976_01_pdf` | `reference-only` | `downloaded` | vehicle-signal red SPD vendor-derived fit | official ams-OSRAM red LED datasheet used for fitted signal SPD |
| `osram_ly_q976_01_pdf` | `reference-only` | `downloaded` | vehicle-signal yellow SPD vendor-derived fit | official ams-OSRAM yellow LED datasheet used for fitted signal SPD |
| `osram_ltrb_rasf_01_pdf` | `reference-only` | `downloaded` | vehicle-signal green SPD vendor-derived fit | official ams-OSRAM true-green LED datasheet used for fitted signal SPD |
| `usgs_asdfr_wavelengths_2151` | `redistributable` | `copied_from_local` | wavelength basis for selected USGS materials | tracked selected local subset entry |
| `usgs_gds376_asphalt_road_old` | `redistributable` | `copied_from_local` | measured dry asphalt baseline | actively bound to `mat_asphalt_dry` |
| `usgs_gds375_concrete_road` | `redistributable` | `copied_from_local` | measured concrete baseline | actively bound to `mat_concrete` |
| `usgs_gds334_galvanized_sheet_metal` | `redistributable` | `copied_from_local` | measured galvanized metal baseline | actively bound to `mat_metal_galvanized` |
| `usgs_gds333_painted_aluminum` | `redistributable` | `copied_from_local` | color/material reference prior | reference-only, not actively bound |
| `usgs_gds338_pvc_white` | `redistributable` | `copied_from_local` | color/material reference prior | reference-only, not actively bound |
| `usgs_gds398_vinyl_red_toy` | `redistributable` | `copied_from_local` | color/material reference prior | reference-only, not actively bound |
| `usgs_gds344_pipe_blue` | `redistributable` | `copied_from_local` | color/material reference prior | reference-only, not actively bound |
| `usgs_gds382_pete_black` | `redistributable` | `copied_from_local` | color/material reference prior | reference-only, not actively bound |
| `usgs_spectralon99_white_ref` | `redistributable` | `copied_from_local` | reflectance reference prior | reference-only, not actively bound |

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

### `onsemi_mt9m034_pdf`

- Failure mode: automated `curl` GET returns `403`, even though the official URL is valid for `HEAD`
- Impact: low to medium
  - this source anchors the donor QE provenance for `camera_reference_rgb_nir_v2`, but the repository now has a working local-copy fallback
- Current fallback:
  - keep the official URL in the source ledger for provenance
  - copy the local file `MT9M034-D.PDF` into `raw/sources/onsemi_mt9m034_pdf/mt9m034-d.pdf`
  - keep the `MT9M034` donor QE control points explicit in `scripts/build_asset_pack.py`
  - continue treating direct automated vendor download as blocked unless the official GET path becomes accessible later

## Operational Rules for New Sources

- Every new source must have a `source.json` record with `id`, `url`, `classification`, `status`, and fetch timestamp.
- Local-path sources may use `copied_from` and `copied_at` instead of `url` and `fetched_at`, but they must still carry status, checksum, and classification.
- The optional measured automotive SRF intake path must freeze `metadata.json` and `srf.csv` into `raw/sources/automotive_sensor_srf_measured/` before the generator may activate a measured camera profile.
- The optional measured emitter SPD intake path must freeze `metadata.json` and `spd.csv` into `raw/sources/traffic_signal_headlamp_spd_measured/` before the generator may activate measured signal curves.
- Successful fetches must include checksum and file size.
- Failed fetches must stay in the ledger with the failure reason instead of being removed.
- A source must not be promoted from `reference-only` to `redistributable` or `derived-only` by assumption; that change requires an explicit term review.
- If a source affects shipped generated outputs, the related policy note must be documented before the output change is merged.

## Current Decision

The blocked `403` sources are documented and no longer treated as silent failures. For the current baseline:

- they do not block the tracked generated asset pack
- they remain provenance gaps to revisit later
- their fallback path is manual capture or alternate official access when those references become necessary for an actual build step
