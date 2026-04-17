# Camera Profile

## Purpose

This repository now ships three generic camera profiles for scene-to-camera simulation:

- `canonical/camera/camera_reference_rgb_nir_v1.camera_profile.json`
- `canonical/camera/camera_reference_rgb_nir_v2.camera_profile.json`
- `canonical/camera/camera_reference_rgb_nir_v3.camera_profile.json`

The goal is to make scenarios reference a concrete camera profile instead of only a broad `sensor_branch`, while preserving earlier vendor-derived baselines for comparison and provenance.

## Current Active Profile

- active profile id: `camera_reference_rgb_nir_v3`
- retained comparison profiles: `camera_reference_rgb_nir_v1`, `camera_reference_rgb_nir_v2`
- optional measured profile id when present: `camera_automotive_measured_rgb_nir_v1`
- sensor branch: `rgb_nir`
- channels: `r`, `g`, `b`, `nir`
- storage grid: `350-1700 nm`, `1 nm`
- effective target range: `400-1100 nm`
- source quality for the shipped generic profiles: `vendor_derived`
- no frozen measured automotive SRF source is present in the shipped baseline, so `v3` remains active

## v1 vs v2 vs v3

### `v1`

- earliest generic vendor-derived baseline
- one shared `optics_transmittance_ref` for all channels
- built from public vendor context rather than explicit donor QE reference curves

### `v2`

- second generic vendor-derived baseline
- uses tracked donor/reference curves from the official `MT9M034` datasheet
- uses `channel_optics_transmittance_refs` so `RGB` and `NIR` can have different optics/filter behavior
- records `reference_curve_refs`, `derivation_method`, and `replaces_profile_id`
- remains in the repo as the pre-`v3` comparison baseline

### `v3`

- active generic vendor-derived baseline
- keeps the `MT9M034` RGB donor curves
- replaces the older mono/NIR envelope with a tracked public Balluff `IMX900` EMVA mono donor curve
- keeps per-channel optics/filter behavior
- is intentionally more defensible than `v2`, but is still not a measured automotive camera SRF

### Optional measured profile

- generated only when a valid measured input is present in the local automotive SRF intake path
- uses `response_model = measured_system_srf`
- stores `active_channel_srf_refs` rather than requiring a `raw * optics = effective` decomposition
- becomes the active scenario-bound camera profile only when the frozen measured source exists and validates cleanly

## Raw vs Effective SRF

All generic shipped profiles track raw and effective channel curves.

- raw channel SRF: channel sensitivity prior before optics weighting
- optics transmittance:
  - `v1`: one shared optics curve
  - `v2` and `v3`: per-channel optics/filter curves
- effective channel SRF: raw channel SRF multiplied by the relevant optics curve and normalized to unit peak

Fixed rule:

- `effective_srf = normalize_unit_peak(raw_srf * optics_transmittance)`

For an optional measured-system profile:

- `active_channel_srf` is the measured system response that scenarios use directly
- no raw-vs-optics decomposition is assumed

## Why These Are `vendor_derived`

The shipped generic profiles are derived from public vendor documentation, public EMVA-style reports, and project-authored curve fitting, not from a measured single-SKU automotive camera calibration.

That means:

- they are more concrete than a pure branch label
- they are still not measured automotive SRF replacements
- they should be treated as stable generic reference cameras, not as ground truth for one exact production sensor

## Scenario Binding

All current scenario profiles now reference the active `v3` profile:

- `canonical/camera/camera_reference_rgb_nir_v3.camera_profile.json`

`v1` and `v2` stay in the repository for comparison, provenance, and backwards review.

If a valid measured automotive SRF source is frozen into `raw/sources/automotive_sensor_srf_measured/`, scenarios will instead bind to:

- `canonical/camera/camera_automotive_measured_rgb_nir_v1.camera_profile.json`

## Remaining Gaps

These profiles do not resolve the measured backlog by themselves.

- automotive sensor SRF remains `backlog_measured_required`
- traffic-signal and headlamp SPD remain `backlog_measured_required`
- wet-road BRDF remains `backlog_measured_required`
- retroreflective sheeting BRDF remains `backlog_measured_required`

The public-data `v3` rollout improves the generic baseline, but it does not close the measured automotive SRF backlog item.

## Contract Notes

- scenarios must carry both `sensor_branch` and `camera_profile_ref`
- camera profiles must carry `source_quality` and `source_ids`
- camera profiles may use either one shared optics ref or per-channel optics refs
- measured camera profiles may instead use `active_channel_srf_refs` with `response_model = measured_system_srf`
- `v2` and `v3` camera profiles carry donor `reference_curve_refs` and explicit `derivation_method` metadata
- camera profiles must validate that raw and effective curves cover `400-1100 nm`
- effective channel curves must be unit-peak normalized
- measured active channel curves must also cover `400-1100 nm` and be unit-peak normalized
