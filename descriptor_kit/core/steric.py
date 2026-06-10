"""Steric subsystem (spec §7): morfeus Sterimol / BuriedVolume + Bondi vdW volume.

Faithful copy of ``src/steric.py`` with package-relative imports.

All three functions operate on a fragment defined by atom indices into a `Geom`.
They build a *local* element/coordinate array containing only the atoms morfeus
needs, remap the global atom indices to local 1-based indices (morfeus uses
1-based atom indexing — verified against morfeus 0.8.0), and call the morfeus
estimators with the conventions fixed in `constants.py`.
"""
from __future__ import annotations
import numpy as np
from morfeus import Sterimol, BuriedVolume

from .constants import (
    STERIMOL_RADII_TYPE,
    BURIED_VOLUME_RADIUS,
    BURIED_VOLUME_RADII_TYPE,
    BURIED_VOLUME_RADII_SCALE,
    BURIED_VOLUME_INCLUDE_HS,
    VDW_RADII_BONDI,
)


def _local_arrays(geom, idxs):
    """Return (elements list, coords ndarray, remap dict) for the global atom
    indices `idxs`, in sorted order.  `remap[global] = local 0-based index`."""
    idxs = sorted(idxs)
    remap = {a: i for i, a in enumerate(idxs)}
    els = [geom.elements[a] for a in idxs]
    xyz = np.asarray(geom.coords)[idxs]
    return els, xyz, remap


def sterimol(geom, dummy_idx, attached_idx, frag_atoms):
    """Sterimol L / B1 / B5 of a substituent (spec §7, D11-D13/D48/D49).

    `dummy_idx`     - the attachment atom (alkyne C or bpy ring C); the Sterimol
                      vector origin.
    `attached_idx`  - the substituent's first atom (its root).
    `frag_atoms`    - the substituent atoms (root + everything grown from it).

    The morfeus calculation is run on the isolated fragment
    {dummy_idx, attached_idx} ∪ frag_atoms.  Returns
    {"L":float, "B1":float, "B5":float}; all strictly positive.
    """
    assert dummy_idx != attached_idx, "dummy and attached atom must differ"
    assert attached_idx in frag_atoms, (
        "attached (root) atom must be part of the fragment")
    assert dummy_idx not in frag_atoms, (
        "dummy (attachment) atom must NOT be part of the fragment")

    idxs = set(frag_atoms) | {dummy_idx, attached_idx}
    els, xyz, remap = _local_arrays(geom, idxs)
    assert "Ni" not in els, "Sterimol fragment must not contain Ni"

    s = Sterimol(
        els, xyz,
        remap[dummy_idx] + 1,       # morfeus is 1-based
        remap[attached_idx] + 1,
        radii_type=STERIMOL_RADII_TYPE,
    )
    L = float(s.L_value)
    B1 = float(s.B_1_value)
    B5 = float(s.B_5_value)
    assert np.isfinite([L, B1, B5]).all(), "Sterimol returned non-finite value"
    assert L > 0 and B1 > 0 and B5 > 0, "Sterimol dimensions must be positive"
    return {"L": L, "B1": B1, "B5": B5}


def percent_buried_volume(geom, metal_idx, include_atoms):
    """Fragment-only %V_bur around `metal_idx` (spec §7; D9/D10/D47/D51/D65).

    Only `metal_idx` + `include_atoms` are passed to morfeus, so the reported
    buried volume reflects that fragment alone.  Bondi radii ×1.17, sphere
    radius 3.5 Å, H excluded (per constants).  Returns a percentage in (0, 100).
    """
    assert metal_idx not in include_atoms, (
        "metal atom must not be listed in include_atoms")
    assert len(include_atoms) >= 1, "need at least one fragment atom"

    idxs = set(include_atoms) | {metal_idx}
    els, xyz, remap = _local_arrays(geom, idxs)
    assert els[remap[metal_idx]] == geom.elements[metal_idx]

    bv = BuriedVolume(
        els, xyz,
        remap[metal_idx] + 1,       # morfeus is 1-based
        radius=BURIED_VOLUME_RADIUS,
        radii_type=BURIED_VOLUME_RADII_TYPE,
        radii_scale=BURIED_VOLUME_RADII_SCALE,
        include_hs=BURIED_VOLUME_INCLUDE_HS,
    )
    # `fraction_buried_volume` ∈ [0,1]; ×100 -> percent.
    pct = float(bv.fraction_buried_volume) * 100.0
    assert np.isfinite(pct), "BuriedVolume returned non-finite value"
    return pct


def vdw_volume(geom, frag_atoms):
    """Sum of Bondi atomic vdW volumes (4/3·π·r³) over `frag_atoms` (spec §7,
    D50).  Ni is skipped (it has no Bondi radius here and is never part of an
    organic fragment).  Returns volume in Å³.
    """
    assert len(frag_atoms) >= 1, "need at least one atom for a vdW volume"
    total = 0.0
    for a in frag_atoms:
        el = geom.elements[a]
        if el == "Ni":
            continue
        r = VDW_RADII_BONDI[el]
        total += 4.0 / 3.0 * np.pi * r ** 3
    assert total > 0, "vdW volume must be positive"
    return float(total)
