// ============================================================================
// Air Bar NEX 3K — Faithful OpenSCAD Model
// Based on real measurements from makerspace disassembly session (3/2/26)
// ============================================================================

// === TOGGLES ================================================================
EXPLODED      = true;     // true = exploded view, false = assembled
CROSS_SECTION = false;    // true = cut away front half to see internals

$fn = 80;
GAP = EXPLODED ? 20 : 0;

// === SNAP-FIT TABS (Push Buttons) ===========================================
TAB_W = 10.0;        // mm width of the push button
TAB_H = 4.0;         // mm height of the push button
TAB_Z_OFFSET = 4.0;  // mm Z-offset from the bottom of the mouthpiece insert
TAB_CLEARANCE = 0.4; // mm gap between tab and shell cutout (printer tolerance)

// === FULL DEVICE (measured) =================================================
DEVICE_HEIGHT = 78.3;     // mm total assembled height (Z axis)
DEVICE_WIDTH  = 48.2;     // mm overall width (X axis)
DEVICE_DEPTH  = 19.0;     // mm overall thickness (Y axis)
CORNER_R      = DEVICE_DEPTH / 2;  // 9.5mm

// === ALUMINUM SHELL =========================================================
SHELL_WALL    = 0.7;      // mm measured wall thickness
SHELL_HEIGHT  = 52.35;    // mm exterior height 
SHELL_INNER_W = 47.6;     // mm inner cavity width
SHELL_INNER_D = 17.7;     // mm inner cavity depth
SHELL_INNER_H = 50.0;     // mm inner cavity height

// === MOUTHPIECE =============================================================
MP_TOTAL_LEN  = 35.95;    // mm total mouthpiece length
MP_INSERT_LEN = 10.0;     // mm portion press-fitting into shell
MP_VISIBLE    = 25.95;    // mm visible above shell
MP_THICKNESS  = 7.8;      // mm tip thickness/depth
MP_TIP_WIDTH  = 16.0;     // mm tip width
MP_AIR_HOLE   = 7.8;      // mm air hole diameter
MP_RIB_THICK  = 1.0;      // mm cross-rib thickness

// === BATTERY (13450 Li-ion) =================================================
BAT_DIA       = 12.4;     
BAT_LEN       = 42.4;     
BAT_NUB_DIA   = 4.0;      
BAT_NUB_LEN   = 1.0;      

// === PCB ====================================================================
PCB_W         = 18.6;     
PCB_D         = 11.6;     
PCB_T         = 0.84;     
USB_C_W       = 9.0;      
USB_C_H       = 3.3;      
MIC_DIA       = 5.0;      

// === INNER CHASSIS ==========================================================
CHASSIS_WALL  = 1.5;      
CHASSIS_H     = 10.0;     

// === RESERVOIR / ATOMIZER ===================================================
RES_W         = 31.65;    
RES_D         = 15.64;    
RES_H         = 46.76;    
RES_AIR_HOLE  = 3.5;      
RES_WALL      = 1.0;      

// === COLORS =================================================================
C_SHELL       = [0.25, 0.65, 0.30, 0.75];  
C_MOUTHPIECE  = [0.15, 0.15, 0.15, 1.00];  
C_BAT_RED     = [0.80, 0.20, 0.15, 1.00];  
C_BAT_YELLOW  = [0.90, 0.80, 0.10, 1.00];  
C_BAT_BLACK   = [0.10, 0.10, 0.10, 1.00];  
C_BAT_NUB     = [0.70, 0.70, 0.72, 1.00];  
C_PCB         = [0.90, 0.90, 0.85, 1.00];  
C_USB         = [0.55, 0.55, 0.55, 1.00];  
C_MIC         = [0.10, 0.10, 0.10, 1.00];  
C_LED         = [1.00, 1.00, 1.00, 1.00];  
C_CHASSIS     = [0.92, 0.92, 0.92, 1.00];  
C_RES_SHELL   = [0.85, 0.80, 0.65, 0.45];  
C_FOAM        = [0.90, 0.75, 0.20, 0.75];  
C_COIL        = [0.70, 0.70, 0.72, 1.00];  
C_WIRE_RED    = [0.80, 0.10, 0.10, 1.00];
C_WIRE_BLACK  = [0.10, 0.10, 0.10, 1.00];

