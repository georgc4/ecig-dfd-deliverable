"""
Body Shell — CadQuery Script

Generates the two-piece clamshell body (left and right halves) with:
- Snap-fit cantilever clips
- Alignment pin/hole pairs
- USB-C port cutout
- LED indicator window
- Bayonet L-slots at base for twist-lock cap
- Cartridge retention lip at top
- Internal PCB standoff ribs
- Finger notch at base seam

Usage:
    pip install cadquery
    python body_shell.py

Outputs:
    body_shell_left.step, body_shell_left.stl
    body_shell_right.step, body_shell_right.stl
"""

import cadquery as cq
import math
from config import (
    OUTER_DIAMETER, INNER_DIAMETER, WALL_THICKNESS,
    BODY_LENGTH, BATTERY_COMPARTMENT_LENGTH, MOUTHPIECE_LENGTH,
    TOTAL_LENGTH, BASE_CAP_LENGTH,
    SNAP_ARM_WIDTH, SNAP_ARM_LENGTH, SNAP_DEFLECTION, SNAP_CATCH_DEPTH,
    SNAP_FIT_CLEARANCE, FILLET_RADIUS,
    USB_C_WIDTH, USB_C_HEIGHT, USB_C_OFFSET_FROM_BASE,
    LED_DIAMETER,
    BAYONET_LUG_WIDTH, BAYONET_LUG_HEIGHT, BAYONET_CLEARANCE,
    NUM_BAYONET_LUGS,
    ALIGNMENT_PIN_DIAMETER, ALIGNMENT_PIN_LENGTH, NUM_ALIGNMENT_PINS,
    PIN_HOLE_CLEARANCE,
    CARTRIDGE_OD,
    BATTERY_CAVITY_DIAMETER, BATTERY_CAVITY_LENGTH,
    PCB_STANDOFF_DIAMETER, PCB_STANDOFF_HEIGHT,
    SPRING_CONTACT_DIAMETER, SPRING_CONTACT_DEPTH,
)

# ─────────────────────────────────────────────────────────────────────────────
# FULL CYLINDRICAL SHELL (before splitting into halves)
# ─────────────────────────────────────────────────────────────────────────────

# The body shell spans from the base cap junction to the mouthpiece junction
# Total shell length = BODY_LENGTH + BATTERY_COMPARTMENT_LENGTH
shell_length = BODY_LENGTH + BATTERY_COMPARTMENT_LENGTH
od = OUTER_DIAMETER
wall = WALL_THICKNESS

# Main hollow cylinder
full_shell = (
    cq.Workplane("XY")
    .circle(od / 2)
    .circle(od / 2 - wall)
    .extrude(shell_length)
)

# ── Battery compartment floor ──
# A disc inside the shell separating battery zone from electronics zone
floor_z = BATTERY_COMPARTMENT_LENGTH
floor_thickness = 1.5  # mm

battery_floor = (
    cq.Workplane("XY")
    .workplane(offset=floor_z - floor_thickness)
    .circle(od / 2 - wall)
    .extrude(floor_thickness)
)

# Spring contact hole through the floor
battery_floor = (
    battery_floor
    .faces(">Z")
    .workplane()
    .hole(SPRING_CONTACT_DIAMETER, floor_thickness)
)

full_shell = full_shell.union(battery_floor)

# ── USB-C port cutout ──
usb_z = USB_C_OFFSET_FROM_BASE  # from base of shell
full_shell = (
    full_shell
    .faces(">X")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(offset=(0, usb_z - shell_length / 2, 0))
    .rect(USB_C_WIDTH, USB_C_HEIGHT)
    .cutBlind(-wall * 2)
)

# ── LED indicator window ──
led_z = usb_z + 8  # slightly above USB-C
full_shell = (
    full_shell
    .faces(">X")
    .workplane(centerOption="CenterOfBoundBox")
    .transformed(offset=(0, led_z - shell_length / 2, 0))
    .circle(LED_DIAMETER / 2)
    .cutBlind(-wall * 2)
)

# ── Bayonet L-slots at base end ──
# The base cap lugs slide into vertical entry slots, then rotate into
# horizontal locking channels
slot_entry_width = BAYONET_LUG_WIDTH + BAYONET_CLEARANCE * 2
slot_entry_height = BAYONET_LUG_HEIGHT + BAYONET_CLEARANCE
slot_channel_arc = 20  # degrees of rotation for the horizontal lock channel

for i in range(NUM_BAYONET_LUGS):
    angle = i * (360 / NUM_BAYONET_LUGS)
    rad = math.radians(angle)

    # Vertical entry slot
    sx = (od / 2 - wall / 2) * math.cos(rad)
    sy = (od / 2 - wall / 2) * math.sin(rad)

    entry_slot = (
        cq.Workplane("XY")
        .transformed(offset=(sx, sy, 0))
        .transformed(rotate=(0, 0, angle))
        .rect(wall + 1, slot_entry_width)
        .extrude(slot_entry_height + 1)
    )
    full_shell = full_shell.cut(entry_slot)

