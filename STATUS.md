# E-Cigarette DfD Project Status

**Project**: Design for Disassembly of Disposable Electronic Cigarettes
**Course**: MECE E4612 - Sustainable Manufacturing, Columbia University
**Date**: March 10, 2026

---

## CAD / Design Work

### DONE

| Part | File | Description |
|------|------|-------------|
| Air Bar NEX 3K (reference) | `cad/assembly_preview.scad` | Full OpenSCAD model of the existing disposable e-cig based on real measurements from 3/2/26 makerspace session. Exploded + cross-section views, all 7 internal components (shell, chassis, PCB, battery, reservoir, mouthpiece, wires). Color-coded. |
| Battery Sled | `cad/battery_sled.py` | CadQuery parametric model: cylindrical carrier, spring contact pocket, polarity key notch |
| Body Shell (L+R) | `cad/body_shell.py` | CadQuery clamshell halves: snap-fit clips, alignment pins, USB-C cutout, LED window, bayonet L-slots, battery floor, finger notch |
| Mouthpiece | `cad/mouthpiece.py` | CadQuery tapered cone, air channel, snap-fit ring |
| Cartridge Sleeve | `cad/cartridge.py` | CadQuery atomizer mock: O-ring groove, contact pads, air hole |
| PCB Bracket | `cad/pcb_bracket.py` | CadQuery flat mount: standoffs, JST-PH hole |
| Assembly | `cad/assembly.py` | Full assembly + exploded view generator |
| Config | `cad/config.py` | Shared dimensions, tolerances, derived values from battery measurements |
| Design Spec | `cad/DESIGN_SPEC.md` | Complete 476-line engineering spec with all 7 parts dimensioned, tolerances, snap-fit parameters, print settings |

### NOT YET DONE - CAD

| Task | Priority | Notes |
|------|----------|-------|
| **Quick-disconnect battery mechanism** | HIGH | The twist-lock bayonet base cap exists in DESIGN_SPEC.md (Part 1) and is coded in `battery_sled.py` but needs refinement. Key design prompts below. |
| **Base cap (twist-lock door)** | HIGH | Needs its own dedicated `.py` or `.scad` file. Currently only specified in DESIGN_SPEC.md but not generated as a standalone part file. |
| **Generate STL/STEP exports** | MEDIUM | Python scripts exist but need to be run to produce actual .stl/.step files for printing |
| **OpenSCAD version of DfD redesign** | LOW | The DfD redesign is in CadQuery/Python only. Could mirror to OpenSCAD if needed for portability. |

### Design Prompts for Quick-Disconnect Battery

The quick-disconnect battery mechanism is the centerpiece of the alternative concept. Key design decisions still needed:

1. **Bayonet lug geometry**: The spec calls for 2 lugs 180deg apart, 3mm wide x 2mm tall. Should these have a detent ramp (click-lock) to prevent accidental rotation?
2. **Spring contact design**: The battery sled has a spring contact pocket (dia 5mm, depth 3mm) at the positive terminal. How is the spring retained? Press-fit brass contact? Conductive foam?
3. **Negative terminal contact**: Base cap has a contact pad recess (dia 6mm, depth 0.8mm). What contact material? Flat nickel strip? Spring?
4. **Ejection mechanism**: Current design relies on gravity (tilt and slide out). Should there be a spring-loaded ejector for horizontal use?
5. **Sealing**: How is the battery compartment sealed against e-liquid ingress? O-ring on base cap? Silicone gasket?
6. **Universal sizing**: The spec defines 3 size classes (S/M/L). The current CAD is sized for the M-class (12mm dia x 40mm battery). Should the sled be parametric to handle all 3 sizes?

---

## Report (LaTeX)

### DONE

