# Design Specification: Universal Removable Battery E-Cigarette Assembly

**Version**: 1.0
**Target**: 3D-printed prototype (FDM, PETG)
**Battery**: Recovered cell from existing disposable vape
**CAD Software**: Fusion 360, Onshape, SolidWorks, or equivalent

---

## 1. Assembly Overview

The device is a cylindrical, pen-style e-cigarette body designed for:
- Tool-free battery removal in <5 seconds
- Clamshell housing with snap-fit clips (no screws, no adhesive)
- Twist-lock (bayonet) base cap for battery compartment access
- Slide-in atomizer cartridge
- Snap-fit mouthpiece

### Overall Dimensions

| Parameter | Value | Tolerance |
|-----------|-------|-----------|
| Outer diameter | 22.0 mm | +0/-0.3 mm |
| Total length (assembled) | 110.0 mm | +/-1.0 mm |
| Wall thickness | 2.5 mm | +/-0.2 mm |

### Module Stack (bottom to top)

```
Z = 0 mm    ┌──────────────────┐
             │  BASE CAP        │  8.0 mm
Z = 8 mm    ├──────────────────┤
             │  BATTERY         │  32.0 mm *
             │  COMPARTMENT     │
Z = 40 mm   ├──────────────────┤
             │  BODY /          │  50.0 mm
             │  ELECTRONICS     │
             │  (PCB + cartridge│
             │   zone)          │
Z = 90 mm   ├──────────────────┤
             │  MOUTHPIECE      │  20.0 mm
Z = 110 mm  └──────────────────┘

* Battery compartment length = 110 - 20 - 50 - 8 = 32 mm
  Adjust if recovered battery is longer
```

---

## 2. Part-by-Part Specifications

### Part 1: Base Cap (Twist-Lock)

**Function**: Closes the battery compartment. Quarter-turn bayonet locking.

```
    ┌────────────────────┐  ← Flat bottom (rounded fillet R=1.0)
    │                    │
    │   ┌────────────┐   │  ← Contact pad recess (dia 6.0, depth 0.8)
    │   │  (-)  pad  │   │
    │   └────────────┘   │
    │                    │  8.0 mm tall
    │  ┌─┐          ┌─┐ │  ← Bayonet lugs (2x, 180 deg apart)
    │  │L│          │L│ │    3.0 mm wide, 2.0 mm tall
    └──┘ └──────────┘ └─┘
         ← 22.0 mm →
```

| Feature | Dimension |
|---------|-----------|
| Outer diameter | 22.0 mm |
| Total height | 8.0 mm |
| Inner cavity diameter | 17.0 + 0.4 mm clearance = 17.4 mm |
| Inner cavity depth | 8.0 - 2.5 = 5.5 mm (wall at bottom) |
| Bayonet lug width | 3.0 mm |
| Bayonet lug height | 2.0 mm |
| Bayonet lug radial position | on inner skirt at r = 8.2 mm |
| Lug count | 2 (180 deg apart) |
| Contact pad recess | dia 6.0 mm, depth 0.8 mm, centered on inner face |
| Bottom edge fillet | R = 1.0 mm |

**Modeling steps**:
1. Extrude solid cylinder 22.0 dia x 8.0 mm
2. Shell from top face, leaving 2.5 mm bottom wall
3. Add 2 bayonet lugs on inner skirt wall (extrude rectangular pads)
4. Cut contact pad recess on inner bottom face
5. Fillet bottom outer edge R=1.0

---

### Part 2: Battery Sled / Carrier

**Function**: Holds the recovered vape battery cell inside the body shell. Spring contact pocket at top for positive terminal.

```
         ┌───────────┐  ← Spring contact pocket
         │  ○ (5mm)  │    (dia 5.0, depth 3.0)
    ┌────┤           ├────┐
    │    │           │    │
    │    │  BATTERY  │    │  32.0 mm tall
    │    │  CAVITY   │    │
    │    │           │    │
    │  ▌ │           │    │  ← Polarity key notch
    │    │           │    │    (2.0 x 1.5 mm, full height)
    └────┤           ├────┘
         └───────────┘
    ← sled OD: 16.6 mm →
    ← cavity ID: 12.5 mm →
```

| Feature | Dimension |
|---------|-----------|
| Sled outer diameter | INNER_DIAMETER - 0.4 = 16.6 mm |
| Cavity inner diameter | BATTERY_DIA + 0.5 mm |
| Sled height | 32.0 mm (= battery compartment length) |
| Spring contact pocket | dia 5.0 mm, depth 3.0 mm, centered on top face |
| Polarity key notch | 2.0 mm wide, 1.5 mm deep, full height, one side |

