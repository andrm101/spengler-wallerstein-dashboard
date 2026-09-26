from pathlib import Path
from scripts.utils.paths import FIGURES

def test_timeline_figure_exists():
    assert (FIGURES / "di_timeline.png").exists()

def test_decomposition_figure_exists_for_usa():
    assert (FIGURES / "di_decomposition_USA_1925.png").exists()
