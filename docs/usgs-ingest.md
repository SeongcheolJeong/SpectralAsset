# USGS Ingest

## Purpose

This document defines how the local USGS Spectral Library Version 7 mirror is used in this repository without turning the full local mirror into a tracked dependency.

## Local Source Root

- default local source root: `usgs_splib07/`
- optional override: `USGS_SPLIB07_ROOT`
- the full local mirror is intentionally ignored by git
- only the selected frozen subset under `raw/sources/usgs_splib07_selected/` is tracked

## Why the Full Library Is Not Tracked

- the local mirror is approximately `6.7G` and is too large to treat as routine tracked repo input
- the build only needs a small subset for the current measured material bindings
- tracking only the selected subset keeps rebuilds reproducible without forcing every checkout to carry the full mirror

## Active-Binding Subset

These files are copied into tracked `raw/` and actively bound into current generated materials.

### Wavelength basis

- `ASCIIdata/ASCIIdata_splib07b/splib07b_Wavelengths_ASDFR_0.35-2.5microns_2151ch.txt`

### Dry asphalt

- `ASCIIdata/ASCIIdata_splib07b/ChapterA_ArtificialMaterials/splib07b_Asphalt_GDS376_Blck_Road_old_ASDFRa_AREF.txt`
- `HTMLmetadata/Asphalt_GDS376_Blck_Road_old_ASDFRa_AREF.html`

### Concrete

- `ASCIIdata/ASCIIdata_splib07b/ChapterA_ArtificialMaterials/splib07b_Concrete_GDS375_Lt_Gry_Road_ASDFRa_AREF.txt`
- `HTMLmetadata/Concrete_GDS375_Lt_Gry_Road_ASDFRa_AREF.html`

### Galvanized sheet metal

- `ASCIIdata/ASCIIdata_splib07b/ChapterA_ArtificialMaterials/splib07b_GalvanizedSheetMetal_GDS334_ASDFRa_AREF.txt`
- `HTMLmetadata/GalvanizedSheetMetal_GDS334_ASDFRa_AREF.html`

## Reference-Only Subset

These files are frozen for provenance and color/material priors, but they are not promoted to measured replacements in this phase.

- `splib07b_Painted_Aluminum_GDS333_LgGr_ASDFRa_AREF.txt`
- `Painted_Aluminum_GDS333_LgGr_ASDFRa_AREF.html`
- `splib07b_Plastic_PVC_GDS338_White_ASDFRa_AREF.txt`
- `Plastic_PVC_GDS338_White_ASDFRa_AREF.html`
- `splib07b_Plastic_Vinyl_GDS398_Red_Toy_ASDFRa_AREF.txt`
- `Plastic_Vinyl_GDS398_Red_Toy_ASDFRa_AREF.html`
- `splib07b_Plastic_Pipe_GDS344_Blue_ASDFRa_AREF.txt`
- `Plastic_Pipe_GDS344_Blue_ASDFRa_AREF.html`
- `splib07b_Plastic_PETE_GDS382_Black_ASDFRa_AREF.txt`
- `Plastic_PETE_GDS382_Black_ASDFRa_AREF.html`
- `splib07b_Spectralon99WhiteRef_LSPHERE_ASDFRa_AREF.txt`
- `Spectralon99WhiteRef_LSPHERE_ASDFRa_AREF.html`

## Active Binding Rules

- `mat_asphalt_dry` binds to the frozen GDS376 road asphalt sample
- `mat_concrete` binds to the frozen GDS375 concrete road sample
- `mat_metal_galvanized` binds to the frozen GDS334 galvanized sheet-metal sample
- `mat_asphalt_wet` is a measured-derived material built from the measured dry asphalt baseline plus the tracked wet modifier

## Safeguards

The frozen USGS subset must not be over-claimed.

- USGS plastics and pigments are useful as color/material priors, but they are not traffic-sign sheeting
- USGS white plastic and Spectralon are not road-marking paint replacements
- USGS artificial materials do not solve retroreflective BRDF or wet-road BRDF
- any future promotion from reference-only to active binding must be documented before the change is merged

## Implementation Notes

- selected files are copied into `raw/sources/usgs_splib07_selected/`
- `raw/sources/usgs_splib07_selected/index.json` is the tracked selection manifest
- `raw/source_ledger.json` records the selected subset with `origin_type: local_path`
- canonical source-specific curves use the `src_usgs_*` naming pattern
