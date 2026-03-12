"""
Assembly — CadQuery Script

Imports all part scripts and positions them in correct assembly order.
Generates both an assembled view and an exploded view for documentation.

Usage:
    pip install cadquery
    python assembly.py

Outputs:
    assembly_closed.step   — fully assembled device
    assembly_exploded.step — exploded view with parts separated
"""

import cadquery as cq
from config import (
    OUTER_DIAMETER, TOTAL_LENGTH,
    BASE_CAP_LENGTH, BATTERY_COMPARTMENT_LENGTH,
    BODY_LENGTH, MOUTHPIECE_LENGTH,
    CARTRIDGE_LENGTH, CARTRIDGE_OD,
)

# ─────────────────────────────────────────────────────────────────────────────
# IMPORT INDIVIDUAL PARTS
# ─────────────────────────────────────────────────────────────────────────────

# Import part modules
from battery_sled import sled as battery_sled, base_cap
from body_shell import right_half as body_right, left_half as body_left
from mouthpiece import mouthpiece
from cartridge import cartridge
from pcb_bracket import bracket as pcb_bracket

# ─────────────────────────────────────────────────────────────────────────────
# ASSEMBLY POSITIONS (Z=0 is bottom of base cap)
# ─────────────────────────────────────────────────────────────────────────────

# Z-axis stack from bottom to top:
z_base_cap = 0
z_body_shell = BASE_CAP_LENGTH
z_battery_sled = BASE_CAP_LENGTH  # sits inside body at base
z_pcb_bracket = BASE_CAP_LENGTH + BATTERY_COMPARTMENT_LENGTH + 5  # above battery floor
z_cartridge = TOTAL_LENGTH - MOUTHPIECE_LENGTH - CARTRIDGE_LENGTH
z_mouthpiece = TOTAL_LENGTH - MOUTHPIECE_LENGTH

# ─────────────────────────────────────────────────────────────────────────────
# CLOSED ASSEMBLY
# ─────────────────────────────────────────────────────────────────────────────

assembly_closed = cq.Assembly()

assembly_closed.add(
    base_cap,
    name="base_cap",
    loc=cq.Location((0, 0, z_base_cap)),
    color=cq.Color(0.3, 0.3, 0.3, 1),  # dark gray
)

assembly_closed.add(
    body_right,
    name="body_shell_right",
    loc=cq.Location((0, 0, z_body_shell)),
    color=cq.Color(0.85, 0.85, 0.85, 1),  # light gray
)

assembly_closed.add(
    body_left,
    name="body_shell_left",
    loc=cq.Location((0, 0, z_body_shell)),
    color=cq.Color(0.85, 0.85, 0.85, 0.6),  # light gray, semi-transparent
)

assembly_closed.add(
    battery_sled,
    name="battery_sled",
    loc=cq.Location((0, 0, z_battery_sled)),
    color=cq.Color(0.2, 0.6, 0.2, 1),  # green
)

assembly_closed.add(
    pcb_bracket,
    name="pcb_bracket",
    loc=cq.Location((0, 0, z_pcb_bracket)),
    color=cq.Color(0.0, 0.5, 0.8, 1),  # blue
)

assembly_closed.add(
    cartridge,
    name="cartridge",
    loc=cq.Location((0, 0, z_cartridge)),
    color=cq.Color(0.9, 0.6, 0.1, 1),  # orange
)

assembly_closed.add(
    mouthpiece,
    name="mouthpiece",
    loc=cq.Location((0, 0, z_mouthpiece)),
    color=cq.Color(0.2, 0.2, 0.2, 1),  # near black
)

# ─────────────────────────────────────────────────────────────────────────────
# EXPLODED VIEW (parts spread apart along Z axis)
# ─────────────────────────────────────────────────────────────────────────────

explode_gap = 15  # mm gap between parts in exploded view

assembly_exploded = cq.Assembly()

ez = 0  # running Z position for exploded layout

assembly_exploded.add(
    base_cap,
    name="base_cap",
    loc=cq.Location((0, 0, ez)),
    color=cq.Color(0.3, 0.3, 0.3, 1),
)
ez += BASE_CAP_LENGTH + explode_gap

assembly_exploded.add(
    battery_sled,
    name="battery_sled",
    loc=cq.Location((0, 0, ez)),
    color=cq.Color(0.2, 0.6, 0.2, 1),
)
ez += BATTERY_COMPARTMENT_LENGTH + explode_gap

# Offset shell halves laterally for visibility
shell_lateral_offset = OUTER_DIAMETER * 0.6

assembly_exploded.add(
    body_right,
    name="body_shell_right",
    loc=cq.Location((shell_lateral_offset, 0, ez)),
    color=cq.Color(0.85, 0.85, 0.85, 1),
)

assembly_exploded.add(
    body_left,
    name="body_shell_left",
    loc=cq.Location((-shell_lateral_offset, 0, ez)),
    color=cq.Color(0.85, 0.85, 0.85, 1),
)
ez += BODY_LENGTH + BATTERY_COMPARTMENT_LENGTH + explode_gap

assembly_exploded.add(
    pcb_bracket,
    name="pcb_bracket",
    loc=cq.Location((0, 0, ez)),
    color=cq.Color(0.0, 0.5, 0.8, 1),
)
ez += 10 + explode_gap

assembly_exploded.add(
    cartridge,
    name="cartridge",
    loc=cq.Location((0, 0, ez)),
    color=cq.Color(0.9, 0.6, 0.1, 1),
)
ez += CARTRIDGE_LENGTH + explode_gap

assembly_exploded.add(
    mouthpiece,
    name="mouthpiece",
    loc=cq.Location((0, 0, ez)),
    color=cq.Color(0.2, 0.2, 0.2, 1),
)

# ─────────────────────────────────────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    assembly_closed.save("assembly_closed.step")
    print("Exported: assembly_closed.step")

    assembly_exploded.save("assembly_exploded.step")
    print("Exported: assembly_exploded.step")

    print("\nTo view: open .step files in FreeCAD, Fusion 360, or Onshape")
    print("To render for paper: use FreeCAD screenshot or CQ-editor")