// === DERIVED POSITIONS ======================================================
X_RES    = -(SHELL_INNER_W/2) + RES_W/2 + 0.5;    
X_BAT    =  (SHELL_INNER_W/2) - BAT_DIA/2 - 0.5;  
Z_FLOOR  = SHELL_WALL;                              
Z_ABOVE_CHASSIS = Z_FLOOR + CHASSIS_H;              

// ============================================================================
// UTILITY: Stadium / Rounded Rectangle
// ============================================================================
module stadium(w, d, h) {
    r = d / 2;
    offset_x = w/2 - r;
    hull() {
        translate([-offset_x, 0, 0]) cylinder(r=r, h=h);
        translate([ offset_x, 0, 0]) cylinder(r=r, h=h);
    }
}

// ============================================================================
// PART 1: ALUMINUM SHELL
// ============================================================================
module aluminum_shell() {
    color(C_SHELL)
    difference() {
        stadium(DEVICE_WIDTH, DEVICE_DEPTH, SHELL_HEIGHT);

        translate([0, 0, SHELL_WALL])
            stadium(SHELL_INNER_W, SHELL_INNER_D, SHELL_HEIGHT);

        translate([-(DEVICE_WIDTH/2) - 0.1, -USB_C_W/2, 1.5])
            cube([SHELL_WALL + 0.2, USB_C_W, USB_C_H]);

        for (y_off = [-USB_C_W/2 - 2.5, USB_C_W/2 + 1.0])
            translate([-(DEVICE_WIDTH/2) - 0.1, y_off, 2.0])
                cube([SHELL_WALL + 0.2, 1.5, 1.5]);

        // ---> ADDED: Push-button cutouts on the flat sides
        for (y_sign = [-1, 1]) {
            translate([0, y_sign * (DEVICE_DEPTH/2), SHELL_HEIGHT - MP_INSERT_LEN + TAB_Z_OFFSET])
                cube([TAB_W, SHELL_WALL * 3, TAB_H], center=true);
        }
    }
}

// ============================================================================
// PART 2: INNER CHASSIS
// ============================================================================
module inner_chassis() {
    color(C_CHASSIS)
    difference() {
        stadium(SHELL_INNER_W - 0.4, SHELL_INNER_D - 0.4, CHASSIS_H);

        translate([0, 0, CHASSIS_WALL])
            stadium(SHELL_INNER_W - 0.4 - 2*CHASSIS_WALL, SHELL_INNER_D - 0.4 - 2*CHASSIS_WALL, CHASSIS_H);

        translate([-PCB_W/2, -PCB_D/2, -0.1])
            cube([PCB_W, PCB_D, PCB_T + 0.5]);

        translate([-(SHELL_INNER_W/2), -USB_C_W/2, 0.5])
            cube([CHASSIS_WALL + 1, USB_C_W, USB_C_H + 1]);

        for (y_sign = [-1, 1])
            translate([-2, y_sign * (SHELL_INNER_D/2 - CHASSIS_WALL - 2), CHASSIS_WALL])
                cube([4, 1.5, CHASSIS_H]);
    }

    color(C_CHASSIS)
    for (x = [-(SHELL_INNER_W/4), SHELL_INNER_W/4])
        for (y_sign = [-1, 1])
            translate([x - 1.5, y_sign * (SHELL_INNER_D/2 - 0.2) - 0.3, CHASSIS_H * 0.4])
                cube([3, 0.6, 2]);
}

// ============================================================================
// PART 3: PCB BOARD
// ============================================================================
module pcb_board() {
    color(C_PCB)
    translate([-PCB_W/2, -PCB_D/2, 0])
        cube([PCB_W, PCB_D, PCB_T]);

    color(C_USB)
    translate([-PCB_W/2 - 1.5, -USB_C_W/2, PCB_T])
        cube([7.5, USB_C_W, USB_C_H]);

    color(C_MIC)
    translate([PCB_W/2 - MIC_DIA/2 - 1.5, 0, PCB_T])
        cylinder(d=MIC_DIA, h=1.5);

    color(C_LED)
    for (x = [-PCB_W/4 - 1, PCB_W/4 + 1])
        for (y = [-PCB_D/4, PCB_D/4])
            translate([x - 0.75, y - 0.5, PCB_T])
                cube([1.5, 1.0, 0.5]);

    color([0.20, 0.20, 0.20, 1])
    translate([-1.0, -PCB_D/4 + 1, PCB_T])
        cube([2.0, 1.0, 0.5]);
}

