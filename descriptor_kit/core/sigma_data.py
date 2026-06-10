"""Curated literature Hammett / Taft sigma table (spec §6, decision log §1).

Verbatim copy of ``src/sigma_data.py``.  Keyed by the *exact canonical SMILES*
emitted by ``hammett.fragment_smiles`` (capped, metal-free fragment).  Each value
records the substituent identity, the element of the **attachment atom**
(``attach``), and the literature constants (``sigma_p``/``sigma_m``/
``sigma_star``/``sigma_I``).  Missing values are ``float('nan')`` and never
guessed.

Primary source for aromatic constants: C. Hansch, A. Leo, R. W. Taft, Chem.
Rev. 1991, 91, 165-195; Taft sigma* / sigma_I: Taft (1956);
Perrin-Dempsey-Serjeant.
"""
from __future__ import annotations

NAN = float("nan")

# Canonical-SMILES -> {identity, attach, sigma_p, sigma_m, sigma_star, sigma_I}
SIGMA_TABLE: dict[str, dict] = {

    # ---- reference: hydrogen substituent (alkyne -H) -------------------
    "[H][H]": {
        "identity": "-H (hydrogen, reference)", "attach": "H",
        "sigma_p": 0.00, "sigma_m": 0.00, "sigma_star": 0.49, "sigma_I": 0.00,
    },

    # ---- halogens ------------------------------------------------------
    "[H]F": {
        "identity": "-F (fluoro)", "attach": "F",
        "sigma_p": 0.06, "sigma_m": 0.34, "sigma_star": 3.21, "sigma_I": 0.52,
    },
    "[H]Cl": {
        "identity": "-Cl (chloro)", "attach": "Cl",
        "sigma_p": 0.23, "sigma_m": 0.37, "sigma_star": 2.96, "sigma_I": 0.47,
    },

    # ---- simple alkyl --------------------------------------------------
    "[H]C([H])([H])[H]": {
        "identity": "-CH3 (methyl)", "attach": "C",
        "sigma_p": -0.17, "sigma_m": -0.07, "sigma_star": 0.00, "sigma_I": -0.04,
    },
    "[H]C([H])([H])C([H])([H])[H]": {
        "identity": "-CH2CH3 (ethyl)", "attach": "C",
        "sigma_p": -0.15, "sigma_m": -0.07, "sigma_star": -0.10, "sigma_I": -0.05,
    },
    # isobutyl -CH2CH(CH3)2 : Hansch-Leo i-Bu (primary alkyl)
    "[H]C([H])([H])C([H])(C([H])([H])[H])C([H])([H])[H]": {
        "identity": "-CH2CH(CH3)2 (isobutyl)", "attach": "C",
        "sigma_p": -0.12, "sigma_m": -0.07, "sigma_star": -0.13, "sigma_I": -0.05,
    },

    # ---- fluoroalkyl ---------------------------------------------------
    "[H]C(F)(F)F": {
        "identity": "-CF3 (trifluoromethyl)", "attach": "C",
        "sigma_p": 0.54, "sigma_m": 0.43, "sigma_star": 2.61, "sigma_I": 0.40,
    },

    # ---- oxygen-attached ----------------------------------------------
    "[H]O[H]": {
        "identity": "-OH (hydroxyl)", "attach": "O",
        "sigma_p": -0.37, "sigma_m": 0.12, "sigma_star": 1.34, "sigma_I": 0.29,
    },
    "[H]OC([H])([H])[H]": {
        "identity": "-OCH3 (methoxy)", "attach": "O",
        "sigma_p": -0.27, "sigma_m": 0.12, "sigma_star": 1.81, "sigma_I": 0.30,
    },
    "[H]OC(=O)C([H])([H])[H]": {
        "identity": "-OC(=O)CH3 (acetoxy, OAc)", "attach": "O",
        "sigma_p": 0.31, "sigma_m": 0.39, "sigma_star": NAN, "sigma_I": 0.38,
    },

    # ---- carbon-attached carboxyl --------------------------------------
    # Capped SMILES is formic acid, but in this dataset the attachment is ALWAYS
    # the carbon (root=C, verified on all 1,836 occurrences) -> carboxylic acid
    # -COOH (the dcbpy / carboxy-alkyne motif), NOT formyloxy -OCHO.
    "[H]OC([H])=O": {
        "identity": "-C(=O)OH (carboxyl)", "attach": "C",
        "sigma_p": 0.45, "sigma_m": 0.37, "sigma_star": NAN, "sigma_I": 0.34,
    },

    # ---- nitrogen-attached --------------------------------------------
    "[H]N([H])[H]": {
        "identity": "-NH2 (amino)", "attach": "N",
        "sigma_p": -0.66, "sigma_m": -0.16, "sigma_star": NAN, "sigma_I": 0.17,
    },
    "[H]N(C([H])([H])[H])C([H])([H])[H]": {
        "identity": "-N(CH3)2 (dimethylamino)", "attach": "N",
        "sigma_p": -0.83, "sigma_m": -0.16, "sigma_star": NAN, "sigma_I": 0.17,
    },
    "[H][N+](=O)[O-]": {
        "identity": "-NO2 (nitro)", "attach": "N",
        "sigma_p": 0.78, "sigma_m": 0.71, "sigma_star": NAN, "sigma_I": 0.65,
    },

    # ---- aryl ----------------------------------------------------------
    "[H]c1c([H])c([H])c([H])c([H])c1[H]": {
        "identity": "-C6H5 (phenyl)", "attach": "C",
        "sigma_p": -0.01, "sigma_m": 0.06, "sigma_star": 0.60, "sigma_I": 0.12,
    },
    # 4-methoxyphenyl -C6H4-OCH3 : FLAGGED (no standard substituted-aryl group
    # constant; user decision = leave NaN).
    "[H]c1c([H])c([H])c(OC([H])([H])[H])c([H])c1[H]": {
        "identity": "-C6H4-OCH3 (4-methoxyphenyl) [FLAGGED: NaN by user decision]",
        "attach": "C",
        "sigma_p": NAN, "sigma_m": NAN, "sigma_star": NAN, "sigma_I": NAN,
    },
    # 4-(trifluoromethoxy)phenyl -C6H4-OCF3 : FLAGGED (NaN by user decision).
    "[H]c1c([H])c([H])c(OC(F)(F)F)c([H])c1[H]": {
        "identity": "-C6H4-OCF3 (4-(trifluoromethoxy)phenyl) [FLAGGED: NaN by user decision]",
        "attach": "C",
        "sigma_p": NAN, "sigma_m": NAN, "sigma_star": NAN, "sigma_I": NAN,
    },
}

# Substituent SMILES deliberately left NaN (surfaced to and confirmed by user).
FLAGGED: set[str] = {
    "[H]c1c([H])c([H])c(OC([H])([H])[H])c([H])c1[H]",  # 4-methoxyphenyl
    "[H]c1c([H])c([H])c(OC(F)(F)F)c([H])c1[H]",         # 4-(trifluoromethoxy)phenyl
}