**NOTE**: Measure your recovered battery diameter and length with calipers. The cavity ID = measured_diameter + 0.5 mm. If the battery is longer than 30 mm, increase the battery compartment length in the body shell accordingly.

**Modeling steps**:
1. Extrude annular cylinder (sled_OD / cavity_ID) x sled_height
2. Cut spring contact pocket from top face (blind hole)
3. Cut polarity key notch (rectangular slot along one side of inner wall)
4. Fillet top outer edges R=0.5

---

### Part 3: Body Shell — Right Half

**Function**: One half of the clamshell housing. Contains snap-fit clips, alignment pins, USB-C cutout, LED window, bayonet slots, and internal features.

```
SIDE VIEW (right half, looking from split seam):

    ┌─── cartridge lip
    │  ┌──────────────────────┐  Z = 82 mm (shell top)
    │  │                      │
    │  │   ELECTRONICS ZONE   │
    │  │  ┌─PCB standoffs─┐   │
    │  │  │  ○         ○  │   │
    │  │  └───────────────┘   │
    │  │  ○ LED                │  Z = 23 mm
    │  │  □ USB-C              │  Z = 15 mm (center)
    │  ├──────────────────────┤  Z = 32 mm (battery floor)
    │  │                      │
    │  │  BATTERY ZONE        │
    │  │  (sled sits here)    │
    │  │                      │
    │  ├──L-slot──────L-slot──┤  Z = 0 (bayonet entry slots)
    └──┘     finger notch     └──

    ← 11.0 mm (half of 22mm) →
```

| Feature | Dimension |
|---------|-----------|
| Shell outer diameter | 22.0 mm |
| Shell inner diameter | 17.0 mm |
| Shell total length | 82.0 mm (body + battery compartment) |
| Split plane | Y = 0 (XZ plane, along long axis) |

**Snap-fit clips** (2 per half):

| Parameter | Value |
|-----------|-------|
| Clip positions (Z from base) | 27 mm and 55 mm |
| Cantilever beam width | 1.5 mm |
| Cantilever beam length | 10.0 mm |
| Beam thickness | 0.8 mm |
| Catch depth | 0.8 mm |
| Catch length | 2.0 mm |

**Alignment pins** (on right half):

| Parameter | Value |
|-----------|-------|
| Pin positions (Z from base) | 20.5 mm and 61.5 mm |
| Pin diameter | 2.0 mm |
| Pin length (protruding) | 3.0 mm |
| Pin radial position | r = 9.25 mm (center of wall) |

**USB-C port cutout**:

| Parameter | Value |
|-----------|-------|
| Width | 9.0 mm |
| Height | 3.3 mm |
| Z position (center) | 15.0 mm from shell base |
| Side | +X face (right side when viewed from front) |

**LED indicator window**:

| Parameter | Value |
|-----------|-------|
| Diameter | 2.0 mm (through-hole) |
| Z position (center) | 23.0 mm from shell base |
| Side | Same face as USB-C |

**Bayonet L-slots** (2x, 180 deg apart at base):

| Parameter | Value |
|-----------|-------|
| Entry slot width | 3.0 + 0.4 = 3.4 mm |
| Entry slot height | 2.0 + 0.2 = 2.2 mm |
| Radial position | at wall center (r = 9.25 mm) |
| Through wall | Yes |

**Battery floor** (internal partition):

| Parameter | Value |
|-----------|-------|
| Z position | 32.0 mm from shell base |
| Thickness | 1.5 mm |
| Spring contact pass-through hole | dia 5.0 mm, centered |

**Cartridge retention lip** (at shell top):

| Parameter | Value |
|-----------|-------|
| Lip height | 1.5 mm (inward ledge) |
| Inner opening | matches cartridge OD + 0.3 mm clearance |

**Finger notch** (at base, on split seam):

| Parameter | Value |
|-----------|-------|
| Shape | Semicircle, R = 5.0 mm |
| Position | Base face, +X edge (split seam) |

**Modeling steps**:
1. Create full cylindrical shell: 22.0 OD, 17.0 ID, 82.0 mm long
2. Add battery floor disc at Z=32 with spring contact hole
3. Cut USB-C port rectangle
4. Cut LED window circle
5. Cut 2 bayonet L-slots at base
6. Add cartridge retention lip at top
7. Cut finger notch at base
8. **Split** shell at Y=0 plane to get right half
9. Add 2 snap-fit cantilever clips along the seam edge
10. Add 2 alignment pins along the seam edge

