"""Pair-level tdelta_* descriptors — one public function per output key.

These are the regioisomer Δ descriptors (spec §3.1, §8.10): each
``tdelta_<core>`` = ``prod_<core>(Type_I) − prod_<core>(Type_II)``.  They are the
ONE family that needs two molecules, so they live in their own API: each function
takes the two single-row results (``compute_descriptors`` output dicts) for the
Type_I and Type_II regioisomers and reads the relevant ``prod_*`` key from each.

NaN if either side is missing the key or either present value is NaN.
"""
from __future__ import annotations
import math


def _isnan(x) -> bool:
    try:
        return x is None or (isinstance(x, float) and math.isnan(x))
    except TypeError:
        return False


def _delta(result_I, result_II, source_col):
    """Type_I value − Type_II value for ``source_col``; NaN if missing/NaN on
    either side.  (NOT a descriptor — shared by every tdelta function.)"""
    a = result_I.get(source_col)
    b = result_II.get(source_col)
    if a is None or b is None or _isnan(a) or _isnan(b):
        return float("nan")
    return float(a) - float(b)


def tdelta_ni_Cb(result_I, result_II):
    """D61: prod_ni_Cb(Type_I) − prod_ni_Cb(Type_II)."""
    return {"tdelta_ni_Cb": _delta(result_I, result_II, "prod_ni_Cb")}


def tdelta_ni_o1(result_I, result_II):
    """D62: prod_ni_o1(Type_I) − prod_ni_o1(Type_II)."""
    return {"tdelta_ni_o1": _delta(result_I, result_II, "prod_ni_o1")}


def tdelta_newcc_Ca(result_I, result_II):
    """D63: prod_newcc_Ca(Type_I) − prod_newcc_Ca(Type_II)."""
    return {"tdelta_newcc_Ca": _delta(result_I, result_II, "prod_newcc_Ca")}


def tdelta_o_ni_bite_Cb(result_I, result_II):
    """D64: prod_o_ni_bite_Cb(Type_I) − prod_o_ni_bite_Cb(Type_II)."""
    return {"tdelta_o_ni_bite_Cb": _delta(result_I, result_II, "prod_o_ni_bite_Cb")}


def tdelta_metallacycle_vbur(result_I, result_II):
    """D65: prod_metallacycle_vbur(Type_I) − prod_metallacycle_vbur(Type_II)."""
    return {"tdelta_metallacycle_vbur": _delta(result_I, result_II, "prod_metallacycle_vbur")}


def tdelta_ni_n_mean(result_I, result_II):
    """prod_ni_n_mean(Type_I) − prod_ni_n_mean(Type_II)."""
    return {"tdelta_ni_n_mean": _delta(result_I, result_II, "prod_ni_n_mean")}


def tdelta_abs_dni_n(result_I, result_II):
    """prod_abs_dni_n(Type_I) − prod_abs_dni_n(Type_II)."""
    return {"tdelta_abs_dni_n": _delta(result_I, result_II, "prod_abs_dni_n")}


def tdelta_ni_bpyplane_dist(result_I, result_II):
    """prod_ni_bpyplane_dist(Type_I) − prod_ni_bpyplane_dist(Type_II)."""
    return {"tdelta_ni_bpyplane_dist": _delta(result_I, result_II, "prod_ni_bpyplane_dist")}


def tdelta_coordplane_rms(result_I, result_II):
    """prod_coordplane_rms(Type_I) − prod_coordplane_rms(Type_II)."""
    return {"tdelta_coordplane_rms": _delta(result_I, result_II, "prod_coordplane_rms")}


def tdelta_tau4(result_I, result_II):
    """prod_tau4(Type_I) − prod_tau4(Type_II)."""
    return {"tdelta_tau4": _delta(result_I, result_II, "prod_tau4")}


def tdelta_metallacycle_perimeter(result_I, result_II):
    """prod_metallacycle_perimeter(Type_I) − prod_metallacycle_perimeter(Type_II)."""
    return {"tdelta_metallacycle_perimeter": _delta(result_I, result_II, "prod_metallacycle_perimeter")}


