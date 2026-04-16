# PBRT Tutorial

## Purpose

This tutorial explains how to use the generated assets in this repository with `PBRT`.

The important constraint is:

- `PBRT` cannot use this repository's `.npz`, `.json`, `USD`, or `GLB` files directly as a full scene package

So the practical workflow is:

1. choose an asset or scenario from this repo
2. convert the geometry into a `PBRT`-friendly mesh format
3. convert the spectral `.npz` curves into `PBRT` spectrum text files
4. use the JSON files as the metadata contract that tells you which geometry, spectra, and states belong together

This repo is therefore a good `PBRT` source pack, not a direct `PBRT` scene pack.

## What PBRT Can Use From This Repo

`PBRT` is most useful here for:

- validating material reflectance
- validating signal/light emission
- comparing dry vs wet road appearance
- checking spectral rendering behavior before simulator integration

The easiest inputs to reuse are:

- geometry from `exports/gltf/*.glb` or `exports/usd/*.usdc`
- material spectra from `canonical/spectra/*.npz`
- material metadata from `canonical/materials/*.spectral_material.json`
- emitter metadata from `canonical/emissive/*.emissive_profile.json`
- scenario lighting references from `canonical/scenarios/*.scenario_profile.json`

## What PBRT Cannot Use Directly

You should treat these as conversion inputs, not drop-in `PBRT` files:

- `canonical/manifests/*.asset_manifest.json`
- `canonical/materials/*.json`
- `canonical/emissive/*.json`
- `canonical/camera/*.json`
- `canonical/scenes/*.usda`
- `exports/gltf/*.glb`
- `exports/usd/*.usdc`
- `canonical/spectra/*.npz`

In practice:

- `.json` tells you what to connect
- `.npz` gives you the numeric curves
- `USD` or `GLB` gives you the geometry source
- you still need a `PBRT` scene file that references converted meshes and converted spectra

## File Mapping

Use this mapping when building a `PBRT` scene:

| Repo file | Role in this repo | PBRT use |
| --- | --- | --- |
| `canonical/manifests/sign_stop.asset_manifest.json` | top-level asset definition | tells you which geometry and materials to use |
| `canonical/geometry/usd/sign_stop.usda` | authoring geometry | convert to triangle mesh |
| `exports/gltf/sign_stop.glb` | runtime mesh export | often the easiest source to convert to `PLY` |
| `canonical/materials/mat_asphalt_dry.spectral_material.json` | material contract | tells you the spectrum meaning and fallback values |
| `canonical/spectra/mat_asphalt_dry_reflectance.npz` | wavelength/value reflectance data | convert to `PBRT` spectrum text |
| `canonical/emissive/emissive_vehicle_standard.emissive_profile.json` | signal state-to-SPD mapping | tells you which SPD to use for each signal state |
| `canonical/scenarios/scenario_clear_noon.scenario_profile.json` | lighting/weather/camera selection | use for scene setup, not direct import |
| `canonical/camera/camera_reference_rgb_nir_v2.camera_profile.json` | camera SRF metadata | usually post-process or custom extension, not direct `PBRT` input |

## Recommended Workflow

### 1. Start From One Asset, Not a Whole Validation Scene

For a first `PBRT` integration, start with one of these:

- `road_asphalt_dry`
- `sign_stop`
- `signal_vehicle_vertical_3_aspect`

They cover the three main cases:

- reflective road material
- reflective sign material on a support object
- emissive signal state

Do not start with `canonical/scenes/*.usda` unless you already have a scene-conversion pipeline.

### 2. Use the Asset Manifest as the Entry Point

Example:

- `canonical/manifests/sign_stop.asset_manifest.json`

This tells you:

- the asset ID
- semantic class
- dimensions
- material IDs
- export file paths

For `sign_stop`, the manifest points to:

- `canonical/templates/signs/sign_stop.svg`
- `canonical/geometry/usd/sign_stop.usda`
- `exports/usd/sign_stop.usdc`
- `exports/gltf/sign_stop.glb`

For `PBRT`, the practical path is usually:

- read the manifest
- take the `gltf_binary` or `usd_binary` geometry path
- convert that geometry to `PLY`
- resolve each material ID through `canonical/materials/`

### 3. Convert Geometry to a PBRT-Friendly Mesh

`PBRT` does not natively consume this repo's `USD` or `GLB` assets as scene assets.

