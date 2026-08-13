"""Locate the calibration tree and the frozen analysis module in either layout.

These scripts were written inside the vault, where the calibration tree sits at
`../phase0_calibration/` and the estimators are `phase0_5/src/02_phase0_5_analysis.py`. The public
repository is flattened — `results/`, `data/` and `src/` live at the repository root — and `phase0_5/`
was renamed to `robustness/` before release. A script that hardcodes either layout is dead on arrival
in the other, which is what happened when the arms were first committed.

Resolution is by probing for files that must exist, not by guessing from the directory name.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Ordered by specificity: the vault's nested tree first, then the flattened repository root.
_ROOT_CANDIDATES = [HERE.parent / "phase0_calibration", HERE.parent, HERE.parent.parent]
_MODULE_CANDIDATES = [
    Path("phase0_5") / "src" / "02_phase0_5_analysis.py",   # vault
    Path("robustness") / "src" / "02_robustness_analysis.py",  # public repository
]
_REQUIRED = [Path("results") / "analysis_final.csv"]


def calibration_root() -> Path:
    for root in _ROOT_CANDIDATES:
        if root.is_dir() and all((root / r).exists() for r in _REQUIRED):
            return root
    tried = "\n  ".join(str(c) for c in _ROOT_CANDIDATES)
    raise SystemExit(
        "cannot locate the calibration tree. Looked for results/analysis_final.csv under:\n  " + tried
    )


def analysis_module():
    """Import the frozen estimator module under whichever name this tree uses."""
    root = calibration_root()
    for rel in _MODULE_CANDIDATES:
        path = root / rel
        if path.exists():
            spec = importlib.util.spec_from_file_location("frozen_analysis", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    tried = "\n  ".join(str(root / c) for c in _MODULE_CANDIDATES)
    raise SystemExit("cannot locate the frozen analysis module. Tried:\n  " + tried)


def structures_module():
    """Import the frozen distance definition, which only the vault layout ships under src/."""
    root = calibration_root()
    for rel in (Path("src") / "02_structures.py",):
        path = root / rel
        if path.exists():
            spec = importlib.util.spec_from_file_location("frozen_structures", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    raise SystemExit(f"cannot locate src/02_structures.py under {root}")