| Section | File | Status |
|---------|------|--------|
| 1. Introduction | `sections/01_introduction.tex` | Mostly complete: product description, functionality, scope, e-waste crisis motivation. Some \todo{} markers for photos. |
| 2. Materials & Processes | `sections/02_materials_processes.tex` | **Weights filled in from makerspace data.** Parts table complete (52g total). Material IDs documented (aluminum housing confirmed, battery specs: 13450 3.7V 650mAh). Disassembly observations filled in (press-fit, X-acto knife, 4-5 min, ~10 steps, destructive). Manufacturing processes specified for housing (impact extrusion + anodizing + pad printing). |
| 3. DfD Analysis | `sections/03_dfd_analysis.tex` | 7 DfD principles applied, snap-fit design, bayonet mount, disassembly comparison table. |
| 5. Alternative Concept | `sections/05_alternative_concept.tex` | Universal Removable Battery Standard spec with 3 sizes, mechanical/electrical interface, impact reduction mechanisms. Has \todo{} for exact dimensions and LCA of alternative. |
| 6. Results | `sections/06_results.tex` | Table structures built. **Disassembly performance table filled in** (reference: ~10 steps, 4-5 min, X-acto knife, destructive). LCA comparison numbers still \todo{X} placeholders. |
| 7. Conclusions | `sections/07_conclusions.tex` | Framework in place. |
| Preamble | `preamble.tex` | Complete. |
| Bibliography | `references.bib` | Key references included. |
| Compiled PDF | `main.pdf` | Compiled output exists. |

### NOT YET DONE - Report

| Task | Priority | For Midterm? | Notes |
|------|----------|--------------|-------|
| ~~Fill in measured weights in Sec 2 parts table~~ | DONE | YES | Battery 12g, housing 13g, PCB 2g, reservoir+atomizer 10g, total 52g |
| ~~Complete material identification methods in Sec 2~~ | DONE | YES | Aluminum confirmed (non-magnetic, 0.7mm wall), battery labeled 13450 3.7V 650mAh |
| **Lifecycle identification for each part** | HIGH | YES (midterm req) | For each of the 7 parts: what is its expected lifecycle? Single-use? Multi-cycle? What limits its life? See table below. |
| **Sourcing identification for each part** | HIGH | YES (midterm req) | For each of the 7 parts: where is it sourced? Raw material origin, manufacturing location, supply chain. See table below. |
| **LCA Section 4** - run actual LCA | HIGH | NO (final) | Entire section is \todo{} placeholders. Need to choose software (SimaPro/OpenLCA), database (Ecoinvent/USLCI), run analysis. |
| **LCA of alternative concept** in Sec 5 | HIGH | NO (final) | Battery impact allocation across N cycles, housing material change, recycling credits |
| **Results section numeric values** | HIGH | NO (final) | All LCA comparison numbers, cost analysis |
| **Insert disassembly photos** | MEDIUM | YES | 10 HEIC photos from makerspace session available in `3_2_26_makerspace_session_results/Air_bar photos/` |
| **Insert CAD renders** | MEDIUM | NO (final) | Exploded view diagrams, dimensional drawings |
| **Battery standard dimensional drawing** | MEDIUM | NO (final) | Exact dims for S/M/L battery classes (currently \todo{} in table) |
| **Discussion section** | LOW | NO (final) | Interpretation of results, barriers to adoption |

---

## Midterm-Specific Requirements

The midterm has different goals from the final. Key midterm deliverables:

### 1. Lifecycle Identification (per part)

| Part | Lifecycle in Current Design | Lifecycle in DfD Redesign | Limiting Factor |
|------|---------------------------|--------------------------|-----------------|
| Battery cell | Single-use (1 cycle of 450+ possible) | 10-450+ reuse cycles | Calendar aging, cycle degradation |
| Outer housing | Single-use, landfilled | Reusable body, recyclable at EOL | Mechanical wear, cosmetic damage |
| Atomizer coil + wick | Single-use (coil degrades) | Single-use (consumable cartridge) | Coil oxidation, wick carbonization |
| PCB assembly | Single-use, e-waste | Reusable across device lifetimes | Component failure (rare) |
| Mouthpiece | Single-use | Reusable (snap-fit, washable) | Hygiene, material fatigue |
| E-liquid reservoir | Single-use (depleted) | Single-use (cartridge is consumable) | E-liquid depletion |
| Seals & insulators | Single-use | Replace with each cartridge swap | Compression set, chemical degradation |

