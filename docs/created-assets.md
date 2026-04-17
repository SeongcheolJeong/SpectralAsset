# Created Assets

## Purpose

This file explains what the generator actually creates in this repository and how the created files relate to each other.

Current generated baseline:

- `61` assets
- `20` spectral materials
- `4` emissive profiles
- `3` camera profiles
- `4` scenario profiles
- `4` validation scenes

## What Counts as an Asset

In this repository, an "asset" usually means a reusable simulation object with:

- an asset manifest in `canonical/manifests/`
- source geometry in `canonical/geometry/usd/`
- runtime exports in `exports/usd/` and `exports/gltf/`
- linked materials, states, and semantic metadata

Examples:

- signs such as `sign_stop`
- traffic lights such as `signal_vehicle_vertical_3_aspect`
- road surfaces such as `road_asphalt_dry`
- furniture such as `furniture_sign_pole`

## Main Asset Families

### `traffic_sign`

These are sign objects such as:

- `sign_stop`
- `sign_yield`
- `sign_speed_limit_50`

Each sign usually has:

- an SVG sign-face template in `canonical/templates/signs/`
- a USD geometry file in `canonical/geometry/usd/`
- an asset manifest in `canonical/manifests/`
- linked spectral materials such as `mat_sign_stop_red` and `mat_sign_white`

### `traffic_light`

These are signal housings such as:

- `signal_vehicle_vertical_3_aspect`
- `signal_vehicle_horizontal_3_aspect`
- `signal_protected_turn_4_aspect`

Each signal usually has:

- a USD geometry file
- an asset manifest
- off-state lens materials
- a linked emissive profile that defines what spectral curve is active in each state

### `road_surface`

These are reusable road or pavement surfaces such as:

- `road_asphalt_dry`
- `road_asphalt_wet`
- `road_concrete`
- `road_asphalt_patched`
- `road_concrete_distressed`
- `road_asphalt_concrete_transition`
- `road_gutter_transition`
- `road_sidewalk_panel`

They mainly depend on spectral material definitions rather than complex state logic, but the newer variants also mix the existing asphalt and concrete materials to represent repairs, joint distress, and urban edge transitions.

### `road_marking`

These are markings such as:

- `marking_lane_white`
- `marking_lane_yellow`
- `marking_crosswalk`
- `marking_stop_line`
- `marking_edge_line_white`
- `marking_arrow_straight_white`
- `marking_arrow_turn_left_white`
- `marking_chevron_gore_white`
- `marking_lane_white_worn`

They use retroreflective or reflective material definitions and are important for camera visibility tests.

### `road_furniture`

These are support/context objects such as:

- `furniture_sign_pole`
- `furniture_signal_pole`
- `furniture_guardrail_bollard_set`
- `furniture_guardrail_segment`
- `furniture_bollard_flexible`
- `furniture_delineator_post`
- `furniture_traffic_cone`
- `furniture_water_barrier`
- `furniture_barricade_panel`
- `furniture_signal_backplate_vertical`
- `furniture_signal_backplate_horizontal`
- `furniture_signal_mast_hanger`
- `furniture_signal_controller_cabinet`
- `furniture_sign_back_octagon`
- `furniture_sign_back_round`
- `furniture_sign_back_triangle`
- `furniture_sign_back_square`
- `furniture_sign_back_rectangle_wide`
- `furniture_sign_mount_bracket_single`
- `furniture_sign_mount_bracket_double`

## Other Generated Objects

### Spectral materials

Stored in `canonical/materials/`.

These define things like:

- asphalt reflectance
- sign-face colors
- lens transmittance
- retroreflective modifiers

Example:

- `canonical/materials/mat_asphalt_dry.spectral_material.json`

### Emissive profiles

Stored in `canonical/emissive/`.

These define emitted light by state for traffic signals and similar assets.

Example:

- `canonical/emissive/emissive_vehicle_standard.emissive_profile.json`

### Camera profiles

Stored in `canonical/camera/`.

These define how spectra are weighted into an `RGB+NIR` camera response.

Current profiles:

- `camera_reference_rgb_nir_v1`
- `camera_reference_rgb_nir_v2`
- `camera_reference_rgb_nir_v3`

### Scenarios

Stored in `canonical/scenarios/`.

These define scene conditions such as:

- illuminant
- atmosphere
- wet/dry state
- active camera profile

### Validation scenes

Stored in `canonical/scenes/`.

These are assembled test environments such as:

- `scene_sign_test_lane`
- `scene_signalized_intersection`
- `scene_night_retroreflection`
- `scene_wet_road_braking`

## How Files Relate

### Example: stop sign

For `sign_stop`, the chain is:

1. `canonical/manifests/sign_stop.asset_manifest.json`
2. `canonical/geometry/usd/sign_stop.usda`
3. `canonical/templates/signs/sign_stop.svg`
4. linked materials such as `mat_sign_stop_red` and `mat_sign_white`
5. linked spectral curves in `canonical/spectra/`

### Example: traffic signal

For `signal_vehicle_vertical_3_aspect`, the chain is:

1. `canonical/manifests/signal_vehicle_vertical_3_aspect.asset_manifest.json`
2. `canonical/geometry/usd/signal_vehicle_vertical_3_aspect.usda`
3. off-state lens and housing materials
4. `canonical/emissive/emissive_vehicle_standard.emissive_profile.json`
5. signal SPD curves in `canonical/spectra/`

### Example: wet asphalt

For `road_asphalt_wet`, the chain is:

1. `canonical/manifests/road_asphalt_wet.asset_manifest.json`
2. `canonical/geometry/usd/road_asphalt_wet.usda`
3. `canonical/materials/mat_asphalt_wet.spectral_material.json`
4. `canonical/spectra/mat_asphalt_wet_reflectance.npz`

## Where to Look First

If you want to understand:

- what an object is: start with `canonical/manifests/`
- how it looks in 3D: open `canonical/geometry/usd/`
- what material it uses: open `canonical/materials/`
- what spectral data backs it: open `canonical/spectra/`
- how signals emit light: open `canonical/emissive/`
- how camera weighting works: open `canonical/camera/`
- how assets are tested together: open `canonical/scenes/` and `validation/reports/`

## Key Point

This repo does not store one asset in one file.

Each created simulation asset is a bundle of:

- geometry
- semantic metadata
- material metadata
- spectral data
- optional emissive state logic
- optional scenario/camera bindings

That split is intentional because the repo is built for camera simulation, not just for rendering one mesh.
