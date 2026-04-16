# Measurement Replacement Priorities

## Purpose

This document closes `P2-T003` by ranking the current measured-replacement backlog by simulation impact and acquisition difficulty. The ranking below is inferred from the current generated catalog, validation scenes, and research priorities in [../deep-research-report.md](../deep-research-report.md).

Current baseline note:

- dry asphalt, concrete, and galvanized metal have already been promoted from a frozen selected USGS v7 subset
- wet asphalt is now a measured-derived material rather than a fully proxy dry/wet pair
- vehicle and protected-turn traffic-signal emissive profiles now use vendor-derived public LED fits, but measured emitter replacement is still pending
- `camera_reference_rgb_nir_v2` is now the active generic reference camera, but the top-ranked automotive SRF backlog still remains measured-required
- the ranked backlog below therefore stays focused on the remaining high-impact camera, emitter, and BRDF gaps

## Inputs

- [../validation/reports/measurement_backlog.json](../validation/reports/measurement_backlog.json)
- [asset-spec.md](asset-spec.md)
- [project-overview.md](project-overview.md)
- [source-policy.md](source-policy.md)
- [../deep-research-report.md](../deep-research-report.md)

## Ranking Method

Impact scale:

- `critical`: changes scene-to-sensor response across nearly the entire pack
- `high`: materially changes one or more important scenario classes or validation scenes
- `medium`: important, but limited to a narrower subset of assets or scenes

Difficulty scale:

- `medium`: can be acquired with a standard spectroradiometric workflow and moderate fixture control
- `high`: needs calibrated lab workflow, stable operating conditions, or vendor cooperation
- `very_high`: needs angular sampling, controlled sample preparation, and repeated measurement campaigns

## Ranked Backlog

| Rank | Backlog ID | Impact | Difficulty | Primary Affected Scope | Why It Ranks Here | Recommended Acquisition Path |
| --- | --- | --- | --- | --- | --- | --- |
| `1` | `automotive_sensor_srf` | `critical` | `high` | all reflective and emissive assets, every scenario, every validation scene | This is the weighting function for every spectrum-to-camera integration. Improving materials before the sensor response is measured still leaves the camera model underconstrained. | EMVA-style narrowband scan or vendor EMVA/NDA report with per-channel spectral response from `350-1100 nm`, plus operating temperature and optics-stack notes |
| `2` | `traffic_signal_headlamp_spd` | `high` | `medium` | night scenarios, traffic-light assets, future nighttime validation work | Night rendering and traffic-light state realism depend directly on emitter spectra. The current vendor-derived signal fits are useful, but measured emitter replacement is still simpler than BRDF gaps and unlocks more believable night scenes quickly. | spectroradiometer capture of traffic signals and representative headlamps with state, drive mode, and viewing geometry recorded |
| `3` | `retroreflective_sheeting_brdf` | `high` | `very_high` | most traffic signs, future retroreflective marking upgrades, night retroreflection scene | The current sign catalog is broad, so retroreflective error propagates across many assets. It ranks below SPD because the acquisition workflow is harder and more angle-sensitive. | controlled retroreflection or BRDF campaign covering sheeting class, entrance angle, observation angle, dry/aged state, and wavelength coverage |
| `4` | `wet_road_spectral_brdf` | `high` | `very_high` | wet asphalt material, wet dusk scenario, wet-road braking scene | This matters strongly for wet-road realism, but today it touches fewer shipped assets than sensor SRF or sign retroreflection. It remains a release-relevant gap once the angular measurement rig is available. | goniometric wet-surface campaign covering dry baseline, water-film thickness, roughness, specular lobe shape, and repeated measurements across drying states |

## Recommended Execution Order

1. Measure or source `automotive_sensor_srf` first.
2. Replace `traffic_signal_headlamp_spd` next to improve night scenes and signal-state realism.
3. Measure `retroreflective_sheeting_brdf` before broadening sign and marking night-validation claims.
4. Measure `wet_road_spectral_brdf` once the angular workflow is stable enough to support repeatable wet-surface capture.

## Raw Data Requirements

| Backlog ID | Minimum Raw Inputs to Track | Promotion Gate from Proxy to Measured |
| --- | --- | --- |
| `automotive_sensor_srf` | wavelength grid, per-channel response, operation point, sensor temperature, calibration reference, optics stack note | raw data is frozen in `raw/`, channel curves are reproducible in `canonical/spectra/`, and provenance identifies the exact sensor or report |
| `traffic_signal_headlamp_spd` | wavelength grid, emitter state, drive mode, ambient conditions, capture distance or geometry, instrument calibration | each emitted-state curve resolves from a tracked raw capture and the emissive profile cites the measured source directly |
| `retroreflective_sheeting_brdf` | wavelength grid, entrance angle, observation angle, sheeting class, dry/aged state, instrument geometry | sign-material manifests replace proxy gain curves with angle-aware measured inputs and record uncertainty/conditions |
| `wet_road_spectral_brdf` | wavelength grid, substrate ID, dry reference, water-film condition, roughness note, geometry | wet-road material manifests replace overlay proxies with measured inputs that explain dry-to-wet state transitions |

## Current Release Implication

- `automotive_sensor_srf` is the highest-value fidelity upgrade for the whole repository.
- `traffic_signal_headlamp_spd` remains the fastest measured night-scene realism win even though vehicle and protected-turn traffic-signal profiles now use vendor-derived public fits.
- `retroreflective_sheeting_brdf` is the highest-risk remaining gap for sign realism after SPD replacement.
- `wet_road_spectral_brdf` stays on the critical backlog, but current v1 scope makes it narrower than the other three items.
- activating `camera_reference_rgb_nir_v2` does not change the measured status of the top-ranked automotive SRF backlog item
- dry road/support material baselines are no longer the first material-fidelity gap because selected USGS v7 measured baselines are now active in the repository.

This ranking should be revisited when the catalog or validation-scene mix changes materially.