// ============================================================================
// PART 4: BATTERY CELL
// ============================================================================
module battery_cell() {
    band = BAT_LEN / 3;

    color(C_BAT_BLACK) cylinder(d=BAT_DIA, h=band);
    color(C_BAT_YELLOW) translate([0, 0, band]) cylinder(d=BAT_DIA, h=band);
    color(C_BAT_RED) translate([0, 0, 2*band]) cylinder(d=BAT_DIA, h=band);
    color(C_BAT_NUB) translate([0, 0, BAT_LEN]) cylinder(d=BAT_NUB_DIA, h=BAT_NUB_LEN);

    color([0.95, 0.95, 0.95, 1])
    translate([0, 0, BAT_LEN - 0.5])
        difference() {
            cylinder(d=BAT_DIA, h=0.5);
            cylinder(d=BAT_DIA - 2, h=0.6);
        }
}

// ============================================================================
// PART 5: RESERVOIR / ATOMIZER
// ============================================================================
module reservoir_atomizer() {
    res_inner_w = RES_W - 2*RES_WALL;
    res_inner_d = RES_D - 2*RES_WALL;

    color(C_RES_SHELL)
    difference() {
        stadium(RES_W, RES_D, RES_H);
        translate([0, 0, RES_WALL]) stadium(res_inner_w, res_inner_d, RES_H);
        translate([0, 0, -0.1]) cylinder(d=RES_AIR_HOLE, h=RES_H + 0.2);
    }

    color(C_FOAM)
    difference() {
        translate([0, 0, RES_WALL + 1]) stadium(res_inner_w - 1, res_inner_d - 1, RES_H - 2*RES_WALL - 2);
        translate([0, 0, -0.1]) cylinder(d=RES_AIR_HOLE + 2, h=RES_H + 0.2);
    }

    color(C_COIL)
    translate([0, 0, 1])
        difference() {
            cylinder(d=8, h=4);
            cylinder(d=RES_AIR_HOLE, h=4.1);
        }

    color(C_RES_SHELL)
    translate([0, 0, RES_H - RES_WALL]) stadium(RES_W, RES_D, RES_WALL);
}

// ============================================================================
// PART 6: MOUTHPIECE (With flexible snap-fit tabs)
// ============================================================================
module mouthpiece() {
    color(C_MOUTHPIECE)
    difference() {
        union() {
            // Main Insert Base
            translate([0, 0, -MP_INSERT_LEN])
                stadium(SHELL_INNER_W - 0.6, SHELL_INNER_D - 0.6, MP_INSERT_LEN);

            // ---> ADDED: Snap-fit push buttons (protruding outwards)
            for (y_sign = [-1, 1]) {
                translate([0, y_sign * ((SHELL_INNER_D - 0.6)/2 + SHELL_WALL/2), -MP_INSERT_LEN + TAB_Z_OFFSET])
                    cube([TAB_W - TAB_CLEARANCE, SHELL_WALL + 1, TAB_H - TAB_CLEARANCE], center=true);
            }

            // Visible Tapered Body
            hull() {
                stadium(DEVICE_WIDTH, DEVICE_DEPTH, 0.01);
                translate([0, 0, MP_VISIBLE]) stadium(MP_TIP_WIDTH, MP_THICKNESS, 0.01);
            }
        }

        // Central Air Hole
        translate([0, 0, -MP_INSERT_LEN - 0.1])
            cylinder(d=MP_AIR_HOLE, h=MP_TOTAL_LEN + 0.2);

        // ---> ADDED: Cutouts to create the flexible "living hinge" for the buttons
        for (y_sign = [-1, 1]) {
            // Vertical side slits
            for (x_sign = [-1, 1]) {
                translate([x_sign * (TAB_W/2 + 0.5), y_sign * (DEVICE_DEPTH/2), -MP_INSERT_LEN + TAB_Z_OFFSET + 1])
                    cube([1.0, 4.0, TAB_H + 4], center=true);
            }
            // Bottom horizontal slit to free the button from the bottom edge
            translate([0, y_sign * (DEVICE_DEPTH/2), -MP_INSERT_LEN + TAB_Z_OFFSET - TAB_H/2 - 0.5])
                cube([TAB_W + 2, 4.0, 1.0], center=true);
            
            // Hollowed relief cavity behind the button so it can flex inward
            translate([0, y_sign * (SHELL_INNER_D/2 - 1.5), -MP_INSERT_LEN + TAB_Z_OFFSET + 1])
                cube([TAB_W + 2, 2.0, TAB_H + 4], center=true);
        }
    }