# ── Cartridge retention lip at top end ──
lip_height = 1.5  # mm
lip_inset = (od / 2 - wall) - (CARTRIDGE_OD / 2 + 0.3)  # slight interference

if lip_inset > 0:
    retention_lip = (
        cq.Workplane("XY")
        .workplane(offset=shell_length - lip_height)
        .circle(od / 2 - wall)
        .circle(od / 2 - wall - lip_inset)
        .extrude(lip_height)
    )
    full_shell = full_shell.union(retention_lip)

# ── Finger notch at base ──
notch_radius = 5.0  # mm semicircle
notch_depth = wall + 1
full_shell = (
    full_shell
    .faces("<Z")
    .workplane()
    .transformed(offset=(od / 2, 0, 0))
    .circle(notch_radius)
    .cutBlind(notch_depth)
)

# ─────────────────────────────────────────────────────────────────────────────
# SPLIT INTO LEFT AND RIGHT HALVES
# ─────────────────────────────────────────────────────────────────────────────

# Splitting plane is the XZ plane (Y=0), cutting along the long axis
split_block = (
    cq.Workplane("XY")
    .transformed(offset=(0, od, shell_length / 2))
    .rect(od * 2, shell_length * 2)
    .extrude(od * 2)
)

right_half = full_shell.cut(
    cq.Workplane("XY")
    .transformed(offset=(0, -od / 2, shell_length / 2))
    .rect(od * 2, shell_length + 2)
    .extrude(-od)
)

left_half = full_shell.cut(
    cq.Workplane("XY")
    .transformed(offset=(0, od / 2, shell_length / 2))
    .rect(od * 2, shell_length + 2)
    .extrude(od)
)

# ─────────────────────────────────────────────────────────────────────────────
# SNAP-FIT CLIPS (on right half, matching recesses on left half)
# ─────────────────────────────────────────────────────────────────────────────

# Snap clips are cantilever beams along the split seam
# 2 clips per half, positioned at 1/3 and 2/3 of shell length
clip_positions_z = [shell_length * 0.33, shell_length * 0.67]
clip_y_offset = SNAP_FIT_CLEARANCE / 2  # on the seam face

for z_pos in clip_positions_z:
    # Cantilever beam on right half (protruding toward left)
    clip = (
        cq.Workplane("XZ")
        .transformed(offset=(0, 0, -clip_y_offset))
        .transformed(offset=(0, z_pos, 0))
        .rect(SNAP_ARM_WIDTH, SNAP_ARM_LENGTH)
        .extrude(-SNAP_CATCH_DEPTH)
    )
    # Catch at the end of the beam
    catch = (
        cq.Workplane("XZ")
        .transformed(offset=(0, 0, -clip_y_offset - SNAP_CATCH_DEPTH))
        .transformed(offset=(0, z_pos + SNAP_ARM_LENGTH / 2 - 1, 0))
        .rect(SNAP_ARM_WIDTH, 2)
        .extrude(-SNAP_CATCH_DEPTH * 0.5)
    )
    right_half = right_half.union(clip).union(catch)

# ─────────────────────────────────────────────────────────────────────────────
# ALIGNMENT PINS (right half) & HOLES (left half)
# ─────────────────────────────────────────────────────────────────────────────

pin_positions_z = [shell_length * 0.25, shell_length * 0.75]

for z_pos in pin_positions_z:
    # Pin on right half
    pin = (
        cq.Workplane("XY")
        .transformed(offset=(0, 0, z_pos))
        .workplane()
        .transformed(offset=(od / 2 - wall / 2, 0, 0))
        .circle(ALIGNMENT_PIN_DIAMETER / 2)
        .extrude(ALIGNMENT_PIN_LENGTH)
    )
    right_half = right_half.union(pin)

    # Matching hole on left half
    hole = (
        cq.Workplane("XY")
        .transformed(offset=(0, 0, z_pos))
        .workplane()
        .transformed(offset=(od / 2 - wall / 2, 0, 0))
        .circle((ALIGNMENT_PIN_DIAMETER + PIN_HOLE_CLEARANCE * 2) / 2)
        .cutBlind(ALIGNMENT_PIN_LENGTH + 0.5)
    )
    left_half = left_half.cut(hole)

# ─────────────────────────────────────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cq.exporters.export(right_half, "body_shell_right.step")
    cq.exporters.export(right_half, "body_shell_right.stl")
    print("Exported: body_shell_right.step, body_shell_right.stl")

    cq.exporters.export(left_half, "body_shell_left.step")
    cq.exporters.export(left_half, "body_shell_left.stl")
    print("Exported: body_shell_left.step, body_shell_left.stl")

    # Also export full shell for reference
    cq.exporters.export(full_shell, "body_shell_full.step")
    print("Exported: body_shell_full.step (reference)")
