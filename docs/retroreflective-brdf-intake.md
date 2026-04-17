# Retroreflective BRDF Intake

## Purpose

This document explains the optional local input path for measured retroreflective sheeting data.

The repository now supports freezing a measured retroreflective source into tracked `raw/` inputs, but the current shipped baseline does not yet include such a frozen source.

That means:

- the intake path exists
- the active retroreflective modifier is still the project proxy curve
- the current repository contract can only activate a shared spectral gain modifier, not a full angle-aware BRDF
- the backlog item `retroreflective_sheeting_brdf` remains open

## Local Input Root

Default ignored local input root:

- `retroreflective_sheeting_brdf_input/`

Optional override:

- `RETROREFLECTIVE_SHEETING_BRDF_ROOT`

The local input root is intentionally ignored by git.

When valid input files are present, the generator copies them into:

- `raw/sources/retroreflective_sheeting_brdf_measured/`

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

Supported gain columns:

- `retroreflective_gain`
- `marking_white_gain`
- `marking_yellow_gain`

At least one supported gain column must be present.

Minimal example:

```csv
wavelength_nm,retroreflective_gain,marking_white_gain,marking_yellow_gain
400,1.02,1.04,1.00
450,1.08,1.10,1.06
500,1.14,1.16,1.10
550,1.18,1.20,1.14
600,1.21,1.24,1.18
650,1.23,1.26,1.20
700,1.22,1.25,1.19
800,1.16,1.18,1.14
900,1.10,1.12,1.08
1100,1.02,1.04,1.00
```

## Required Metadata Fields

Recommended fields in `metadata.json`:

- `classification`
- `license_summary`
- `report_id`
- `report_date`
- `wavelength_unit`
- `response_scale`
- `sheeting_class`
- `sample_state`
- `entrance_angle_deg`
- `observation_angle_deg`
- `measurement_geometry`
- `calibration_reference`
- `measurement_notes`
- `channel_columns`

Example:

```json
{
  "classification": "derived-only",
  "license_summary": "Local measured retroreflective sheeting data provided for in-repo use.",
  "report_id": "RETRO-2026-001",
  "report_date": "2026-04-17",
  "wavelength_unit": "nm",
  "response_scale": "unit_gain",
  "sheeting_class": "Engineer Grade",
  "sample_state": "dry",
  "entrance_angle_deg": -4.0,
  "observation_angle_deg": 0.2,
  "measurement_geometry": "Fixed entrance/observation geometry",
  "calibration_reference": "Calibrated narrowband retroreflection rig",
  "measurement_notes": "Shared retroreflective gain plus separate white and yellow marking captures.",
  "channel_columns": {
    "retroreflective_gain": "retroreflective_gain",
    "marking_white_gain": "marking_white_gain",
    "marking_yellow_gain": "marking_yellow_gain"
  }
}
```

## Generator Behavior

When the local input is present and valid, the generator:

1. copies the source files into `raw/sources/retroreflective_sheeting_brdf_measured/`
2. records a source-ledger entry with local-path provenance
3. resamples the measured gain curves onto the repo master grid
4. writes source-specific measured retroreflective curves into `canonical/spectra/`
5. activates a measured shared retroreflective gain modifier for the current marking-material path
6. upgrades `mat_marking_white` and `mat_marking_yellow` from fully proxy to `measured_derivative`

When the local input is absent:

- no measured retroreflective source is frozen
- no measured retroreflective modifier is generated
- the proxy `mat_retroreflective_gain` curve remains active

## Activation Gate

The measured retroreflective modifier is only activated if the frozen input:

- covers at least `400-1100 nm`
- includes at least one supported gain column
- has strictly increasing wavelength values
- passes material validation through the existing generated-material path

Selection behavior:

- if `retroreflective_gain` is present, it becomes the active shared modifier
- if only `marking_white_gain` and `marking_yellow_gain` are present, they are averaged into the current shared modifier path
- if only one marking-specific gain column is present, that single measured curve becomes the active shared modifier

## Important Limitation

This intake does **not** solve the full `retroreflective_sheeting_brdf` backlog item.

The current repository material contract still uses a shared spectral gain curve. It does not yet model:

- entrance-angle dependence
- observation-angle dependence
- separate sign-sheeting classes
- full BRDF or RA tables

So this intake is a measurable fidelity improvement for the current simplified path, not a full angular retroreflective BRDF replacement.

## Current Status

Current repo truth:

- intake support exists
- no frozen measured retroreflective source is present in the shipped baseline
- `mat_marking_white` and `mat_marking_yellow` still use the proxy shared retroreflective gain curve
- `retroreflective_sheeting_brdf` remains `backlog_measured_required`
