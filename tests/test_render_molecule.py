"""Tests for render_molecule function."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from iqc_dashboard.app import render_molecule, STMOL_AVAILABLE, PY3DMOL_AVAILABLE


class TestRenderMolecule:
    """Test suite for render_molecule function."""
    
    def test_render_molecule_with_none_xyz(self):
        """Test render_molecule with None XYZ string."""
        with patch('iqc_dashboard.app.st') as mock_st:
            render_molecule(None, label="Test")
            mock_st.warning.assert_called()
    
    def test_render_molecule_with_empty_xyz(self):
        """Test render_molecule with empty XYZ string."""
        with patch('iqc_dashboard.app.st') as mock_st:
            render_molecule("", label="Test")
            mock_st.warning.assert_called()
    
    def test_render_molecule_without_stmol(self):
        """Test render_molecule when stmol is not available."""
        with patch('iqc_dashboard.app.STMOL_AVAILABLE', False):
            with patch('iqc_dashboard.app.st') as mock_st:
                xyz = "3\nH2O\nH 0.0 0.0 0.0\nO 0.0 0.0 0.96\nH 0.87 0.0 0.39"
                render_molecule(xyz, label="Test")
                mock_st.error.assert_called()
    
    def test_render_molecule_without_py3dmol(self):
        """Test render_molecule when py3Dmol is not available."""
        with patch('iqc_dashboard.app.STMOL_AVAILABLE', True):
            with patch('iqc_dashboard.app.PY3DMOL_AVAILABLE', False):
                with patch('iqc_dashboard.app.st') as mock_st:
                    xyz = "3\nH2O\nH 0.0 0.0 0.0\nO 0.0 0.0 0.96\nH 0.87 0.0 0.39"
                    render_molecule(xyz, label="Test")
                    mock_st.error.assert_called()
    
    @patch('iqc_dashboard.app.stmol')
    @patch('iqc_dashboard.app.py3Dmol')
    def test_render_molecule_success(self, mock_py3dmol, mock_stmol):
        """Test successful molecule rendering."""
        # Mock the libraries
        with patch('iqc_dashboard.app.STMOL_AVAILABLE', True):
            with patch('iqc_dashboard.app.PY3DMOL_AVAILABLE', True):
                with patch('iqc_dashboard.app.st') as mock_st:
                    # Setup mocks
                    mock_view = MagicMock()
                    mock_py3dmol.view.return_value = mock_view
                    
                    xyz = "3\nH2O\nH 0.0 0.0 0.0\nO 0.0 0.0 0.96\nH 0.87 0.0 0.39"
                    render_molecule(xyz, style='stick', label="Test")
                    
                    # Verify py3Dmol was called
                    mock_py3dmol.view.assert_called_once_with(width=400, height=400)
                    mock_view.addModel.assert_called_once_with(xyz, 'xyz')
                    mock_view.setStyle.assert_called()
                    mock_view.zoomTo.assert_called_once()
                    mock_view.render.assert_called_once()
                    mock_stmol.showmol.assert_called_once()
    
    @patch('iqc_dashboard.app.stmol')
    @patch('iqc_dashboard.app.py3Dmol')
    def test_render_molecule_different_styles(self, mock_py3dmol, mock_stmol):
        """Test render_molecule with different styles."""
        with patch('iqc_dashboard.app.STMOL_AVAILABLE', True):
            with patch('iqc_dashboard.app.PY3DMOL_AVAILABLE', True):
                with patch('iqc_dashboard.app.st'):
                    mock_view = MagicMock()
                    mock_py3dmol.view.return_value = mock_view
                    
                    xyz = "3\nH2O\nH 0.0 0.0 0.0\nO 0.0 0.0 0.96\nH 0.87 0.0 0.39"
                    
                    # Test sphere style
                    render_molecule(xyz, style='sphere')
                    mock_view.setStyle.assert_called_with({'sphere': {'radius': 0.5}})
                    
                    # Test cartoon style
                    mock_view.reset_mock()
                    render_molecule(xyz, style='cartoon')
                    mock_view.setStyle.assert_called_with({'cartoon': {}})
                    
                    # Test default style
                    mock_view.reset_mock()
                    render_molecule(xyz, style='unknown')
                    mock_view.setStyle.assert_called_with({'stick': {}, 'sphere': {'radius': 0.3}})

