"""Tests for DataManager class."""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from iqc_dashboard.app import DataManager


class TestDataManager:
    """Test suite for DataManager class."""
    
    def test_init(self, temp_dir):
        """Test DataManager initialization."""
        dm = DataManager(temp_dir)
        assert dm.temp_dir == Path(temp_dir)
        assert dm.parquet_files == []
        assert dm.temp_dir.exists()
    
    def test_save_uploaded_files(self, temp_dir):
        """Test saving uploaded files."""
        dm = DataManager(temp_dir)
        
        # Create mock uploaded files
        mock_file1 = Mock()
        mock_file1.name = "test1.parquet"
        mock_file1.getbuffer.return_value = b"test data 1"
        
        mock_file2 = Mock()
        mock_file2.name = "test2.parquet"
        mock_file2.getbuffer.return_value = b"test data 2"
        
        uploaded_files = [mock_file1, mock_file2]
        saved_paths = dm.save_uploaded_files(uploaded_files)
        
        assert len(saved_paths) == 2
        assert all(Path(p).exists() for p in saved_paths)
        assert dm.parquet_files == saved_paths
    
    def test_save_uploaded_files_with_none(self, temp_dir):
        """Test saving uploaded files with None values."""
        dm = DataManager(temp_dir)
        
        mock_file = Mock()
        mock_file.name = "test.parquet"
        mock_file.getbuffer.return_value = b"test data"
        
        uploaded_files = [mock_file, None]
        saved_paths = dm.save_uploaded_files(uploaded_files)
        
        assert len(saved_paths) == 1
        assert Path(saved_paths[0]).exists()
    
    @patch('iqc_dashboard.app.duckdb')
    def test_get_connection(self, mock_duckdb, temp_dir):
        """Test getting DuckDB connection."""
        mock_conn = Mock()
        mock_duckdb.connect.return_value = mock_conn
        
        # Mock streamlit cache_resource
        with patch('iqc_dashboard.app.st') as mock_st:
            mock_st.cache_resource = lambda x: x
            conn = DataManager.get_connection()
            assert conn == mock_conn
            mock_duckdb.connect.assert_called_once()
    
    def test_get_summary_stats_empty(self, temp_dir):
        """Test get_summary_stats with no files."""
        dm = DataManager(temp_dir)
        parquet_hash = dm._get_parquet_files_hash()
        result = dm.get_summary_stats(parquet_hash)
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    def test_get_summary_stats_with_data(self, temp_dir, sample_parquet_file):
        """Test get_summary_stats with actual data."""
        dm = DataManager(temp_dir)
        dm.parquet_files = [sample_parquet_file]
        
        # Setup mock connection
        mock_conn = Mock()
        mock_execute = Mock()
        mock_conn.execute.return_value = mock_execute
        
        # Return actual DataFrame with summary stats
        summary_df = pd.DataFrame({
            'total_rows': [3],
            'unique_formulas': [3],
            'converged_count': [2],
            'not_converged_count': [1]
        })
        mock_execute.df.return_value = summary_df
        
        # Mock streamlit and patch get_connection
        with patch('iqc_dashboard.app.st') as mock_st:
            mock_st.cache_resource = lambda x: x
            with patch.object(DataManager, 'get_connection', return_value=mock_conn):
                parquet_hash = dm._get_parquet_files_hash()
                result = dm.get_summary_stats(parquet_hash)
                
                assert isinstance(result, pd.DataFrame)
                assert not result.empty
                assert 'total_rows' in result.columns
                assert result['total_rows'].iloc[0] == 3
    
    def test_get_filtered_data_empty(self, temp_dir):
        """Test get_filtered_data with no files."""
        dm = DataManager(temp_dir)
        result = dm.get_filtered_data()
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    def test_get_filtered_data_with_filters(self, temp_dir, sample_parquet_file):
        """Test get_filtered_data with filters."""
        dm = DataManager(temp_dir)
        dm.parquet_files = [sample_parquet_file]
        
        # Setup mock connection
        mock_conn = Mock()
        mock_execute = Mock()
        mock_conn.execute.return_value = mock_execute
        
        # Return filtered DataFrame
        filtered_df = pd.DataFrame({
            'unique_name': ['mol_001', 'mol_002'],
            'formula': ['H2O', 'CO2'],
            'calculator': ['dft', 'dft'],
            'opt_converged': [True, True]
        })
        mock_execute.df.return_value = filtered_df
        
        # Mock streamlit and patch get_connection
        with patch('iqc_dashboard.app.st') as mock_st:
            mock_st.cache_resource = lambda x: x
            with patch.object(DataManager, 'get_connection', return_value=mock_conn):
                result = dm.get_filtered_data(calculator='dft', opt_converged=True)
                
                assert isinstance(result, pd.DataFrame)
                # Should filter to converged molecules
                if not result.empty:
                    assert all(result['opt_converged'] == True)
    
    def test_get_unique_values(self, temp_dir, sample_parquet_file):
        """Test get_unique_values."""
        dm = DataManager(temp_dir)
        dm.parquet_files = [sample_parquet_file]
        
        # Setup mock connection
        mock_conn = Mock()
        mock_execute = Mock()
        mock_conn.execute.return_value = mock_execute
        
        # Return DataFrame with unique values
        values_df = pd.DataFrame({
            'formula': ['H2O', 'CO2', 'NH3']
        })
        mock_execute.df.return_value = values_df
        
        # Mock streamlit and patch get_connection
        with patch('iqc_dashboard.app.st') as mock_st:
            mock_st.cache_resource = lambda x: x
            with patch.object(DataManager, 'get_connection', return_value=mock_conn):
                parquet_hash = dm._get_parquet_files_hash()
                values = dm.get_unique_values('formula', parquet_hash)
                
                assert isinstance(values, list)
                assert 'H2O' in values
                assert 'CO2' in values
                assert 'NH3' in values
    
    def test_get_unique_values_empty(self, temp_dir):
        """Test get_unique_values with no files."""
        dm = DataManager(temp_dir)
        parquet_hash = dm._get_parquet_files_hash()
        values = dm.get_unique_values('formula', parquet_hash)
        assert values == []
    
    def test_get_molecule_by_name(self, temp_dir, sample_parquet_file):
        """Test get_molecule_by_name."""
        dm = DataManager(temp_dir)
        dm.parquet_files = [sample_parquet_file]
        
        # Setup mock connection
        mock_conn = Mock()
        mock_execute = Mock()
        mock_conn.execute.return_value = mock_execute
        
        # Return DataFrame with molecule data
        molecule_df = pd.DataFrame({
            'unique_name': ['mol_001'],
            'formula': ['H2O'],
            'number_of_atoms': [3]
        })
        mock_execute.df.return_value = molecule_df
        
        # Mock streamlit and patch get_connection
        with patch('iqc_dashboard.app.st') as mock_st:
            mock_st.cache_resource = lambda x: x
            with patch.object(DataManager, 'get_connection', return_value=mock_conn):
                molecule = dm.get_molecule_by_name('mol_001')
                
                assert molecule is not None
                assert molecule['formula'] == 'H2O'
                assert molecule['unique_name'] == 'mol_001'
    
    def test_get_molecule_by_name_not_found(self, temp_dir, sample_parquet_file):
        """Test get_molecule_by_name with non-existent molecule."""
        dm = DataManager(temp_dir)
        dm.parquet_files = [sample_parquet_file]
        
        # Mock streamlit
        with patch('iqc_dashboard.app.st') as mock_st:
            mock_st.cache_resource = lambda x: x
            molecule = dm.get_molecule_by_name('nonexistent')
            assert molecule is None
    
    def test_get_molecule_by_index(self, temp_dir, sample_parquet_file):
        """Test get_molecule_by_index."""
        dm = DataManager(temp_dir)
        dm.parquet_files = [sample_parquet_file]
        
        # Setup mock connection
        mock_conn = Mock()
        mock_execute = Mock()
        mock_conn.execute.return_value = mock_execute
        
        # Return DataFrame with molecule data
        molecule_df = pd.DataFrame({
            'unique_name': ['mol_001'],
            'formula': ['H2O'],
            'number_of_atoms': [3]
        })
        mock_execute.df.return_value = molecule_df
        
        # Mock streamlit and patch get_connection
        with patch('iqc_dashboard.app.st') as mock_st:
            mock_st.cache_resource = lambda x: x
            with patch.object(DataManager, 'get_connection', return_value=mock_conn):
                molecule = dm.get_molecule_by_index(0)
                
                assert molecule is not None
                assert molecule['unique_name'] == 'mol_001'
    
    def test_get_all_molecule_names(self, temp_dir, sample_parquet_file):
        """Test get_all_molecule_names."""
        dm = DataManager(temp_dir)
        dm.parquet_files = [sample_parquet_file]
        
        # Setup mock connection
        mock_conn = Mock()
        mock_execute = Mock()
        mock_conn.execute.return_value = mock_execute
        
        # Return DataFrame with molecule names
        names_df = pd.DataFrame({
            'unique_name': ['mol_001', 'mol_002', 'mol_003']
        })
        mock_execute.df.return_value = names_df
        
        # Mock streamlit and patch get_connection
        with patch('iqc_dashboard.app.st') as mock_st:
            mock_st.cache_resource = lambda x: x
            with patch.object(DataManager, 'get_connection', return_value=mock_conn):
                parquet_hash = dm._get_parquet_files_hash()
                names = dm.get_all_molecule_names(parquet_hash)
                
                assert isinstance(names, list)
                assert len(names) == 3
                assert 'mol_001' in names
                assert 'mol_002' in names
                assert 'mol_003' in names

