## Overview

Blender Source Plus is a Python add-on based on Blender Source Tools 3.4.3 that brings Valve Source Engine assets into Blender and exports them back to Source tools.

## Tech Stack

- Language: Python 3.12 (`.python-version`, `pyproject.toml`)
- Runtime / Framework: Blender 4.5 LTS (`bpy`, `bmesh`, `mathutils`) is the development and functional testing baseline. `bl_info` declares Blender 4.1.0 as the minimum version.
- Key Dependencies: Blender's bundled Python APIs at runtime and `fake-bpy-module-4-5` for development type stubs.
- Package Manager: `uv` manages the development environment (`package = false`). The build script packages the add-on for Blender.

## Structural Map

```
bl-source-plus/
|- pyproject.toml              # uv development configuration and add-on ZIP version
|- uv.lock                     # Locked development dependencies
|- scripts/
|  \- build_addon.py           # Builds the installable add-on ZIP
\- src/
   \- bl_source_plus/          # Blender add-on package and ZIP root folder
      |- __init__.py           # Add-on metadata, property groups, registration, and menu hooks
      |- utils.py              # Shared state, engine/compiler detection, formatting, and logging
      |- datamodel.py          # Standalone binary and KeyValues2 DMX codec
      |- export_smd.py         # SMD/DMX exporter and QC compile operator
      |- import_smd.py         # SMD, VTA, DMX, and QC importer
      |- flex.py               # Flex controllers, shape keys, and corrective drivers
      \- GUI.py                # 3D View sidebar panels in the Source Plus tab and other UI classes
```

`datamodel` is independent of Blender. `utils` and the core operators use it, `GUI` uses the operators, and `__init__` owns Blender registration.

## Commands

```powershell
# Sync development dependencies into .venv.
uv sync

# Build the installable ZIP in dist/. The build script handles packaging.
uv run python scripts/build_addon.py

# Run a Python script in the development environment.
uv run python path/to/script.py

# Use the Blender CLI workflow below for functional tests. The repository has no configured test, lint, typecheck, or format commands.
```

## Workflows

- [blender-functional-testing.md](.agents/workflows/blender-functional-testing.md) - Add-on functional testing with Blender CLI.
- [build-and-install.md](.agents/workflows/build-and-install.md) - Build and install the add-on ZIP.

## Notes

- [repository-maintenance.md](.agents/notes/repository-maintenance.md) - Upstream package history, updater status, and license notices.
