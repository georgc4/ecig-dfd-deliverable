"""
Mouthpiece — CadQuery Script

Tapered cylinder with snap-fit ring at base and internal air channel.
Designed for comfort and sleek aesthetics.

Usage:
    pip install cadquery
    python mouthpiece.py

Outputs:
    mouthpiece.step, mouthpiece.stl
"""

import cadquery as cq
from config import (
    OUTER_DIAMETER, WALL_THICKNESS, FILLET_RADIUS,
    MOUTHPIECE_LENGTH, MOUTHPIECE_TIP_DIAMETER, AIR_CHANNEL_DIAMETER,
    SNAP_CATCH_DEPTH, SNAP_FIT_CLEARANCE,
)

# ─────────────────────────────────────────────────────────────────────────────
# MOUTHPIECE — tapered cylinder
# ─────────────────────────────────────────────────────────────────────────────

base_radius = OUTER_DIAMETER / 2
tip_radius = MOUTHPIECE_TIP_DIAMETER / 2
length = MOUTHPIECE_LENGTH
air_r = AIR_CHANNEL_DIAMETER / 2

# Outer tapered profile via loft between two circles
mouthpiece = (
    cq.Workplane("XY")
    .circle(base_radius)
    .workplane(offset=length)
    .circle(tip_radius)
    .loft()
)

# Hollow out the air channel
air_channel = (
    cq.Workplane("XY")
    .circle(air_r)
    .extrude(length)
)
mouthpiece = mouthpiece.cut(air_channel)

# ── Snap-fit ring at base ──
# An internal lip that snaps into the body shell top opening
snap_ring_height = 3.0   # mm
snap_ring_od = OUTER_DIAMETER - SNAP_FIT_CLEARANCE * 2  # fits inside body ID
snap_ring_id = OUTER_DIAMETER - 2 * WALL_THICKNESS + SNAP_FIT_CLEARANCE
snap_ring_wall = (snap_ring_od - snap_ring_id) / 2

snap_ring = (
    cq.Workplane("XY")
    .workplane(offset=-snap_ring_height)
    .circle(snap_ring_od / 2)
    .circle(snap_ring_id / 2)
    .extrude(snap_ring_height)
)

# Small catch bump on the snap ring
catch_bump = (
    cq.Workplane("XY")
    .workplane(offset=-snap_ring_height)
    .circle(snap_ring_od / 2 + SNAP_CATCH_DEPTH * 0.4)
    .circle(snap_ring_od / 2)
    .extrude(1.5)
)

mouthpiece = mouthpiece.union(snap_ring).union(catch_bump)

# ── Comfort fillet on tip ──
mouthpiece = mouthpiece.edges(">Z").fillet(min(tip_radius * 0.3, 2.0))

# ── Base edge fillet ──
mouthpiece = mouthpiece.edges("<Z and not %Circle").fillet(FILLET_RADIUS)

# ─────────────────────────────────────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cq.exporters.export(mouthpiece, "mouthpiece.step")
    cq.exporters.export(mouthpiece, "mouthpiece.stl")
    print("Exported: mouthpiece.step, mouthpiece.stl")
