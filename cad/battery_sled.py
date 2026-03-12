"""
Battery Sled + Base Cap — CadQuery Script

Generates two parts:
1. Battery sled: cylindrical carrier that holds the recovered vape cell
   with spring contact pocket and polarity key
2. Base cap: twist-lock (bayonet) cap for tool-free battery access

Usage:
    pip install cadquery
    python battery_sled.py

Outputs:
    battery_sled.step, battery_sled.stl
    base_cap.step, base_cap.stl
"""

import cadquery as cq
from config import (
    BATTERY_CAVITY_DIAMETER, BATTERY_CAVITY_LENGTH,
    BATTERY_COMPARTMENT_LENGTH, OUTER_DIAMETER, INNER_DIAMETER,
    WALL_THICKNESS, FILLET_RADIUS,
    SPRING_CONTACT_DIAMETER, SPRING_CONTACT_DEPTH,
    BAYONET_LUG_WIDTH, BAYONET_LUG_HEIGHT, BAYONET_CLEARANCE,
    NUM_BAYONET_LUGS, BASE_CAP_LENGTH,
)
import math

# ─────────────────────────────────────────────────────────────────────────────
# BATTERY SLED
# ─────────────────────────────────────────────────────────────────────────────

sled_od = INNER_DIAMETER - 0.4  # slight clearance inside body shell
sled_id = BATTERY_CAVITY_DIAMETER
sled_length = BATTERY_COMPARTMENT_LENGTH

# Main cylindrical sled body
sled = (
    cq.Workplane("XY")
    .circle(sled_od / 2)
    .circle(sled_id / 2)
    .extrude(sled_length)
)

# Spring contact pocket at the top (positive terminal)
sled = (
    sled
    .faces(">Z")
    .workplane()
    .hole(SPRING_CONTACT_DIAMETER, SPRING_CONTACT_DEPTH)
)

# Polarity key — asymmetric notch on one side of the cavity wall
# This prevents reverse battery insertion
key_width = 2.0   # mm
key_depth = 1.5   # mm
key_height = sled_length

sled = (
    sled
    .faces("<Z")
    .workplane()
    .transformed(offset=(sled_id / 2 + key_depth / 2, 0, key_height / 2))
    .rect(key_depth, key_width)
    .cutBlind(key_height)
)

# Fillet the top edge for smooth insertion
sled = sled.edges("|Z").fillet(FILLET_RADIUS)

# ─────────────────────────────────────────────────────────────────────────────
# BASE CAP (Twist-Lock / Bayonet)
# ─────────────────────────────────────────────────────────────────────────────

cap_od = OUTER_DIAMETER
cap_id = INNER_DIAMETER + BAYONET_CLEARANCE * 2
cap_length = BASE_CAP_LENGTH

# Main cap body — short cylinder
base_cap = (
    cq.Workplane("XY")
    .circle(cap_od / 2)
    .extrude(cap_length)
)

# Hollow out most of the interior to save material
base_cap = (
    base_cap
    .faces(">Z")
    .workplane()
    .hole(cap_id - WALL_THICKNESS, cap_length - WALL_THICKNESS)
)

# Bayonet lugs — protruding tabs on the cap skirt
# These engage with L-shaped slots in the body shell
lug_radial_pos = cap_id / 2 - 0.5  # position on inner skirt
for i in range(NUM_BAYONET_LUGS):
    angle = i * (360 / NUM_BAYONET_LUGS)
    rad = math.radians(angle)
    x = lug_radial_pos * math.cos(rad)
    y = lug_radial_pos * math.sin(rad)

    lug = (
        cq.Workplane("XY")
        .transformed(offset=(x, y, cap_length - BAYONET_LUG_HEIGHT))
        .rect(BAYONET_LUG_WIDTH, WALL_THICKNESS * 0.6)
        .extrude(BAYONET_LUG_HEIGHT)
    )
    base_cap = base_cap.union(lug)

# Flat contact pad recess on inner face (negative terminal)
contact_pad_dia = 6.0  # mm
contact_pad_depth = 0.8  # mm recess for soldered pad

base_cap = (
    base_cap
    .faces(">Z")
    .workplane()
    .hole(contact_pad_dia, contact_pad_depth)
)

# Rounded bottom edge for aesthetics
base_cap = base_cap.edges("<Z").fillet(1.0)

# ─────────────────────────────────────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cq.exporters.export(sled, "battery_sled.step")
    cq.exporters.export(sled, "battery_sled.stl")
    print("Exported: battery_sled.step, battery_sled.stl")

    cq.exporters.export(base_cap, "base_cap.step")
    cq.exporters.export(base_cap, "base_cap.stl")
    print("Exported: base_cap.step, base_cap.stl")
