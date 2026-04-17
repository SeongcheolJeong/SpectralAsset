# File Formats

## Purpose

This file explains the main generated file formats used in this repository, especially:

- `.npz`
- `.json`
- `USD`

## What Is `.npz`

`.npz` is a NumPy archive format.

In practice, it is a zipped container of one or more numeric arrays. In this repository it is used for spectral and camera-response data.

Typical arrays inside a file are:

- `wavelength_nm`
- `values`

Common uses in this repo:

- material reflectance
- lens transmittance
- emitted light spectra (`SPD`)
- camera spectral response curves (`SRF`)
- wavelength grids

Examples:

- `canonical/spectra/mat_asphalt_dry_reflectance.npz`
- `canonical/spectra/spd_signal_red_vendor_ref.npz`
- `canonical/spectra/cam_ref_rgbnir_v2_r_effective_srf.npz`
- `canonical/spectra/grid_master_350_1700_1nm.npz`

Important note:

- `.npz` itself does not tell you the meaning of the numbers
- the meaning comes from the JSON file that references it

So `.npz` is the numeric data layer.

## What Is `.json`

`.json` is a text-based metadata format.

In this repository, JSON files describe what the assets are, how they connect, and what each spectral file means.

Common JSON file types here:

- asset manifests
- spectral material files
- emissive profiles
- camera profiles
- scenario profiles
- source-ledger entries
- validation reports

Examples:

- `canonical/manifests/sign_stop.asset_manifest.json`
- `canonical/materials/mat_asphalt_dry.spectral_material.json`
- `canonical/emissive/emissive_vehicle_standard.emissive_profile.json`
- `canonical/camera/camera_reference_rgb_nir_v3.camera_profile.json`
- `canonical/scenarios/scenario_clear_noon.scenario_profile.json`
- `validation/reports/validation_summary.json`

What JSON does in this repo:

- gives IDs and semantic meaning
- points to `.npz` files and geometry files
- records provenance, source quality, and licenses
- records states, scenario links, and export targets

So `.json` is the contract and metadata layer.

## What Is USD

`USD` means `Universal Scene Description`.

It is a 3D scene and asset format used to describe geometry, hierarchy, references, transforms, and scene composition.

In this repo, USD is the main geometry/scene format.

Two USD forms appear here:

### `.usda`

This is the text form of USD.

Use it when you want to:

- read the file directly
- inspect geometry structure
- inspect references and transforms

Examples:

- `canonical/geometry/usd/sign_stop.usda`
- `canonical/scenes/scene_sign_test_lane.usda`

### `.usdc`

This is the binary form of USD.

Use it when you want:

- compact storage
- faster interchange/runtime loading

Examples:

- `exports/usd/sign_stop.usdc`
- `exports/usd/scene_sign_test_lane.usdc`

So USD is the 3D geometry and scene layer.

## What Is `.glb`

`GLB` is the binary form of `glTF`.

This repo exports GLB files for runtime portability.

Examples:

- `exports/gltf/sign_stop.glb`
- `exports/gltf/signal_vehicle_vertical_3_aspect.glb`

Compared with USD:

- USD is the main authoring/interchange scene format here
- GLB is the simpler runtime export

## How the Formats Work Together

The repository is split by responsibility:

- `.npz`: numeric spectral data
- `.json`: meaning, relationships, validation metadata
- `.usda` / `.usdc`: 3D geometry and scene structure
- `.glb`: runtime export

## Example: one material

For dry asphalt:

1. `canonical/materials/mat_asphalt_dry.spectral_material.json`
2. `canonical/spectra/mat_asphalt_dry_reflectance.npz`

The JSON says:

- this is a reflective material
- what the curve means
- which file contains the curve
- what fallback color to use in non-spectral runtimes

The `.npz` stores the actual wavelength/value data.

## Example: one asset

For a stop sign:

1. `canonical/manifests/sign_stop.asset_manifest.json`
2. `canonical/geometry/usd/sign_stop.usda`
3. `exports/usd/sign_stop.usdc`
4. `exports/gltf/sign_stop.glb`
5. linked material JSON files
6. linked spectral `.npz` files

That means:

- JSON says what the asset is
- USD stores the geometry
- GLB is the portable export
- material JSON points to the spectral `.npz` data

## Example: one camera profile

For `camera_reference_rgb_nir_v3`:

1. `canonical/camera/camera_reference_rgb_nir_v3.camera_profile.json`
2. `canonical/spectra/cam_ref_rgbnir_v3_*_raw_srf.npz`
3. `canonical/spectra/cam_ref_rgbnir_v3_*_effective_srf.npz`
4. `canonical/spectra/cam_ref_rgbnir_v3_rgb_optics_transmittance.npz`
5. `canonical/spectra/cam_ref_rgbnir_v3_nir_optics_transmittance.npz`

The JSON explains:

- which channels exist
- which raw and effective SRF files belong to each channel
- which optics/filter curves are used
- where the donor/reference curves came from

The `.npz` files store the actual channel curves.

## Short Definitions

- `.npz`: zipped NumPy arrays for wavelength-based numeric data
- `.json`: structured text metadata and file-to-file relationships
- `.usda`: human-readable USD text
- `.usdc`: binary USD
- `.glb`: binary glTF runtime export

## Practical Rule

If you want to know:

- "what are the numbers?" open `.npz`
- "what do the numbers mean?" open `.json`
- "what is the 3D object?" open `.usda` or `.usdc`
- "what is the portable runtime model?" open `.glb`
