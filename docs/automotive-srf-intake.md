# Automotive SRF Intake

## Purpose

This document explains the optional local input path for measured automotive camera spectral response data.

The repository now supports freezing a measured automotive `RGB+NIR` camera SRF source into tracked `raw/` inputs, but the current shipped baseline does not yet include such a frozen source.

That means:

- the intake path exists
- the active camera profile is still `camera_reference_rgb_nir_v2`
- the measured backlog item `automotive_sensor_srf` remains open until a real measured source is provided

## Local Input Root

Default ignored local input root:

- `automotive_sensor_srf_input/`

Optional override:

- `AUTOMOTIVE_SENSOR_SRF_ROOT`

The local input root is intentionally ignored by git.

When valid input files are present, the generator copies them into:

- `raw/sources/automotive_sensor_srf_measured/`

That frozen copy becomes the tracked source of truth.

## Required Input Files

Required:

- `metadata.json`
- `srf.csv`

Optional:

- `report.pdf`

## Required CSV Structure

The generator expects a header row with either:

- `wavelength_nm`

or:

- `wavelength_um`

It also expects channel columns for:

- `r`
- `g`
- `b`
- `nir`

Minimal example:

```csv
wavelength_nm,r,g,b,nir
400,0.01,0.05,0.18,0.00
450,0.03,0.22,0.44,0.00
500,0.10,0.42,0.30,0.00
600,0.44,0.20,0.02,0.03
700,0.28,0.05,0.00,0.24
800,0.04,0.01,0.00,0.76
900,0.01,0.00,0.00,0.92
1000,0.00,0.00,0.00,0.48
1100,0.00,0.00,0.00,0.02
```

## Required Metadata Fields

Minimum required fields in `metadata.json`:

- `sensor_vendor`
- `sensor_model`

Recommended fields:

- `report_id`
- `report_date`
- `temperature_c`
- `measurement_type`
- `calibration_reference`
- `optics_stack_note`
- `measurement_notes`
- `license_summary`
- `classification`
- `response_scale`
- `wavelength_unit`

Example:

```json
{
  "sensor_vendor": "Example Vendor",
  "sensor_model": "Example RGBN Sensor",
  "report_id": "EMVA-Example-001",
  "report_date": "2026-04-17",
  "temperature_c": 25.0,
  "measurement_type": "measured_system_srf",
  "calibration_reference": "Narrowband scan, calibrated monochromator",
  "optics_stack_note": "Measured with the system optics and filter stack installed.",
  "measurement_notes": "Per-channel system response exported as CSV.",
  "license_summary": "Local measured data provided for in-repo use.",
  "classification": "derived-only",
  "response_scale": "unit_fraction",
  "wavelength_unit": "nm"
}
```

## Generator Behavior

When the local input is present and valid, the generator:

1. copies the source files into `raw/sources/automotive_sensor_srf_measured/`
2. records a source-ledger entry with local-path provenance
3. resamples the per-channel SRF curves onto the repo master grid
4. writes normalized active SRF curves into `canonical/spectra/`
5. generates `camera_automotive_measured_rgb_nir_v1.camera_profile.json`
6. promotes that measured profile to active scenario use

When the local input is absent:

- no measured automotive SRF source is frozen
- no measured automotive camera profile is generated
- `camera_reference_rgb_nir_v2` remains active

## Activation Gate

The measured profile is only activated if the frozen input:

- covers at least `400-1100 nm`
- includes all four channels `r`, `g`, `b`, `nir`
- has strictly increasing wavelength values
- passes the camera-profile validation checks already used by the generator

If the input is malformed, the build fails instead of silently inventing a measured profile.

## Current Status

Current repo truth:

- intake support exists
- no frozen measured automotive SRF source is present in the shipped baseline
- `camera_reference_rgb_nir_v2` remains the active profile
- `automotive_sensor_srf` remains `backlog_measured_required`