### 2. Sourcing Identification (per part)

| Part | Raw Material Origin | Manufacturing Location | Supply Chain Notes |
|------|-------------------|----------------------|-------------------|
| Battery cell (Li-ion) | Lithium: Australia/Chile/Argentina. Cobalt: DRC. Nickel: Indonesia/Philippines. Graphite: China. | Cell assembly: Shenzhen, China (Dongguan) | Conflict mineral concerns (cobalt). IEC 62133 certified. |
| Outer housing (Al) | Bauxite: Australia/Guinea/Brazil. Alumina refining: China. | Extrusion + anodizing: Shenzhen, China | High embodied energy (Hall-Heroult process) |
| Atomizer coil | Kanthal: Sweden (Sandvik). Nichrome: various. Cotton wick: India/Egypt/USA. | Coil winding: Shenzhen, China | Wire drawn to precise gauge (28-32 AWG) |
| PCB assembly | Copper: Chile/Peru. FR4: China. Components: global (TI, ST, etc.) | SMT assembly: Shenzhen, China | Lead-free solder (RoHS). BOM cost ~$0.30-0.50 |
| Mouthpiece (PP/PC) | Petroleum-derived polymer. PP: Middle East/USA refineries. | Injection molding: co-located with assembly | Single-cavity mold, cycle time ~15-30s |
| E-liquid | PG/VG: petroleum-derived (USA/China). Nicotine: tobacco extract (India/China). Flavoring: food-grade (USA/EU). | Blending + filling: China or USA | FDA/TPD regulated in destination markets |
| Seals (silicone) | Silicone: from silica sand (global). Platinum-cured. | Compression molding: China | Medical-grade silicone available |

### 3. Other Midterm Tasks

- [ ] Present makerspace measurement data clearly
- [ ] Document disassembly process with photos
- [ ] Identify at least 2 metallic and 2 non-metallic materials (DONE in report structure)
- [ ] Identify at least 3 parts with multiple manufacturing processes (DONE in report structure)

---

## Presentation

| File | Status |
|------|--------|
| `slides/outline.md` | Complete 12-slide outline with speaker notes, timing, visual suggestions, speaker assignments |

---

## Makerspace Data

| File | Status |
|------|--------|
| `3_2_26_makerspace_session_results/Air_bar_msrmnts_1.rtf` | Raw measurement notes from Air Bar NEX 3K disassembly |
| `3_2_26_makerspace_session_results/Air_bar photos/` | 10 HEIC photos of disassembly |

---

## Summary: What's Done vs. What's Left

### DONE
- Reference product OpenSCAD model (faithful to real measurements)
- DfD redesign CAD (7 parts fully specified + coded in CadQuery)
- Report structure with all 7 sections
- DfD principles analysis
- Alternative concept framework (Universal Removable Battery Standard)
- Presentation outline
- Makerspace disassembly + measurements

### LEFT TO DO (MIDTERM)
- Fill in measured weights from makerspace data
- Complete material ID methods documentation
- Lifecycle identification for each part (table drafted above)
- Sourcing identification for each part (table drafted above)
- Insert disassembly photos into report
- Polish Section 2 (Materials & Processes) with real data

### LEFT TO DO (FINAL)
- Run LCA (SimaPro or OpenLCA) for reference product
- Run LCA for DfD concept
- Run LCA for alternative concept (with battery reuse allocation)
- Fill in all numeric results in Section 6
- Generate CAD renders/exports for report figures
- Refine quick-disconnect battery design (see prompts above)
- Create dedicated base cap part file
- Complete Discussion section
- Finalize battery standard dimensional drawings (S/M/L exact dims)
- Cost analysis