The safest path is:

1. take `exports/gltf/<asset>.glb`
2. convert it to `PLY`
3. reference the resulting mesh from your `PBRT` scene

Typical tools for the conversion step are:

- Blender
- Assimp-based pipelines
- your own `USD` or `glTF` conversion tooling

Practical recommendation:

- use `GLB -> PLY` for individual assets
- use `USD` only if you already have a strong `USD` pipeline

### 4. Convert `.npz` Spectra Into PBRT Spectrum Text

The repo stores spectra as `.npz` arrays with:

- `wavelength_nm`
- `values`

`PBRT` expects a text spectrum representation, so you need an export step.

Minimal example:

```python
import numpy as np
from pathlib import Path

def npz_to_pbrt_spectrum(npz_path: str, out_path: str, min_nm: int = 360, max_nm: int = 1100, step_nm: int = 5):
    data = np.load(npz_path)
    wavelength_nm = data["wavelength_nm"].astype(float)
    values = data["values"].astype(float)

    sample_wavelengths = np.arange(min_nm, max_nm + step_nm, step_nm, dtype=float)
    sample_values = np.interp(sample_wavelengths, wavelength_nm, values, left=0.0, right=0.0)
    sample_values = np.clip(sample_values, 0.0, None)

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for wl, v in zip(sample_wavelengths, sample_values):
            f.write(f"{wl:.1f} {v:.8f}\n")
```

Use this for:

- reflectance curves
- transmittance curves
- signal SPD curves
- illuminant curves

Recommended first conversions:

- `canonical/spectra/mat_asphalt_dry_reflectance.npz`
- `canonical/spectra/mat_asphalt_wet_reflectance.npz`
- `canonical/spectra/spd_signal_red_vendor_ref.npz`
- `canonical/spectra/illuminant_am1_5_global_tilt.npz`

### 5. Build PBRT Materials From the JSON Contracts

Example input:

- `canonical/materials/mat_asphalt_dry.spectral_material.json`

This tells you:

- `material_type`
- `quantity_type`
- which `.npz` file is the primary curve
- rough fallback values in `pbr_fallback`
- source quality and provenance

For `PBRT`, the mapping is:

- reflective material -> use the converted reflectance spectrum as the base reflectance
- transmittance material -> use the converted transmittance spectrum
- emissive material -> use the converted SPD as emission

For quick previews, the `pbr_fallback` block is a reasonable shortcut when you do not want to wire spectral input yet.

For example, `mat_asphalt_dry` already includes:

- `pbr_fallback.baseColorFactor`
- `pbr_fallback.roughnessFactor`

That is useful for a fast non-spectral `PBRT` draft, while the `.npz` route is the higher-fidelity path.

### 6. Use Emissive Profiles for Signal States

Example:

- `canonical/emissive/emissive_vehicle_standard.emissive_profile.json`

This file tells you which spectrum belongs to each signal state:

- `red`
- `yellow`
- `green`
- `flashing_yellow`
- `off`

That means the `PBRT` workflow is:

1. choose the active state
2. follow the state mapping to the correct SPD
3. convert that `.npz` SPD to a `PBRT` spectrum text file
4. bind it to the luminous part of the mesh as an emitting material or area light

For a red vehicle signal, the active source curve is:

- `canonical/spectra/spd_signal_red_vendor_ref.npz`

The housing geometry still comes from the signal mesh, but only the active lens should emit.

### 7. Use Scenario Profiles for Lighting, Not Direct Scene Import

Example:

- `canonical/scenarios/scenario_clear_noon.scenario_profile.json`

This gives you:

- `illuminant_ref`
- `atmosphere_ref`
- surface-state overrides
- sensor branch
- active camera profile

For `PBRT`, use it like this:

- `illuminant_ref`: convert to a `PBRT` spectrum for your sun/sky or distant-light setup
- `surface_state_overrides`: pick dry or wet asset/material variants
- `camera_profile_ref`: keep for later image weighting or custom sensor work
- `atmosphere_ref`: use as guidance for fog/media/sky configuration, not as a direct import file

Practical example:

- `scenario_clear_noon` -> use `road_asphalt_dry` and `illuminant_am1_5_global_tilt.npz`
- `scenario_wet_dusk` -> use `road_asphalt_wet` plus the dusk illuminant
- `scenario_urban_night` -> use the urban-night illuminant and signal SPDs

