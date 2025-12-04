"""Pytest configuration and fixtures."""

import pytest
import tempfile
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
import numpy as np


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_parquet_file(temp_dir):
    """Create a sample Parquet file with IQC-like data."""
    data = {
        'unique_name': ['mol_001', 'mol_002', 'mol_003'],
        'formula': ['H2O', 'CO2', 'NH3'],
        'number_of_atoms': [3, 3, 4],
        'number_of_electrons': [10, 22, 10],
        'spin': [0.0, 0.0, 0.0],
        'calculator': ['dft', 'dft', 'dft'],
        'task': ['opt', 'opt', 'opt'],
        'model': ['model1', 'model1', 'model1'],
        'initial_energy_eV': [-10.5, -20.3, -15.2],
        'opt_energy_eV': [-10.6, -20.4, -15.3],
        'opt_converged': [True, True, False],
        'opt_steps': [10, 15, 20],
        'opt_time': [1.5, 2.0, 2.5],
        'initial_xyz': [
            '3\nH2O\nH 0.0 0.0 0.0\nO 0.0 0.0 0.96\nH 0.87 0.0 0.39',
            '3\nCO2\nC 0.0 0.0 0.0\nO 1.16 0.0 0.0\nO -1.16 0.0 0.0',
            '4\nNH3\nN 0.0 0.0 0.0\nH 0.0 0.94 0.0\nH 0.82 -0.31 0.0\nH -0.82 -0.31 0.0'
        ],
        'opt_xyz': [
            '3\nH2O optimized\nH 0.0 0.0 0.0\nO 0.0 0.0 0.97\nH 0.88 0.0 0.40',
            '3\nCO2 optimized\nC 0.0 0.0 0.0\nO 1.17 0.0 0.0\nO -1.17 0.0 0.0',
            '4\nNH3 optimized\nN 0.0 0.0 0.0\nH 0.0 0.95 0.0\nH 0.83 -0.32 0.0\nH -0.83 -0.32 0.0'
        ],
        'vibrational_frequencies_cm^-1': [
            [100, 200, 300],
            [150, 250, 350],
            [120, 220, 320, 420]
        ],
        'G_eV': [-10.7, -20.5, -15.4],
        'H_eV': [-10.6, -20.4, -15.3],
        'S_eV/K': [0.001, 0.002, 0.0015],
    }
    
    df = pd.DataFrame(data)
    file_path = Path(temp_dir) / 'test_data.parquet'
    
    # Convert list columns to proper format for Parquet
    table = pa.Table.from_pandas(df)
    pq.write_table(table, file_path)
    
    return str(file_path)


@pytest.fixture
def sample_parquet_files(temp_dir, sample_parquet_file):
    """Create multiple sample Parquet files."""
    # Copy the first file and create a second one
    import shutil
    file1 = Path(sample_parquet_file)
    file2 = Path(temp_dir) / 'test_data_2.parquet'
    shutil.copy(file1, file2)
    
    return [str(file1), str(file2)]


@pytest.fixture
def mock_streamlit():
    """Mock Streamlit for testing."""
    class MockStreamlit:
        @staticmethod
        def cache_resource(func):
            return func
        
        @staticmethod
        def error(msg):
            print(f"STREAMLIT ERROR: {msg}")
        
        @staticmethod
        def warning(msg):
            print(f"STREAMLIT WARNING: {msg}")
    
    return MockStreamlit

