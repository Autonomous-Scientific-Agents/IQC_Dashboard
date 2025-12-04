"""Tests for CLI module."""

import pytest
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from iqc_dashboard.cli import main


class TestCLI:
    """Test suite for CLI module."""
    
    @patch('iqc_dashboard.cli.subprocess.run')
    @patch('iqc_dashboard.cli.sys')
    def test_main_success(self, mock_sys, mock_run):
        """Test successful CLI execution."""
        mock_run.return_value = MagicMock(returncode=0)
        mock_sys.executable = '/usr/bin/python'
        
        main()
        
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert 'streamlit' in args
        assert 'run' in args
    
    @patch('iqc_dashboard.cli.subprocess.run')
    @patch('iqc_dashboard.cli.sys')
    def test_main_error(self, mock_sys, mock_run):
        """Test CLI execution with error."""
        mock_run.side_effect = MagicMock(returncode=1)
        mock_run.side_effect.__class__ = Exception
        mock_sys.exit = MagicMock()
        
        with pytest.raises(Exception):
            main()

