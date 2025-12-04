"""
IQC Dashboard - Computational Chemistry Dashboard

A high-performance Streamlit app for analyzing computational chemistry data
from Parquet files with 3D molecular visualization.
"""

__version__ = "0.1.0"

from iqc_dashboard.app import main, DataManager, render_molecule

__all__ = ["main", "DataManager", "render_molecule"]