---

### Part 4: Body Shell — Left Half

Mirror of right half except:
- **No alignment pins** — instead has **alignment holes**: dia 2.0 + 0.3 = 2.3 mm, depth 3.5 mm
- **No snap-fit clips** — instead has **matching recesses**: rectangular pockets where the catch engages
- Finger notch on matching side

---

### Part 5: Mouthpiece

**Function**: Tapered comfort tip with snap-fit attachment to body shell top.

```
         ┌──┐  ← 10.0 mm tip diameter
        ╱    ╲
       ╱      ╲   20.0 mm tall
      ╱   ○    ╲  ← air channel dia 4.0 mm (through)
     ╱          ╲
    ├────────────┤  ← 22.0 mm base diameter
    │ snap ring  │  3.0 mm tall, extends below base
    └────────────┘
```

| Feature | Dimension |
|---------|-----------|
| Base diameter | 22.0 mm |
| Tip diameter | 10.0 mm |
| Height (tapered section) | 20.0 mm |
| Air channel | dia 4.0 mm, through-hole |
| Snap ring OD | 22.0 - 0.6 = 21.4 mm (fits inside shell ID) |
| Snap ring ID | 17.0 + 0.3 = 17.3 mm |
| Snap ring height | 3.0 mm (extends below taper base) |
| Snap catch bump | +0.3 mm on snap ring OD, 1.5 mm tall band |
| Tip fillet | R = 1.5 mm |

**Modeling steps**:
1. Loft between base circle (r=11.0) and tip circle (r=5.0), height 20 mm
2. Cut air channel through-hole dia 4.0
3. Add snap ring below base: annular extrusion 3.0 mm down
4. Add catch bump ring on snap ring OD
5. Fillet tip edge R=1.5

---

### Part 6: Cartridge Sleeve (Atomizer Mock)

**Function**: Represents the atomizer/reservoir cartridge. Slides into body from top.

```
    ┌────────────┐  ← Closed top (cap 1.5 mm thick)
    │            │     Air hole dia 3.0 mm through
    │            │
    │  HOLLOW    │  35.0 mm tall
    │  INTERIOR  │
    │            │
    │ ═══O-ring══│  ← O-ring groove at 3.0 mm from base
    │            │
    ├──□────□────┤  ← Contact pad recesses (2x)
    └────────────┘
    ← 16.0 mm OD →
```

| Feature | Dimension |
|---------|-----------|
| Outer diameter | 16.0 mm |
| Wall thickness | 1.5 mm |
| Total height | 35.0 mm |
| Top cap thickness | 1.5 mm |
| Air channel | dia 3.0 mm, through-hole |
| O-ring groove position | 3.0 mm from base |
| O-ring groove width | 1.5 mm |
| O-ring groove depth | 0.8 mm (recess from OD) |
| Contact pads | 2x: 3.0 x 3.0 mm, 0.5 mm deep, spaced 5.0 mm apart |
| Top edge fillet | R = 0.5 mm |

**Modeling steps**:
1. Extrude annular cylinder 16.0 OD, 13.0 ID, 35.0 mm
2. Add solid cap at top (extrude disc at Z=33.5, 1.5 mm thick)
3. Cut air channel through-hole dia 3.0
4. Cut O-ring groove (annular recess on outer surface)
5. Cut 2 contact pad recesses on bottom face
6. Fillet top edge R=0.5

---

### Part 7: PCB Mount Bracket

**Function**: Flat bracket inside body for mounting PCB with press-fit standoffs.

```
    ┌───────────────────────────┐
    │  ○                     ○  │  ← Standoff posts (2x)
    │  (2.5mm dia, 3mm tall)    │     Spacing: 9.6 mm
    │                           │
    │       ┌─────────┐        │  ← JST-PH hole
    │       │  6x3.6  │        │     (6.0 x 3.6 mm rect)
    │       └─────────┘        │
    └───────────────────────────┘
    ← 16.0 mm wide →
           12.0 mm deep
           1.5 mm thick
```

| Feature | Dimension |
|---------|-----------|
| Width | 16.0 mm |
| Depth | 12.0 mm |
| Thickness | 1.5 mm |
| Standoff diameter | 2.5 mm |
| Standoff height | 3.0 mm |
| Standoff pilot hole | 1.9 mm (press-fit) |
| Standoff spacing | 9.6 mm center-to-center |
| JST-PH hole | 6.0 x 3.6 mm rectangle |
| Edge fillet | R = 0.5 mm |

---

## 3. Snap-Fit Design Parameters

