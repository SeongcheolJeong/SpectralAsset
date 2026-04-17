# Wet-Road BRDF Intake

## Purpose

This document explains the optional local input path for measured wet-road spectral data.

The repository now supports freezing a measured wet-road source into tracked `raw/` inputs, but the current shipped baseline does not yet include such a frozen source.

That means:

- the intake path exists
- the active wet asphalt material is still the measured-derived fallback built from USGS dry asphalt plus tracked wet modifiers
- the current repository contract can activate measured wet reflectance and an optional measured wet overlay curve
- the full angle-aware `wet_road_spectral_brdf` backlog item remains open

## Local Input Root

Default ignored local input root:

- `wet_road_spectral_brdf_input/`

Optional override:

- `WET_ROAD_SPECTRAL_BRDF_ROOT`

The local input root is intentionally ignored by git.

When valid input files are present, the generator copies them into:

- `raw/sources/wet_road_spectral_brdf_measured/`

That frozen copy becomes the tracked source of truth.

## Required Input Files

Required:

- `metadata.json`
- `brdf.csv`

Optional:

- `report.pdf`

## Required CSV Structure

The generator expects a header row with either:

- `wavelength_nm`

or:

- `wavelength_um`

Supported columns:

- `wet_reflectance`
- `wet_overlay_transmittance`

`wet_reflectance` is required.
`wet_overlay_transmittance` is optional.

Minimal example:

```csv
wavelength_nm,wet_reflectance,wet_overlay_transmittance
400,0.03,0.90
450,0.04,0.93
500,0.05,0.95
600,0.06,0.97
700,0.07,0.97
800,0.08,0.96
900,0.09,0.95
1100,0.10,0.91
```

## Recommended Metadata Fields

- `classification`
- `license_summary`
- `report_id`
- `report_date`
- `wavelength_unit`
- `response_scale`
- `substrate_id`
- `dry_reference`
- `water_condition`
- `roughness_note`
- `measurement_geometry`
- `calibration_reference`
- `film_thickness_mm`
- `specular_boost`
- `roughness_factor`
- `measurement_notes`
- `channel_columns`

Example:

```json
{
  "classification": "derived-only",
  "license_summary": "Local measured wet-road data provided for in-repo use.",
  "report_id": "WET-2026-001",
  "report_date": "2026-04-17",
  "wavelength_unit": "nm",
  "response_scale": "unit_fraction",
  "substrate_id": "urban asphalt lane",
  "dry_reference": "USGS GDS376 dry asphalt baseline",
  "water_condition": "uniform thin water film",
  "roughness_note": "nominal road surface roughness",
  "measurement_geometry": "fixed capture geometry",
  "calibration_reference": "calibrated wet-surface spectral capture",
  "film_thickness_mm": 0.5,
  "specular_boost": 1.8,
  "roughness_factor": 0.24,
  "measurement_notes": "Measured wet reflectance plus optional overlay transmittance.",
  "channel_columns": {
    "wet_reflectance": "wet_reflectance",
    "wet_overlay_transmittance": "wet_overlay_transmittance"
  }
}
```

## Generator Behavior

When the local input is present and valid, the generator:

1. copies the source files into `raw/sources/wet_road_spectral_brdf_measured/`
2. records a source-ledger entry with local-path provenance
3. resamples the measured wet-road curves onto the repo master grid
4. writes source-specific measured wet-road spectra into `canonical/spectra/`
5. activates measured wet reflectance for `mat_asphalt_wet`
6. activates measured wet overlay transmittance too when that optional curve is present
7. updates the current wet material roughness/specular metadata from the frozen input metadata

When the local input is absent:

- no measured wet-road source is frozen
- no measured wet-road curves are generated
- the measured-derived wet-asphalt fallback remains active

## Activation Gate

The measured wet-road path is only activated if the frozen input:

- covers at least `400-1100 nm`
- includes `wet_reflectance`
- has strictly increasing wavelength values
- passes material validation through the existing generated-material path

Selection behavior:

- measured `wet_reflectance` replaces the current measured-derived wet reflectance
- measured `wet_overlay_transmittance` is optional; if absent, the tracked proxy overlay remains active

## Important Limitation

This intake does **not** solve the full `wet_road_spectral_brdf` backlog item.

The current repository material contract still uses:

- a single wet reflectance curve
- an optional wet overlay transmittance curve
- scalar roughness/specular metadata

It does not yet model:

- angle-dependent wet-road BRDF
- specular lobe variation across geometry
- repeated drying-state captures
- a full goniometric wet-surface contract

So this intake improves the current simplified wet-road path, but it is not a full measured BRDF replacement.

## Current Status

Current repo truth:

- intake support exists
- no frozen measured wet-road source is present in the shipped baseline
- `mat_asphalt_wet` still uses the measured-derived fallback path
- `wet_road_spectral_brdf` remains `backlog_measured_required`
