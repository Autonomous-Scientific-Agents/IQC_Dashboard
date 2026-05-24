"""
IQC Dashboard - Computational Chemistry Dashboard

A high-performance Streamlit app for analyzing computational chemistry data
from Parquet files with 3D molecular visualization.
"""

__version__ = "0.1.0"

__all__ = ["main", "DataManager", "render_molecule"]


def __getattr__(name):
    """Lazily expose app objects without importing Streamlit during CLI startup."""
    if name in __all__:
        from iqc_dashboard.app import DataManager, main, render_molecule

        exports = {
            "main": main,
            "DataManager": DataManager,
            "render_molecule": render_molecule,
        }
        return exports[name]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
