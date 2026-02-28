"""
Root entrypoint for Streamlit.

This repository's app lives under `Attached-Assets/main.py`, but many users run:

    streamlit run main.py

from the repo root. This thin wrapper delegates to the real app.

Keeping logic in a single place avoids duplication and ensures tests and the UI
stay in sync.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def _run_attached_assets_main() -> None:
    repo_root = Path(__file__).parent
    attached_assets_dir = repo_root / "Attached-Assets"
    target = attached_assets_dir / "main.py"

    if not target.exists():
        raise FileNotFoundError(f"Streamlit entrypoint not found: {target}")

    # Ensure imports inside Attached-Assets/ work (e.g. `from utils...`, `from models...`)
    attached_assets_str = str(attached_assets_dir)
    if attached_assets_str not in sys.path:
        sys.path.insert(0, attached_assets_str)

    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    _run_attached_assets_main()
