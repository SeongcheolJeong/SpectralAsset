# Public-Data Upgrade

## Purpose

This document explains the `internet-only` public-data upgrade phase that strengthened the current baseline without claiming that the measured backlog is solved.

The phase intentionally targeted the strongest public-data wins:

- a stronger generic `RGB+NIR` camera profile
- public night-emitter priors for headlamp and streetlight contribution in `urban_night`

It intentionally did not attempt to close the measured backlog.

## Current Public-Data Results

- active generic camera: `camera_reference_rgb_nir_v3`
- retained earlier baselines: `camera_reference_rgb_nir_v1`, `camera_reference_rgb_nir_v2`
- public headlamp LED donor column: `LED-B4`
- public streetlight LED donor column: `LED-B3`
- public halogen-like headlamp prior: CIE illuminant A
- `urban_night` now uses public headlamp/streetlight priors when measured emitter data is absent

## Exact Public Sources Used

Camera references:

- `onsemi_mt9m034_pdf`
- `balluff_imx900_emva_report_pdf`
- `basler_color_emva_knowledge`
- `sony_imx900_product_page`
- `sony_isx016_pdf`
- `emva_1288_standard_pdf`

Night-emitter references:

- `cie_illuminant_a_csv`
- `cie_led_illuminants_csv`
- `fhwa_spectral_driver_performance_pdf`

## Public-Data Honesty Rules

- direct numeric public dataset matching the shipped quantity may only be called `measured_standard` if it truly is the shipped physical quantity
- public plot fit or public reference mixture remains `vendor_derived`
- narrative-only documentation remains `reference-only`

This rule is why:

- `camera_reference_rgb_nir_v3` is still `vendor_derived`
- public headlamp and streetlight priors do not close the emitter measurement backlog

## Why v3 Does Not Close Automotive SRF

`camera_reference_rgb_nir_v3` is stronger than `v2`, but it is still a synthetic generic profile built from:

- public donor QE references
- public EMVA-style context
- project-authored optics assumptions

It is not a measured single-system automotive SRF frozen from a real camera capture.

So the backlog item `automotive_sensor_srf` remains `backlog_measured_required`.

## Why Public Night Priors Do Not Close Emitter Backlog

The public headlamp and streetlight priors improve `urban_night`, but they are still generic donor spectra.

They are not:

- measured traffic-signal captures
- measured headlamp captures
- measured streetlight captures from the exact deployment context

So the backlog item `traffic_signal_headlamp_spd` remains `backlog_measured_required`.

## Deferred by Design

This public-data phase did not include:

- retroreflective proxy tuning from public sources
- wet-road proxy tuning from public sources

Those follow-ups remain intentionally deferred so the public-data phase stays focused on the highest-value camera and night-emitter improvements.
