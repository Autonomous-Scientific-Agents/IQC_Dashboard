"""Tests for CLI module."""

import pytest
import subprocess
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from iqc_dashboard.cli import main


class TestCLI:
    """Test suite for CLI module."""

    @patch("iqc_dashboard.cli.subprocess.run")
    @patch("iqc_dashboard.cli._is_port_available", return_value=True)
    def test_main_success(self, mock_is_port_available, mock_run):
        """Test successful CLI execution."""
        mock_run.return_value = MagicMock(returncode=0)

        main([])

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "streamlit" in args
        assert "run" in args
        assert "--server.address=localhost" in args
        assert "--server.port=8501" in args
        assert "--browser.serverPort=8501" in args
        mock_is_port_available.assert_called_once_with("localhost", 8501)

    @patch("iqc_dashboard.cli.subprocess.run")
    @patch("iqc_dashboard.cli._is_port_available", return_value=True)
    def test_main_error(self, mock_is_port_available, mock_run):
        """Test CLI execution with error."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ["streamlit"])

        with pytest.raises(SystemExit) as exc_info:
            main([])

        assert exc_info.value.code == 1
        mock_is_port_available.assert_called_once_with("localhost", 8501)

    @patch("iqc_dashboard.cli.subprocess.run")
    @patch("iqc_dashboard.cli._is_port_available")
    def test_main_uses_next_available_port(self, mock_is_port_available, mock_run, capsys):
        """Test CLI picks the next available default port."""
        mock_is_port_available.side_effect = lambda host, port: port == 8502
        mock_run.return_value = MagicMock(returncode=0)

        main([])

        args = mock_run.call_args[0][0]
        assert "--server.port=8502" in args
        assert "--browser.serverPort=8502" in args
        assert "Port 8501 is in use" in capsys.readouterr().err

    @patch("iqc_dashboard.cli.subprocess.run")
    @patch("iqc_dashboard.cli._is_port_available", return_value=False)
    def test_main_exits_when_explicit_port_unavailable(
        self,
        mock_is_port_available,
        mock_run,
        capsys,
    ):
        """Test CLI exits when the requested port is unavailable."""
        with pytest.raises(SystemExit) as exc_info:
            main(["--port", "8600"])

        assert exc_info.value.code == 1
        assert "Port 8600 is not available on localhost." in capsys.readouterr().err
        mock_run.assert_not_called()
        mock_is_port_available.assert_called_once_with("localhost", 8600)

    @patch("iqc_dashboard.cli.subprocess.run")
    @patch("iqc_dashboard.cli._is_port_available", return_value=True)
    def test_main_accepts_streamlit_port_alias(self, mock_is_port_available, mock_run):
        """Test CLI accepts Streamlit-style port and address flags."""
        mock_run.return_value = MagicMock(returncode=0)

        main(["--server.port", "8601", "--server.address", "127.0.0.1"])

        args = mock_run.call_args[0][0]
        assert "--server.address=127.0.0.1" in args
        assert "--server.port=8601" in args
        assert "--browser.serverPort=8601" in args
        mock_is_port_available.assert_called_once_with("127.0.0.1", 8601)
