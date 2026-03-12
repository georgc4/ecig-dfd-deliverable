# CAD — Universal Removable Battery E-Cigarette Prototype

3D-printable prototype assembly for the DfD-redesigned electronic cigarette with universal removable battery.

## Quick Start

### Option A: Run CadQuery Python Scripts

```bash
# Install CadQuery
pip install cadquery

# 1. Measure your recovered vape battery and edit config.py:
#    BATTERY_DIAMETER = <measured_diameter_mm>
#    BATTERY_LENGTH   = <measured_length_mm>

# 2. Generate all parts
cd cad/
python battery_sled.py    # → battery_sled.stl, base_cap.stl
python body_shell.py      # → body_shell_right.stl, body_shell_left.stl
python mouthpiece.py      # → mouthpiece.stl
python cartridge.py       # → cartridge.stl
python pcb_bracket.py     # → pcb_bracket.stl

# 3. Generate assembly views
python assembly.py        # → assembly_closed.step, assembly_exploded.step
```

### Option B: Manual CAD from Design Spec

Open `DESIGN_SPEC.md` for a complete dimensioned specification with per-part modeling steps. Use with Fusion 360, Onshape, SolidWorks, or any parametric CAD tool.

## File Structure

```
cad/
├── config.py           # Shared dimensions — EDIT BATTERY SIZE HERE
├── battery_sled.py     # Battery carrier + base cap
├── body_shell.py       # Clamshell body (left & right halves)
├── mouthpiece.py       # Tapered mouthpiece with snap-fit
├── cartridge.py        # Atomizer/reservoir cartridge sleeve
├── pcb_bracket.py      # PCB mount bracket
├── assembly.py         # Full assembly + exploded view
├── DESIGN_SPEC.md      # Human-readable CAD spec for manual modeling
└── README.md           # This file
```

## Before You Print — Measure Your Battery

1. Carefully extract the battery cell from the disposable vape
2. Measure diameter and length with calipers (to 0.1 mm)
3. Update `config.py`:
   ```python
   BATTERY_DIAMETER = 12.0   # ← your measured value
   BATTERY_LENGTH = 40.0     # ← your measured value
   ```
4. Regenerate all parts (the clearances are calculated automatically)

## Bill of Materials

| Component | Spec | Qty | ~Cost |
|-----------|------|-----|-------|
| Battery spring contact | Keystone 5230 or equiv, gold-plated | 2 | $1.50 |
| JST-PH 2-pin connector pair | 2.0 mm pitch, male + female | 2 pairs | $2.00 |
| Neodymium disc magnets (optional) | 3 mm x 1 mm, N52 | 4 | $3.00 |
| Battery cell | Recovered from existing disposable vape | 1 | $0 |
| PETG filament | 1.75 mm, any color | ~50 g | $2.00 |
| **Total** | | | **~$8.50** |

## Print Settings

| Parameter | Value |
|-----------|-------|
| Material | PETG |
| Nozzle | 0.4 mm |
| Layer height | 0.2 mm |
| Infill | 20% gyroid |
| Walls | 3 perimeters |
| Support | Minimal (bayonet slots only if needed) |

### Print Order (recommended)

1. **Battery sled** — quick print, test battery fit first
2. **Base cap** — test bayonet lug fit with sled
3. **Body shell right half** — longest print, test snap-fits
4. **Body shell left half** — test clamshell closure
5. **Cartridge** — test slide-in fit
6. **PCB bracket** — test internal fit
7. **Mouthpiece** — test snap onto body top

## Assembly

1. Insert battery sled into body shell right half
2. Place PCB bracket above battery floor
3. Connect JST-PH wires
4. Close with left half (press until 4 clicks)
5. Insert cartridge from top
6. Snap on mouthpiece
7. Drop battery into sled through open base
8. Twist-lock base cap (quarter-turn clockwise)

**Battery removal**: Quarter-turn base cap counter-clockwise, tilt, battery slides out. <5 seconds, no tools.

## Generating Paper Figures

After building the assembly:
1. Open `assembly_exploded.step` in FreeCAD or your CAD tool
2. Set orthographic front view
3. Export as PDF/PNG → `../figures/exploded_view_dfd.pdf`
4. Set cross-section view → `../figures/cross_section.pdf`
5. Photo of printed prototype → `../figures/prototype_photo.jpg`