def tdelta_cremer_pople_Q(result_I, result_II):
    """prod_cremer_pople_Q(Type_I) − prod_cremer_pople_Q(Type_II)."""
    return {"tdelta_cremer_pople_Q": _delta(result_I, result_II, "prod_cremer_pople_Q")}


def tdelta_dih_ni_o_c_Ca(result_I, result_II):
    """prod_dih_ni_o_c_Ca(Type_I) − prod_dih_ni_o_c_Ca(Type_II)."""
    return {"tdelta_dih_ni_o_c_Ca": _delta(result_I, result_II, "prod_dih_ni_o_c_Ca")}


def tdelta_dih_o_c_ca_cb(result_I, result_II):
    """prod_dih_o_c_ca_cb(Type_I) − prod_dih_o_c_ca_cb(Type_II)."""
    return {"tdelta_dih_o_c_ca_cb": _delta(result_I, result_II, "prod_dih_o_c_ca_cb")}


def tdelta_cc_metallacycle_len(result_I, result_II):
    """prod_cc_metallacycle_len(Type_I) − prod_cc_metallacycle_len(Type_II)."""
    return {"tdelta_cc_metallacycle_len": _delta(result_I, result_II, "prod_cc_metallacycle_len")}


def tdelta_cc_alternation(result_I, result_II):
    """prod_cc_alternation(Type_I) − prod_cc_alternation(Type_II)."""
    return {"tdelta_cc_alternation": _delta(result_I, result_II, "prod_cc_alternation")}


def tdelta_o_c_o_angle(result_I, result_II):
    """prod_o_c_o_angle(Type_I) − prod_o_c_o_angle(Type_II)."""
    return {"tdelta_o_c_o_angle": _delta(result_I, result_II, "prod_o_c_o_angle")}


def tdelta_co_asym(result_I, result_II):
    """prod_co_asym(Type_I) − prod_co_asym(Type_II)."""
    return {"tdelta_co_asym": _delta(result_I, result_II, "prod_co_asym")}


def tdelta_co_len_mean(result_I, result_II):
    """prod_co_len_mean(Type_I) − prod_co_len_mean(Type_II)."""
    return {"tdelta_co_len_mean": _delta(result_I, result_II, "prod_co_len_mean")}


def tdelta_carboxylate_tilt(result_I, result_II):
    """prod_carboxylate_tilt(Type_I) − prod_carboxylate_tilt(Type_II)."""
    return {"tdelta_carboxylate_tilt": _delta(result_I, result_II, "prod_carboxylate_tilt")}


def tdelta_ni_ccarb(result_I, result_II):
    """prod_ni_ccarb(Type_I) − prod_ni_ccarb(Type_II)."""
    return {"tdelta_ni_ccarb": _delta(result_I, result_II, "prod_ni_ccarb")}


def tdelta_ni_alkene_centroid(result_I, result_II):
    """prod_ni_alkene_centroid(Type_I) − prod_ni_alkene_centroid(Type_II)."""
    return {"tdelta_ni_alkene_centroid": _delta(result_I, result_II, "prod_ni_alkene_centroid")}


def tdelta_bpy_dihedral(result_I, result_II):
    """prod_bpy_dihedral(Type_I) − prod_bpy_dihedral(Type_II)."""
    return {"tdelta_bpy_dihedral": _delta(result_I, result_II, "prod_bpy_dihedral")}


# Ordered registry of every pair (tdelta) descriptor function.
ALL = [
    tdelta_ni_Cb, tdelta_ni_o1, tdelta_newcc_Ca, tdelta_o_ni_bite_Cb,
    tdelta_metallacycle_vbur, tdelta_ni_n_mean, tdelta_abs_dni_n,
    tdelta_ni_bpyplane_dist, tdelta_coordplane_rms, tdelta_tau4,
    tdelta_metallacycle_perimeter, tdelta_cremer_pople_Q, tdelta_dih_ni_o_c_Ca,
    tdelta_dih_o_c_ca_cb, tdelta_cc_metallacycle_len, tdelta_cc_alternation,
    tdelta_o_c_o_angle, tdelta_co_asym, tdelta_co_len_mean,
    tdelta_carboxylate_tilt, tdelta_ni_ccarb, tdelta_ni_alkene_centroid,
    tdelta_bpy_dihedral,
]