Reference: [Formlabs Snap-Fit Enclosure Design Guide](https://formlabs.com/blog/designing-3d-printed-snap-fit-enclosures/)

### Cantilever Beam Snap-Fit

```
    Fixed end                    Free end
    ┌════════════════════════════┐
    │         beam               ├─┐ ← catch
    │    (10.0 x 1.5 x 0.8 mm)  ├─┘   (0.8 mm)
    └════════════════════════════┘
```

| Parameter | Value | Notes |
|-----------|-------|-------|
| Beam length | 10.0 mm | Longer = more flexible |
| Beam width | 1.5 mm | Along circumference |
| Beam thickness | 0.8 mm | Radial direction |
| Catch depth | 0.8 mm | How far it protrudes |
| Catch angle (entry) | 30 deg | Gentle ramp for insertion |
| Catch angle (retention) | 90 deg | Square face for holding |
| Max deflection | 0.5 mm | Should not exceed 2% of beam length |
| Material | PETG | Elongation at break ~23% |
| Print orientation | XY plane | Beam axis parallel to build plate |

### Engagement Force Estimate

For PETG (E ~ 2100 MPa, allowable strain ~ 2%):
- Deflection force ~ 1.5-3 N (comfortable finger push)
- Retention force > 5 N (won't pop open in pocket)

---

## 4. Bayonet Mount Design

```
BODY SHELL (base end, unrolled view):

    ─────┬─────────────┬─────────
         │  entry slot │
         │  ↓          │
    ═════╪═════════════╪═════════  ← locking channel
         │             │
    ─────┴─────────────┴─────────

    Entry slot: 3.4 mm wide x 2.2 mm tall (vertical)
    Locking channel: 3.4 mm wide x 2.2 mm tall (horizontal, 90 deg arc)

BASE CAP (matching lugs):

    Two rectangular lugs on inner skirt:
    - 3.0 mm wide x 2.0 mm tall
    - 180 deg apart
    - Insert vertically into entry slots, twist 90 deg to lock
```

---

## 5. Assembly Sequence

1. **Start with body shell right half** (flat, seam face up)
2. **Insert battery sled** into battery compartment zone
3. **Insert PCB bracket** onto internal standoff ribs above battery floor
4. **Connect JST-PH wire** from battery sled contacts to PCB bracket
5. **Close with body shell left half** — press until snap-fits click (4 clicks)
6. **Insert cartridge** from top (push until O-ring engages retention lip)
7. **Snap on mouthpiece** (push down until snap ring clicks)
8. **Insert battery** through open base (drop into sled, positive terminal up)
9. **Attach base cap** — align lugs with entry slots, push in, quarter-turn clockwise to lock

**Disassembly**: Reverse order. Battery removal: quarter-turn base cap, tilt device, battery slides out.

---

## 6. 3D Print Settings

| Parameter | Value |
|-----------|-------|
| Material | PETG (recommended) or PLA+ |
| Nozzle | 0.4 mm |
| Layer height | 0.2 mm |
| Infill | 20% gyroid |
| Walls/perimeters | 3 (= 1.2 mm, plus remaining wall is infill) |
| Top/bottom layers | 4 |
| Support | Minimal — only for bayonet L-slots if needed |
| Print orientation | All parts upright (Z = device axis) |
| Bed adhesion | Brim for body shell halves (tall, thin) |
| Post-processing | Light sanding at snap-fit seam for smooth closure |

### Print Orientation Notes

- **Body shell halves**: Print standing up (split seam on build plate). This orients snap-fit beams in XY for maximum strength.
- **Base cap**: Print upside down (flat bottom = build plate contact).
- **Mouthpiece**: Print tip-down for smooth outer surface.
- **Battery sled**: Print standing up.
- **Cartridge**: Print standing up.

---

## 7. Critical Tolerances Summary

| Mating Pair | Clearance | Notes |
|-------------|-----------|-------|
| Battery in sled cavity | 0.25 mm/side | Must slide freely |
| Shell halves at seam | 0.30 mm | Smooth closure |
| Snap-fit catch engagement | 0.80 mm depth | Audible click |
| Alignment pin in hole | 0.15 mm/side | Firm but insertable |
| Bayonet lug in slot | 0.20 mm | Smooth rotation |
| Mouthpiece snap ring in shell | 0.30 mm | Push-fit with detent |
| Cartridge in body | 0.30 mm | Snug via O-ring groove |

**Test fit**: Print the battery sled first as a quick test. If the battery is too tight or too loose, adjust `BATTERY_CLEARANCE` in `config.py` and reprint.