    // Cross-ribs inside the air channel
    color(C_MOUTHPIECE)
    translate([0, 0, -MP_INSERT_LEN]) {
        translate([-MP_AIR_HOLE/2, -MP_RIB_THICK/2, 0]) cube([MP_AIR_HOLE, MP_RIB_THICK, MP_INSERT_LEN]);
        translate([-MP_RIB_THICK/2, -MP_AIR_HOLE/2, 0]) cube([MP_RIB_THICK, MP_AIR_HOLE, MP_INSERT_LEN]);
    }
}

// ============================================================================
// PART 7: WIRES
// ============================================================================
module wires(bat_x, wire_len) {
    color(C_WIRE_RED) translate([bat_x + BAT_DIA/2 + 1.0, -1, 0]) cylinder(d=0.8, h=wire_len);
    color(C_WIRE_BLACK) translate([bat_x + BAT_DIA/2 + 2.5, 1, 0]) cylinder(d=0.8, h=wire_len);
}

// ============================================================================
// ASSEMBLY
// ============================================================================
module full_assembly() {
    z_shell      = 0;
    z_chassis    = Z_FLOOR;                      
    z_pcb        = Z_FLOOR + 1.0;                
    z_internals  = Z_ABOVE_CHASSIS;              
    z_mouthpiece = SHELL_HEIGHT;                 

    ez_shell     = 0;
    ez_chassis   = EXPLODED ? -(CHASSIS_H + GAP) : z_chassis;
    ez_pcb       = EXPLODED ? -(CHASSIS_H + GAP) + 1.0 : z_pcb;
    ez_battery   = EXPLODED ? SHELL_HEIGHT + GAP : z_internals;
    ez_reservoir = EXPLODED ? SHELL_HEIGHT + GAP*2 + BAT_LEN + BAT_NUB_LEN : z_internals;
    ez_mouthpiece= EXPLODED ? SHELL_HEIGHT + GAP*3 + BAT_LEN + BAT_NUB_LEN + RES_H : z_mouthpiece;

    ex_battery   = EXPLODED ? 20 : X_BAT;
    ex_reservoir = EXPLODED ? -20 : X_RES;

    translate([0, 0, ez_shell]) aluminum_shell();
    translate([0, 0, ez_chassis]) inner_chassis();
    translate([0, 0, ez_pcb]) pcb_board();
    translate([ex_battery, 0, ez_battery]) battery_cell();
    translate([ex_reservoir, 0, ez_reservoir]) reservoir_atomizer();
    translate([0, 0, ez_mouthpiece]) mouthpiece();

    if (!EXPLODED) {
        translate([0, 0, Z_FLOOR]) wires(X_BAT, Z_ABOVE_CHASSIS + BAT_LEN);
    }
}

// ============================================================================
// RENDER
// ============================================================================
if (CROSS_SECTION) {
    difference() {
        full_assembly();
        translate([-DEVICE_WIDTH, 0, -50])
            cube([DEVICE_WIDTH * 2, DEVICE_DEPTH, DEVICE_HEIGHT + 200]);
    }
} else {
    full_assembly();
}

if (EXPLODED) {
    label_x = DEVICE_WIDTH/2 + 8;
    color("black") {
        translate([label_x, 0, SHELL_HEIGHT/2]) text("Aluminum Shell", size=3, halign="left");
        translate([label_x, 0, -(CHASSIS_H + GAP) + CHASSIS_H/2]) text("Inner Chassis + PCB", size=3, halign="left");
        translate([30, 0, SHELL_HEIGHT + GAP + BAT_LEN/2]) text("Battery (13450)", size=3, halign="left");
        translate([-55, 0, SHELL_HEIGHT + GAP*2 + BAT_LEN + BAT_NUB_LEN + RES_H/2]) text("Reservoir + Atomizer", size=3, halign="left");
        translate([label_x, 0, SHELL_HEIGHT + GAP*3 + BAT_LEN + BAT_NUB_LEN + RES_H + MP_VISIBLE/2]) text("Mouthpiece", size=3, halign="left");
    }
}