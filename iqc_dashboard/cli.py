"""
Command-line interface for IQC Dashboard.
"""

import sys
from pathlib import Path
import subprocess


def main():
    """Run the Streamlit app."""
    # Get the path to the app.py file in the package
    package_dir = Path(__file__).parent
    app_file = package_dir / "app.py"
    
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(app_file)],
            check=True
        )
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        sys.exit(0)