### 8. Treat Camera Profiles Separately

Current active camera profile:

- `canonical/camera/camera_reference_rgb_nir_v2.camera_profile.json`

This file is important, but it is not a direct `PBRT` scene file.

Use it in one of two ways:

1. render spectrally in `PBRT`, then apply the repo's camera effective SRF curves in a post-process
2. build a custom `PBRT` sensor extension that consumes the effective SRF curves directly

For most users, option `1` is the practical path.

Important limitation:

- the camera profile is still `vendor_derived`, not measured
- the automotive sensor backlog is still open

## Minimal Example Plan

If you want the fastest useful `PBRT` test, do this:

### Example A: dry asphalt patch

Use:

- geometry: `exports/gltf/road_asphalt_dry.glb`
- material JSON: `canonical/materials/mat_asphalt_dry.spectral_material.json`
- reflectance: `canonical/spectra/mat_asphalt_dry_reflectance.npz`
- scenario: `canonical/scenarios/scenario_clear_noon.scenario_profile.json`
- illuminant: `canonical/spectra/illuminant_am1_5_global_tilt.npz`

Goal:

- validate the measured USGS-derived dry asphalt baseline under daytime illumination

### Example B: stop sign

Use:

- geometry: `exports/gltf/sign_stop.glb`
- manifest: `canonical/manifests/sign_stop.asset_manifest.json`
- materials:
  - `mat_sign_stop_red`
  - `mat_sign_white`
  - `mat_metal_galvanized`

Goal:

- validate sign-face and pole appearance under daylight

Important note:

- the sign colors are still proxy materials, not measured retroreflective sign-sheeting BRDF replacements

### Example C: red traffic signal at night

Use:

- geometry: `exports/gltf/signal_vehicle_vertical_3_aspect.glb`
- emissive profile: `canonical/emissive/emissive_vehicle_standard.emissive_profile.json`
- active SPD: `canonical/spectra/spd_signal_red_vendor_ref.npz`
- scenario: `canonical/scenarios/scenario_urban_night.scenario_profile.json`

Goal:

- validate the active red-signal emission with the current vendor-derived SPD fit

## Example Scene Fragment

The exact `PBRT` scene syntax depends on your renderer version and scene conventions, but the structure should look like this:

```text
MakeNamedMaterial "asphalt"
    "string type" ["diffuse"]
    "spectrum reflectance" ["materials/mat_asphalt_dry_reflectance.spd"]

AttributeBegin
    NamedMaterial "asphalt"
    Shape "plymesh"
        "string filename" ["meshes/road_asphalt_dry.ply"]
AttributeEnd
```

For an emitting traffic-signal lens, the structure becomes:

```text
AttributeBegin
    AreaLightSource "diffuse"
        "spectrum L" ["lights/spd_signal_red_vendor_ref.spd"]
    Shape "plymesh"
        "string filename" ["meshes/signal_red_lens.ply"]
AttributeEnd
```

Treat these as structural examples. The exact material model, scale, and light parameters should follow your `PBRT` version and your calibration goals.

## Recommended First Rendering Order

Do the integration in this order:

1. `road_asphalt_dry` under `scenario_clear_noon`
2. `road_asphalt_wet` under `scenario_wet_dusk`
3. `sign_stop` under `scenario_clear_noon`
4. `signal_vehicle_vertical_3_aspect` with the red state under `scenario_urban_night`

That sequence lets you validate:

- measured dry reflectance
- measured-derived wet reflectance
- mixed-material asset assembly
- emissive state handling

## Known Limitations

When using this repo with `PBRT`, keep these limits in mind:

- there is no direct `USD -> PBRT` or `.json -> PBRT` pipeline in this repository yet
- `.npz` spectra must be converted before `PBRT` can use them
- camera profiles are not direct `PBRT` inputs unless you add post-processing or a custom sensor path
- sign materials are still proxy approximations, not measured retroreflective sheeting
- road-marking retroreflection remains incomplete
- wet-road BRDF remains incomplete

## Practical Rule

If you want to use this repo with `PBRT`, think of the files like this:

- asset manifest = what to assemble
- `GLB` or `USD` = where the geometry comes from
- material/emissive JSON = which curves to use
- `.npz` = the actual spectral numbers
- scenario JSON = which lighting and surface state to choose
- camera profile JSON = how to weight the final spectral result after rendering
