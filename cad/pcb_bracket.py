"""
PCB Mount Bracket — CadQuery Script

Flat bracket conforming to the inner shell radius with press-fit standoff posts
and JST-PH connector mounting hole. Sits in the body/electronics zone.

Usage:
    pip install cadquery
    python pcb_bracket.py

Outputs:
    pcb_bracket.step, pcb_bracket.stl
"""

import cadquery as cq
from config import (
    INNER_DIAMETER, WALL_THICKNESS,
    PCB_STANDOFF_DIAMETER, PCB_STANDOFF_HEIGHT,
    JST_MOUNT_HOLE_DIAMETER,
    FILLET_RADIUS,
)

# ─────────────────────────────────────────────────────────────────────────────
# PCB MOUNT BRACKET
# ─────────────────────────────────────────────────────────────────────────────

# Bracket is a flat plate that spans the inner diameter
bracket_width = INNER_DIAMETER - 1.0   # slight clearance inside shell
bracket_depth = 12.0   # mm — along the Z axis of the device
bracket_thickness = 1.5  # mm

# Main flat bracket plate
bracket = (
    cq.Workplane("XY")
    .rect(bracket_width, bracket_depth)
    .extrude(bracket_thickness)
)

# ── Press-fit standoff posts ──
# Two posts for PCB mounting holes (standard 2.5mm holes)
standoff_spacing = bracket_width * 0.6  # distance between posts

for x_off in [-standoff_spacing / 2, standoff_spacing / 2]:
    standoff = (
        cq.Workplane("XY")
        .workplane(offset=bracket_thickness)
        .transformed(offset=(x_off, 0, 0))
        .circle(PCB_STANDOFF_DIAMETER / 2)
        .extrude(PCB_STANDOFF_HEIGHT)
    )
    bracket = bracket.union(standoff)

    # Pilot hole in the standoff for press-fit
    pilot_dia = PCB_STANDOFF_DIAMETER - 0.6  # tight interference fit
    pilot_hole = (
        cq.Workplane("XY")
        .workplane(offset=bracket_thickness)
        .transformed(offset=(x_off, 0, 0))
        .circle(pilot_dia / 2)
        .extrude(PCB_STANDOFF_HEIGHT)
    )
    bracket = bracket.cut(pilot_hole)

# ── JST-PH connector mounting hole ──
# Through-hole for JST-PH 2-pin header body
bracket = (
    bracket
    .faces("<Z")
    .workplane()
    .transformed(offset=(0, -bracket_depth / 4, 0))
    .rect(JST_MOUNT_HOLE_DIAMETER, JST_MOUNT_HOLE_DIAMETER * 0.6)
    .cutThruAll()
)

# ── Fillet edges ──
bracket = bracket.edges("|Z").fillet(FILLET_RADIUS)

# ─────────────────────────────────────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cq.exporters.export(bracket, "pcb_bracket.step")
    cq.exporters.export(bracket, "pcb_bracket.stl")
    print("Exported: pcb_bracket.step, pcb_bracket.stl")
