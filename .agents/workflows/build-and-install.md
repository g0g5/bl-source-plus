# Build and install the add-on ZIP

Build the legacy add-on ZIP from the repository root and install it through Blender's Add-ons preferences.

1. Run `uv run python scripts/build_addon.py`. The script reads `[project].version` from `pyproject.toml` with `tomllib` and writes `dist/bl_source_plus-<version>.zip`. It stages the source, skips `__pycache__` and compiled Python files, and puts all entries under the single `bl_source_plus/` folder required for installation.
2. In Blender 4.5 LTS, open **Edit > Preferences > Add-ons** and choose **Install from Disk** from the top-right menu. Select the ZIP in `dist/`, then enable the add-on. [Blender 4.5 LTS Add-ons manual](https://docs.blender.org/manual/en/4.5/editors/preferences/addons.html)

`dist/` is gitignored. The repository has no Python package build backend for `uv build`.
