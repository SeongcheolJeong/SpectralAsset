# Camera Profile

## Purpose

This repository now ships two generic camera profiles for scene-to-camera simulation:

- `canonical/camera/camera_reference_rgb_nir_v1.camera_profile.json`
- `canonical/camera/camera_reference_rgb_nir_v2.camera_profile.json`

The goal is to make scenarios reference a concrete camera profile instead of only a broad `sensor_branch`, while preserving the earlier baseline for comparison.

## Current Active Profile

- active profile id: `camera_reference_rgb_nir_v2`
- retained comparison profile: `camera_reference_rgb_nir_v1`
- sensor branch: `rgb_nir`
- channels: `r`, `g`, `b`, `nir`
- storage grid: `350-1700 nm`, `1 nm`
- effective target range: `400-1100 nm`
- source quality for both current profiles: `vendor_derived`

## v1 vs v2

### `v1`

- earlier generic vendor-derived baseline
- one shared `optics_transmittance_ref` for all channels
- built from public vendor context rather than explicit donor QE reference curves

### `v2`

- active generic vendor-derived baseline
- uses tracked donor/reference curves from the official `MT9M034` datasheet
- uses `channel_optics_transmittance_refs` so `RGB` and `NIR` can have different optics/filter behavior
- records `reference_curve_refs`, `derivation_method`, and `replaces_profile_id`
- the official `MT9M034` PDF URL currently remains a preserved `fetch_failed` ledger entry, so the donor QE curves are tracked as explicit project-authored control points rather than parsed from a frozen raw PDF

## Raw vs Effective SRF

Both profiles track raw and effective channel curves.

- raw channel SRF: channel sensitivity prior before optics weighting
- optics transmittance:
  - `v1`: one shared optics curve
  - `v2`: per-channel optics/filter curves
- effective channel SRF: raw channel SRF multiplied by the relevant optics curve and normalized to unit peak

Fixed rule:

- `effective_srf = normalize_unit_peak(raw_srf * optics_transmittance)`

## Why These Are `vendor_derived`

The shipped profiles are derived from public vendor documentation and project-authored curve fitting, not from a measured single-SKU automotive camera calibration.

That means:

- they are more concrete than a pure branch label
- they are still not measured automotive SRF replacements
- they should be treated as stable generic reference cameras, not as ground truth for one exact sensor

## Scenario Binding

All current scenario profiles now reference the active `v2` profile:

- `canonical/camera/camera_reference_rgb_nir_v2.camera_profile.json`

`v1` stays in the repository for comparison, provenance, and backwards review.

## Remaining Gaps

These profiles do not resolve the measured backlog by themselves.

- automotive sensor SRF remains `backlog_measured_required`
- traffic-signal and headlamp SPD remain `backlog_measured_required`
- wet-road BRDF remains `backlog_measured_required`
- retroreflective sheeting BRDF remains `backlog_measured_required`

## Contract Notes

- scenarios must carry both `sensor_branch` and `camera_profile_ref`
- camera profiles must carry `source_quality` and `source_ids`
- camera profiles may use either one shared optics ref or per-channel optics refs
- `v2` camera profiles carry donor `reference_curve_refs` and explicit `derivation_method` metadata
- camera profiles must validate that raw and effective curves cover `400-1100 nm`
- effective channel curves must be unit-peak normalized
