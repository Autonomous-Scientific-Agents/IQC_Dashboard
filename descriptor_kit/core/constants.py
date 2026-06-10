"""Physical constants and tolerances. Single source of truth (spec §4).

Verbatim copy of ``src/constants.py``; this is the only place radii/tolerances
are defined for the kit.
"""
# Cordero (2008) covalent radii, Angstrom
COVALENT_RADII = {"H":0.31,"C":0.76,"N":0.71,"O":0.66,"F":0.57,"Cl":1.02,"Ni":1.24}
# Bondi vdW radii (for D50 vdW volume), Angstrom
VDW_RADII_BONDI = {"H":1.20,"C":1.70,"N":1.55,"O":1.52,"F":1.47,"Cl":1.75}
HEAVY_BOND_SCALE = 1.20          # heavy-heavy: dist < scale*(ri+rj)
MAX_DEGREE = {"C":4,"N":4,"O":2,"F":1,"Cl":1,"H":1}   # heavy-degree sanity (excl. H count? see geometry)
BURIED_VOLUME_RADIUS = 3.5
BURIED_VOLUME_RADII_TYPE = "bondi"
BURIED_VOLUME_RADII_SCALE = 1.17
BURIED_VOLUME_INCLUDE_HS = False
STERIMOL_RADII_TYPE = "bondi"
