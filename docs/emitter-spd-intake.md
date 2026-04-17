# Emitter SPD Intake

## Purpose

This document explains the optional local input path for measured traffic-signal and headlamp spectral power distribution data.

The repository now supports freezing a measured emitter source into tracked `raw/` inputs, but the current shipped baseline does not yet include such a frozen source.

That means:

- the intake path exists
- vehicle and protected-turn traffic-signal profiles still use vendor-derived public fits
- the `urban_night` illuminant now uses public headlamp and streetlight priors when measured emitter data is absent
- the backlog item `traffic_signal_headlamp_spd` remains open

## Local Input Root

Default ignored local input root:

- `traffic_signal_headlamp_spd_input/`

Optional override:

- `TRAFFIC_SIGNAL_HEADLAMP_SPD_ROOT`

The local input root is intentionally ignored by git.

When valid input files are present, the generator copies them into:

- `raw/sources/traffic_signal_headlamp_spd_measured/`

That frozen copy becomes the tracked source of truth.

## Required Input Files

Required:

- `metadata.json`
- `spd.csv`

Optional:

- `report.pdf`

## Required CSV Structure

The generator expects a header row with either:

- `wavelength_nm`

or:

- `wavelength_um`

Required emitter columns:

- none globally, but see the activation rules below

Optional emitter columns:

- `signal_red`
- `signal_yellow`
- `signal_green`
- `headlamp_led_lowbeam`
- `headlamp_halogen_lowbeam`
- `streetlight_led_4000k`
- `signal_ped_red`
- `signal_ped_white`
- `signal_countdown_amber`

Minimal example:

```csv
wavelength_nm,signal_red,signal_yellow,signal_green,headlamp_led_lowbeam,streetlight_led_4000k
400,0.00,0.00,0.00,0.12,0.05
450,0.00,0.00,0.02,0.38,0.18
500,0.00,0.00,0.22,0.62,0.34
550,0.00,0.04,0.48,0.88,0.62
600,0.08,0.42,0.06,0.94,0.84
650,0.58,0.18,0.00,0.82,0.92
700,0.42,0.00,0.00,0.56,0.88
800,0.00,0.00,0.00,0.14,0.42
900,0.00,0.00,0.00,0.02,0.10
1100,0.00,0.00,0.00,0.00,0.00
```

## Required Metadata Fields

Recommended fields in `metadata.json`:

- `classification`
- `license_summary`
- `report_id`
- `report_date`
- `wavelength_unit`
- `response_scale`
- `calibration_reference`
- `capture_geometry`
- `drive_mode`
- `ambient_conditions`
- `measurement_notes`
- `channel_columns`

Example:

```json
{
  "classification": "derived-only",
  "license_summary": "Local measured traffic-signal and headlamp SPD data provided for in-repo use.",
  "report_id": "SPD-2026-001",
  "report_date": "2026-04-17",
  "wavelength_unit": "nm",
  "response_scale": "unit_fraction",
  "calibration_reference": "Calibrated spectroradiometer with dark correction",
  "capture_geometry": "On-axis capture at fixed distance",
  "drive_mode": "steady operating state",
  "ambient_conditions": "Indoor dark-room capture",
  "measurement_notes": "Signal red/yellow/green plus headlamp and streetlight captures.",
  "channel_columns": {
    "signal_red": "signal_red",
    "signal_yellow": "signal_yellow",
    "signal_green": "signal_green",
    "headlamp_led_lowbeam": "headlamp_led_lowbeam",
    "streetlight_led_4000k": "streetlight_led_4000k"
  }
}
```

## Generator Behavior

When the local input is present and valid, the generator:

1. copies the source files into `raw/sources/traffic_signal_headlamp_spd_measured/`
2. records a source-ledger entry with local-path provenance
3. resamples the measured curves onto the repo master grid
4. writes measured emitter curves into `canonical/spectra/`
5. switches vehicle and protected-turn emissive profiles to measured signal curves only if `signal_red`, `signal_yellow`, and `signal_green` are all present
6. updates the `urban_night` illuminant to include measured headlamp or streetlight curves whenever those curves are present, even if measured traffic-signal curves are not

When the local input is absent:

- no measured emitter source is frozen
- no measured signal SPDs are generated
- vendor-derived signal curves remain active
- `urban_night` uses public headlamp and streetlight priors when those public source files are available, otherwise it falls back to the active signal curves only

## Activation Gate

Measured traffic-signal curves are only activated if the frozen input:

- covers at least `400-1100 nm`
- includes `signal_red`, `signal_yellow`, and `signal_green`
- has strictly increasing wavelength values
- passes emissive-profile validation

Headlamp-only or streetlight-only input is allowed.

If the frozen input contains:

- `headlamp_led_lowbeam`, `headlamp_halogen_lowbeam`, or `streetlight_led_4000k`

then those curves may improve `urban_night` even when the measured traffic-signal red/yellow/green trio is missing.

## Current Status

Current repo truth:

- intake support exists
- no frozen measured traffic-signal or headlamp SPD source is present in the shipped baseline
- vehicle and protected-turn signal profiles remain `vendor_derived`
- `urban_night` still lacks measured headlamp or streetlight curves, but now uses public `LED-B4` and `LED-B3` priors when measured data is absent
- `traffic_signal_headlamp_spd` remains `backlog_measured_required`

## Practical Result

You can now provide either of these:

- a combined measured emitter file with signal plus headlamp curves
- a headlamp-only or streetlight-only measured file

The difference is:

- combined measured signal data can replace the active vehicle/protected-turn signal SPDs
- headlamp-only data cannot replace signal SPDs, but it can still improve the `urban_night` illuminant
