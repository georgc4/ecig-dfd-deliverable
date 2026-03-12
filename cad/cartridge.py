"""
Cartridge Sleeve (Atomizer Mock) — CadQuery Script

Slide-in cylindrical cartridge representing the atomizer/reservoir module.
Includes O-ring groove for snug fit and contact pad recesses at the bottom.

Usage:
    pip install cadquery
    python cartridge.py

Outputs:
    cartridge.step, cartridge.stl
"""

import cadquery as cq
from config import (
    CARTRIDGE_OD, CARTRIDGE_LENGTH, CARTRIDGE_WALL,
    FILLET_RADIUS,
)

# ─────────────────────────────────────────────────────────────────────────────
# CARTRIDGE SLEEVE
# ─────────────────────────────────────────────────────────────────────────────

od = CARTRIDGE_OD
length = CARTRIDGE_LENGTH
wall = CARTRIDGE_WALL

# Main hollow cylinder
cartridge = (
    cq.Workplane("XY")
    .circle(od / 2)
    .circle(od / 2 - wall)
    .extrude(length)
)

# ── Closed top ──
# The top end is capped (e-liquid reservoir sealed end)
cap_thickness = 1.5  # mm
top_cap = (
    cq.Workplane("XY")
    .workplane(offset=length - cap_thickness)
    .circle(od / 2 - wall)
    .extrude(cap_thickness)
)
cartridge = cartridge.union(top_cap)

# ── Air channel through the center ──
air_hole_dia = 3.0  # mm
cartridge = (
    cartridge
    .faces(">Z")
    .workplane()
    .hole(air_hole_dia, length)
)

# ── O-ring groove near the base ──
# For snug friction fit inside the body shell
oring_groove_dia = od - 0.4  # slightly recessed from OD
oring_groove_width = 1.5     # mm
oring_groove_depth = 0.8     # mm
oring_z_from_base = 3.0      # mm up from the bottom

oring_groove = (
    cq.Workplane("XY")
    .workplane(offset=oring_z_from_base)
    .circle(od / 2)
    .circle(od / 2 - oring_groove_depth)
    .extrude(oring_groove_width)
)
cartridge = cartridge.cut(oring_groove)

# ── Contact pad recesses at bottom ──
# Two flat areas for electrical contact with spring pins from body
contact_width = 3.0   # mm
contact_height = 3.0  # mm
contact_depth = 0.5   # mm recess
contact_spacing = 5.0  # mm apart (center to center)

for offset_x in [-contact_spacing / 2, contact_spacing / 2]:
    pad_recess = (
        cq.Workplane("XY")
        .transformed(offset=(offset_x, 0, 0))
        .rect(contact_width, contact_height)
        .extrude(contact_depth)
    )
    cartridge = cartridge.cut(pad_recess)

# ── Fillet top edge for smooth insertion ──
cartridge = cartridge.edges(">Z").fillet(FILLET_RADIUS)

# ─────────────────────────────────────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cq.exporters.export(cartridge, "cartridge.step")
    cq.exporters.export(cartridge, "cartridge.stl")
    print("Exported: cartridge.step, cartridge.stl")
