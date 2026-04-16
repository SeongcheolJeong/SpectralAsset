# Camera Profile

## Purpose

This repository now ships one generic camera profile for scene-to-camera simulation:

- `canonical/camera/camera_reference_rgb_nir_v1.camera_profile.json`

The goal is to make scenarios reference a concrete camera profile instead of only a broad `sensor_branch`.

## Current Profile

- profile id: `camera_reference_rgb_nir_v1`
- sensor branch: `rgb_nir`
- channels: `r`, `g`, `b`, `nir`
- storage grid: `350-1700 nm`, `1 nm`
- effective target range: `400-1100 nm`
- current source quality: `vendor_derived`

## Raw vs Effective SRF

The profile tracks both raw and effective channel curves.

- raw channel SRF: generic channel sensitivity prior before optics weighting
- optics transmittance: generic lens/filter stack transmittance prior
- effective channel SRF: raw channel SRF multiplied by optics transmittance and normalized to unit peak

Fixed rule:

- `effective_srf = normalize_unit_peak(raw_srf * optics_transmittance)`

## Why This Is `vendor_derived`

The current profile is derived from public vendor documentation and vendor-adjacent public references, not from a measured single-SKU automotive camera calibration.

That means:

- it is more concrete than a pure branch label
- it is still not a measured automotive SRF replacement
- it should be treated as a stable generic reference camera, not as ground truth for one exact sensor

## Scenario Binding

All current scenario profiles now reference the same camera profile:

- `canonical/camera/camera_reference_rgb_nir_v1.camera_profile.json`

This keeps the phase data-first and avoids introducing multiple camera branches before the measured backlog is reduced.

## Remaining Gaps

This profile does not resolve the measured backlog by itself.

- automotive sensor SRF remains `backlog_measured_required`
- traffic-signal and headlamp SPD remain `backlog_measured_required`
- wet-road BRDF remains `backlog_measured_required`
- retroreflective sheeting BRDF remains `backlog_measured_required`

## Contract Notes

- scenarios must carry both `sensor_branch` and `camera_profile_ref`
- camera profiles must carry `source_quality` and `source_ids`
- camera profiles must validate that raw and effective curves cover `400-1100 nm`
- effective channel curves must be unit-peak normalized
