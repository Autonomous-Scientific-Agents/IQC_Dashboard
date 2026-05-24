"""Tests for selection state helpers used by Streamlit navigation controls."""

import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from iqc_dashboard.app import move_indexed_selection, sync_indexed_selection


def test_move_indexed_selection_updates_value_and_index():
    """Test Next updates both the selectbox value and selected index."""
    state = {
        "selected_molecule_index": 0,
        "selected_molecule_select": "mol_a",
    }
    molecule_names = ["mol_a", "mol_b", "mol_c"]

    result = move_indexed_selection(
        state,
        molecule_names,
        "selected_molecule_select",
        1,
        "selected_molecule_index",
    )

    assert result == 1
    assert state["selected_molecule_index"] == 1
    assert state["selected_molecule_select"] == "mol_b"

def test_move_indexed_selection_clamps_at_bounds():
    """Test navigation does not move outside available options."""
    state = {
        "selected_molecule_index": 2,
        "selected_molecule_select": "mol_c",
    }
    molecule_names = ["mol_a", "mol_b", "mol_c"]

    result = move_indexed_selection(
        state,
        molecule_names,
        "selected_molecule_select",
        1,
        "selected_molecule_index",
    )

    assert result == 2
    assert state["selected_molecule_index"] == 2
    assert state["selected_molecule_select"] == "mol_c"


def test_sync_indexed_selection_repairs_stale_selectbox_value():
    """Test filters or data changes repair stale selected values before rendering."""
    state = {
        "selected_molecule_index": 4,
        "selected_molecule_select": "old_mol",
    }
    molecule_names = ["mol_a", "mol_b"]

    result = sync_indexed_selection(
        state,
        molecule_names,
        "selected_molecule_select",
        "selected_molecule_index",
    )

    assert result == 1
    assert state["selected_molecule_index"] == 1
    assert state["selected_molecule_select"] == "mol_b"
