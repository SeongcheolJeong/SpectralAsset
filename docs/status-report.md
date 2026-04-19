# Project Status Report

Snapshot date: April 19, 2026

This document is an internal snapshot of repository status, validation health, and near-term roadmap position for the autonomous-driving camera simulation asset pack.

## Executive Summary

- This repository generates an engine-agnostic asset pack for autonomous-driving camera simulation, including geometry, materials, emissive profiles, camera profiles, scenarios, scenes, and validation reports.
- The current baseline is healthy: release gates pass, generator outputs are tracked, and the current glTF validation set is clean.
- Catalog depth is no longer the main constraint. The pack now has broad standalone coverage across all five major asset families: `traffic_sign`, `traffic_light`, `road_surface`, `road_marking`, and `road_furniture`.
- The main remaining strategic gaps are measured-data replacement items, especially automotive SRF, traffic-signal/headlamp SPD, retroreflective sheeting, and wet-road behavior.
- The current next queued implementation item is `P3-T061`, which continues `road_furniture` expansion with transit-platform controller microsupport, curbside-priority attachments, and separator-island hardware follow-up.

## Current Baseline Snapshot

Current truth comes from `validation/reports/validation_summary.json`, `validation/reports/gltf_validation.json`, and the live backlog/docs that interpret those reports.

| Metric | Current value |
| --- | --- |
| Total assets | `379` |
| Traffic signs | `90` |
| Traffic lights | `61` |
| Road surfaces | `57` |
| Road markings | `69` |
| Road furniture | `102` |
| Spectral materials | `27` |
| Emissive profiles | `33` |
| Camera profiles | `3` |
| Scenario profiles | `4` |
| Validation scenes | `4` |
| GLBs checked | `383` |
| GLB errors | `0` |
| GLB warnings | `0` |
| Release-gate status | `pass` |
| Active camera profile | `camera_reference_rgb_nir_v3` |

## What Has Been Delivered

`P0-P2` work is effectively in place. Repository governance, git rules, source-policy handling, selected raw-source freezing, measured-vs-proxy clarity, USGS-based dry-material promotion, generic camera-profile support, and the public-data camera/night-emitter upgrade are all already landed in the working baseline. The active generic camera is now `camera_reference_rgb_nir_v3`, and public headlamp/streetlight priors are wired into `urban_night` when measured emitter data is absent.

`P3` is the dominant completed workstream. The broader expansion program now spans roughly sixty scoped follow-up batches, with the first fifty-seven completed and already pushing the pack far beyond the original starter baseline. The project now ships broad standalone coverage across all five asset families: `90` traffic signs, `61` traffic lights, `57` road surfaces, `69` road markings, and `102` roadside/support furniture assets. That means the repository is no longer constrained by starter-count coverage; it now has substantial standalone depth in geometry, templates, scene placements, and support context.

`P4` validation and reproducibility work is also in place. Validation expectations are documented, tracked generated outputs remain part of version control by design, and the generator preserves previous `generated_at` values by default to reduce rebuild churn. The current baseline continues to pass asset, material, emissive, camera, scenario, scale, semantic, wet-road, and release-gate checks.

`P5` intake scaffolding is implemented, but measured promotion is still blocked by missing real datasets. The repository can now accept and freeze local measured inputs for automotive SRF, traffic-signal/headlamp SPD, retroreflective sheeting, and wet-road behavior, but none of those measured datasets are currently present in tracked `raw/`. As a result, fidelity limits are now driven more by spectral and measurement gaps than by catalog-count or export-format gaps.

## Validation and Quality Status

The current baseline validates cleanly. Generator outputs are wired and tracked, scenario/material/emissive/camera validation passes, and glTF validation is clean across `383` checked files with `0` errors and `0` warnings. Release gates currently pass.

Quality status is also explicit about current limits. The active camera profile remains `camera_reference_rgb_nir_v3`, which is a public-data `vendor_derived` baseline rather than a measured automotive SRF. `urban_night` currently uses active signal curves plus public headlamp/streetlight priors, with `LED-B4` selected as the headlamp donor and `LED-B3` selected as the streetlight donor when no measured headlamp/streetlight source is active.

In this repository, a “healthy baseline” means generated outputs are intentionally tracked, rebuild behavior is reviewable, and the validation reports are the primary truth source for status. That is important because the project is not just source code; it is also a curated generated-data baseline with manifests, spectra, exports, and reports that are meant to be versioned together.

## Blockers and Open Risks

| Area | Status | Why blocked | Current fallback |
| --- | --- | --- | --- |
| Measured automotive SRF | `blocked` | No frozen measured automotive SRF dataset exists in tracked `raw/`. | `camera_reference_rgb_nir_v3` remains the active public-data `vendor_derived` camera profile. |
| Measured traffic-signal/headlamp SPD | `blocked` | No frozen measured emitter SPD dataset exists in tracked `raw/`. | Vendor-derived signal SPDs remain active, and `urban_night` uses public headlamp/streetlight priors. |
| Measured retroreflective sheeting | `blocked` | No frozen measured retroreflective dataset exists in tracked `raw/`. | The proxy shared retroreflective gain curve remains active. |
| Measured wet-road data | `blocked` | No frozen measured wet-road dataset exists in tracked `raw/`. | The simplified measured-derived wet asphalt path remains active. |

Two non-data risks remain visible. First, some upstream source pages still return `403`, so the repository depends on documented fallback handling rather than complete automated fetch coverage. Second, the retroreflective and wet-road contracts are still simplified: the current retroreflective path uses a shared spectral gain modifier rather than a full angle-aware BRDF, and the wet-road path uses a simplified wet reflectance plus overlay model rather than a full angle-aware wet-road BRDF.

## Next Steps

Immediate execution should follow the live backlog rather than this report. The current next queued task is `P3-T061`: expand `road_furniture` with transit-platform controller microsupport, curbside-priority attachments, and separator-island hardware follow-up. That is the current near-term implementation path already scoped in the backlog.

Near-term recommendation: continue catalog/support-tail expansion only if that still adds practical value for the intended downstream use. The asset catalog is already broad, so additional `P3` work should be judged on scenario usefulness and support-context depth rather than raw count growth alone.

Strategic recommendation: measured-data acquisition is still the highest-value fidelity unlock. The measured backlog remains open even though intake tooling is already built. If the project needs materially better realism rather than more catalog breadth, the highest-value next step is still real measured data for automotive SRF, traffic-signal/headlamp SPD, retroreflective sheeting, and wet-road behavior.

## Source References

Sources used for this report:

- [project-overview.md](project-overview.md)
- [task-backlog.md](task-backlog.md)
- [catalog-gap-review.md](catalog-gap-review.md)
- [validation_summary.json](../validation/reports/validation_summary.json)
- [gltf_validation.json](../validation/reports/gltf_validation.json)
- [measurement_backlog.json](../validation/reports/measurement_backlog.json)
