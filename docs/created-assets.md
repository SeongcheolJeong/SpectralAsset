# Created Assets

## Purpose

This file explains what the generator actually creates in this repository and how the created files relate to each other.

Current generated baseline:

- `142` assets
- `25` spectral materials
- `13` emissive profiles
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
- `sign_stop_weathered`
- `sign_yield`
- `sign_speed_limit_50`
- `sign_speed_limit_50_weathered`
- `sign_pedestrian_crossing_weathered`
- `sign_yield_weathered_heavy`
- `sign_no_entry_weathered_heavy`
- `sign_roundabout_mandatory`
- `sign_stop_ahead_text`
- `sign_construction_weathered_heavy`
- `sign_priority_road`
- `sign_hospital_arrow_right`
- `sign_parking_arrow_left`
- `sign_hotel_arrow_left`
- `sign_airport_arrow_right`
- `sign_truck_route_right`
- `sign_centre_left_text`
- `sign_one_way_text_left`
- `sign_one_way_text_right`
- `sign_detour_left_text`
- `sign_detour_right_text`
- `sign_bypass_right_text`

Each sign usually has:

- an SVG sign-face template in `canonical/templates/signs/`
- a USD geometry file in `canonical/geometry/usd/`
- an asset manifest in `canonical/manifests/`
- linked spectral materials such as `mat_sign_stop_red` and `mat_sign_white`
- optional weathering overlays such as `mat_sign_weathered_film`
- heavier weathering overlays such as `mat_sign_weathered_heavy_film`

The newer route/service additions now also include:

- service-direction panels such as hospital, parking, and hotel
- transport or logistics panels such as airport and truck-route signs
- locale-style wayfinding panels such as `CENTRE` and `BYPASS`

### `traffic_light`

These are signal housings such as:

- `signal_vehicle_vertical_3_aspect`
- `signal_vehicle_horizontal_3_aspect`
- `signal_protected_turn_4_aspect`
- `signal_beacon_amber_single`
- `signal_beacon_red_single`
- `signal_warning_dual_amber_horizontal`
- `signal_warning_dual_red_horizontal`
- `signal_lane_control_overhead_3_aspect`
- `signal_lane_control_reversible_2_aspect`
- `signal_transit_priority_vertical_4_aspect`
- `signal_transit_priority_horizontal_4_aspect`
- `signal_directional_arrow_left_3_aspect`
- `signal_directional_arrow_right_3_aspect`
- `signal_rail_crossing_dual_red_vertical`
- `signal_rail_crossing_dual_red_horizontal`

Each signal usually has:

- a USD geometry file
- an asset manifest
- off-state lens materials
- a linked emissive profile that defines what spectral curve is active in each state

The newer specialized signal heads now also include:

- lane-control state maps for red `X`, yellow merge arrow, and green open-lane arrow behavior
- transit-priority state maps for stop, caution, go, and call indications
- directional-arrow state maps for red, yellow, green, and flashing yellow arrow behavior
- rail-crossing state maps for left, right, or paired red flashing behavior

### `road_surface`

These are reusable road or pavement surfaces such as:

- `road_asphalt_dry`
- `road_asphalt_wet`
- `road_concrete`
- `road_asphalt_patched`
- `road_concrete_distressed`
- `road_asphalt_concrete_transition`
- `road_gutter_transition`
- `road_gravel_shoulder`
- `road_asphalt_gravel_transition`
- `road_construction_plate_patch`
- `road_asphalt_pothole_distressed`
- `road_eroded_shoulder_edge`
- `road_rural_crowned_lane`
- `road_dirt_track_dual_rut`
- `road_dirt_track_washout`
- `road_bridge_expansion_joint`
- `road_lane_drop_transition`
- `road_sidewalk_panel`

They mainly depend on spectral material definitions rather than complex state logic, but the newer variants now mix asphalt, concrete, steel-plate, and gravel proxy materials to represent repairs, rural shoulders, crowned rural lanes, dirt-track ruts, bridge-joint panels, lane-drop tapers, pothole distress, and edge-dropoff conditions.

### `road_marking`

These are markings such as:

- `marking_lane_white`
- `marking_lane_yellow`
- `marking_crosswalk`
- `marking_crosswalk_worn`
- `marking_stop_line`
- `marking_stop_line_worn`
- `marking_edge_line_white`
- `marking_edge_line_yellow`
- `marking_centerline_double_yellow`
- `marking_centerline_solid_dashed_yellow`
- `marking_arrow_straight_white`
- `marking_arrow_turn_left_white`
- `marking_arrow_turn_right_white`
- `marking_arrow_straight_right_white`
- `marking_merge_left_white`
- `marking_chevron_gore_white`
- `marking_hatched_median_yellow`
- `marking_hatched_island_white`
- `marking_lane_white_worn`
- `marking_raised_marker_white`
- `marking_raised_marker_yellow`
- `marking_raised_marker_bicolor`
- `marking_only_text_white`
- `marking_stop_text_white`
- `marking_bus_text_white`
- `marking_bike_text_white`
- `marking_bus_only_box_white`
- `marking_bus_stop_box_white`
- `marking_bike_box_white`
- `marking_loading_zone_box_white`
- `marking_transit_lane_panel_red`
- `marking_bike_lane_panel_green`

They use retroreflective or reflective material definitions and are important for camera visibility tests. The newer specialization pass now also covers bus/bike lane legends, boxed curbside/transit legends, red/green colored lane panels, hatched median/island channelization, and right-turn follow-up arrow families.

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
- `furniture_signal_side_mount_bracket`
- `furniture_signal_service_disconnect`
- `furniture_signal_meter_pedestal`
- `furniture_signal_mast_hanger`
- `furniture_signal_controller_cabinet`
- `furniture_signal_controller_cabinet_single`
- `furniture_signal_battery_backup_cabinet`
- `furniture_signal_junction_box`
- `furniture_utility_pull_box`
- `furniture_utility_transformer_padmount`
- `furniture_bus_stop_shelter`
- `furniture_bus_stop_totem`
- `furniture_bus_stop_bench`
- `furniture_utility_handhole_cluster`
- `furniture_service_bollard_pair`
- `furniture_utility_pole_concrete`
- `furniture_utility_pole_steel`
- `furniture_sign_back_octagon`
- `furniture_sign_back_round`
- `furniture_sign_back_triangle`
- `furniture_sign_back_square`
- `furniture_sign_back_rectangle_wide`
- `furniture_sign_mount_bracket_single`
- `furniture_sign_mount_bracket_double`
- `furniture_sign_overhead_bracket`

The newest roadside-context pass adds transit-stop and curbside service detail so scenes can now place a shelter, stop marker, bench, grouped handholes, and protective service bollards instead of implying all curbside context through signs, poles, and cabinets alone.

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

Current specialized additions include:

- `emissive_lane_control_standard`
- `emissive_lane_control_reversible`
- `emissive_transit_priority_standard`
- `emissive_directional_arrow_standard`
- `emissive_rail_crossing_dual_red`

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
