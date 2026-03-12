"""
Shared configuration for all CadQuery part scripts.

INSTRUCTIONS:
1. Measure your recovered vape battery with calipers
2. Update BATTERY_DIAMETER and BATTERY_LENGTH below
3. All other dimensions derive from these + the constants below
4. Run any part script to regenerate STL/STEP files

All dimensions in millimeters.
"""

# =============================================================================
# BATTERY DIMENSIONS — MEASURE YOUR RECOVERED CELL AND UPDATE THESE
# =============================================================================
BATTERY_DIAMETER = 12.0      # mm — measure with calipers
BATTERY_LENGTH = 40.0        # mm — measure with calipers

# =============================================================================
# CLEARANCES & TOLERANCES (tuned for FDM / PETG at 0.2mm layer height)
# =============================================================================
BATTERY_CLEARANCE = 0.25     # mm per side — radial clearance around battery
BATTERY_LENGTH_CLEARANCE = 2.0  # mm — extra depth for spring compression
SNAP_FIT_CLEARANCE = 0.3    # mm — gap between mating shell halves
PIN_HOLE_CLEARANCE = 0.15   # mm — press-fit alignment pin tolerance
BAYONET_CLEARANCE = 0.2     # mm — twist-lock slot clearance

# =============================================================================
# WALL & STRUCTURAL DIMENSIONS
# =============================================================================
WALL_THICKNESS = 2.5         # mm — outer shell wall
SNAP_ARM_WIDTH = 1.5         # mm — cantilever snap-fit beam width
SNAP_ARM_LENGTH = 10.0       # mm — cantilever snap-fit beam length
SNAP_DEFLECTION = 0.5        # mm — snap catch deflection
SNAP_CATCH_DEPTH = 0.8      # mm — snap catch engagement depth
FILLET_RADIUS = 0.5          # mm — minimum internal fillet

# =============================================================================
# OVERALL DEVICE DIMENSIONS
# =============================================================================
OUTER_DIAMETER = 22.0        # mm — external diameter of assembled device
TOTAL_LENGTH = 110.0         # mm — mouthpiece tip to base cap bottom

# Module lengths (these sum to TOTAL_LENGTH)
MOUTHPIECE_LENGTH = 20.0     # mm
BODY_LENGTH = 50.0           # mm — electronics + cartridge zone
BASE_CAP_LENGTH = 8.0        # mm — twist-lock base cap

# =============================================================================
# DERIVED DIMENSIONS — do not edit directly
# =============================================================================
INNER_DIAMETER = OUTER_DIAMETER - 2 * WALL_THICKNESS
BATTERY_CAVITY_DIAMETER = BATTERY_DIAMETER + 2 * BATTERY_CLEARANCE
BATTERY_CAVITY_LENGTH = BATTERY_LENGTH + BATTERY_LENGTH_CLEARANCE
BATTERY_COMPARTMENT_LENGTH = TOTAL_LENGTH - MOUTHPIECE_LENGTH - BODY_LENGTH - BASE_CAP_LENGTH

# =============================================================================
# CONNECTOR & PORT DIMENSIONS
# =============================================================================
USB_C_WIDTH = 9.0            # mm — USB-C port cutout width
USB_C_HEIGHT = 3.3           # mm — USB-C port cutout height
USB_C_OFFSET_FROM_BASE = 15.0  # mm — center of USB-C from base of body
LED_DIAMETER = 2.0           # mm — LED indicator window

# =============================================================================
# CARTRIDGE DIMENSIONS
# =============================================================================
CARTRIDGE_OD = 16.0          # mm — cartridge outer diameter
CARTRIDGE_LENGTH = 35.0      # mm — cartridge total length
CARTRIDGE_WALL = 1.5         # mm — cartridge wall thickness

# =============================================================================
# BAYONET MOUNT
# =============================================================================
BAYONET_LUG_WIDTH = 3.0     # mm — width of each lug
BAYONET_LUG_HEIGHT = 2.0    # mm — height/depth of lug engagement
BAYONET_ROTATION = 90.0     # degrees — quarter-turn to lock
NUM_BAYONET_LUGS = 2        # symmetrically placed

# =============================================================================
# ALIGNMENT FEATURES
# =============================================================================
ALIGNMENT_PIN_DIAMETER = 2.0  # mm
ALIGNMENT_PIN_LENGTH = 3.0   # mm
NUM_ALIGNMENT_PINS = 2

# =============================================================================
# SPRING CONTACT (Keystone 5230 or equivalent)
# =============================================================================
SPRING_CONTACT_DIAMETER = 5.0  # mm — pocket diameter for spring contact
SPRING_CONTACT_DEPTH = 3.0    # mm — pocket depth

# =============================================================================
# MOUTHPIECE
# =============================================================================
MOUTHPIECE_TIP_DIAMETER = 10.0  # mm — tapered tip
AIR_CHANNEL_DIAMETER = 4.0      # mm — internal airflow bore

# =============================================================================
# PCB MOUNT
# =============================================================================
PCB_STANDOFF_DIAMETER = 2.5  # mm
PCB_STANDOFF_HEIGHT = 3.0    # mm
JST_MOUNT_HOLE_DIAMETER = 6.0  # mm — hole for JST-PH connector body
