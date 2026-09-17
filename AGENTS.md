## Project Overview
A Blender add-on for importing and exporting Valve Source Engine assets (SMD, DMX, QC). Currently a rename/repackage of "Blender Source Tools" v3.4.3 as the base for a more modern, feature-complete add-on. `uv` manages the dev environment only.

## Tech Stack
- Language: Python 3.12 (`.python-version`, `pyproject.toml`)
- Runtime / Framework: Blender 4.1+ add-on (`bpy`, `bmesh`, `mathutils`)
- Key Dependencies: none at runtime; dev-only `fake-bpy-module-4-5` for `bpy` type stubs
- Package Manager: `uv` (non-package project; dev env + dependency management only)

## Structural Map

```
bl-source-plus/
|- pyproject.toml              # uv project def (dev env only, package = false); no build backend
|- uv.lock                     # Lockfile (dev dep fake-bpy-module-4-5 only)
|- scripts/
|  \- build_addon.py           # Packages src/bl_source_plus into dist/bl_source_plus-<version>.zip
|- dist/                       # Build products (gitignored); installable add-on zips
\- src/
   \- bl_source_plus/          # The Blender add-on package (zip root folder when installed)
      |- __init__.py           # Add-on entrypoint: bl_info, PropertyGroups, register()/unregister(), menu hooks
      |- utils.py              # Shared base: State singleton, engine/compiler detection, formatting/logging helpers
      |- datamodel.py          # Standalone DMX read/write (binary + KeyValues2); no bpy dependency
      |- export_smd.py         # SMD/DMX exporter and QC compile operator
      |- import_smd.py         # SMD/QC importer operator
      |- flex.py               # Flex controller + shape-key/corrective-driver logic
      |- GUI.py                # Blender panels, menus, UIList, config operators
      |- translations.py       # Localized display strings (EN/JP)
      |- update.py             # In-addon self-updater (still points at the original BST server)
      \- ordered_set.py        # Vendored MIT OrderedSet utility
```

Module dependency direction: `datamodel` is a standalone leaf; `utils` depends on `datamodel`; the core operators depend on `utils`/`datamodel`; `GUI` and the add-on `__init__` sit on top and own Blender registration.

## Development Guide
### Commands

```
# Install/sync dependencies (creates .venv; does not install the add-on)
uv sync

# Build the installable add-on zip -> dist/bl_source_plus-<version>.zip
uv run python scripts/build_addon.py

# Run Python in the project env
uv run python <script>
```

There is no test, lint, typecheck, or format command configured in this repo. Do not assume one exists. `uv build` is intentionally unavailable (no build backend).

### Workflows
- **Building the add-on**: run `scripts/build_addon.py`. It reads the version from `[project].version` in `pyproject.toml` (via `tomllib`) for the zip filename, stages the source excluding `__pycache__`/compiled files, and writes a zip whose single top-level folder is `bl_source_plus/` (required by Blender's install-from-zip).
- **Installing**: in Blender 4.1+, *Edit > Preferences > Add-ons > Install...* and pick the zip from `dist/`.

## Notes
- The add-on cannot be exercised from the CLI; functional verification requires loading it in Blender 4.1+ (its `__init__.py` supports `register()` under `__main__`).
- The add-on package was renamed from the vendored `io_scene_valvesource/` to `src/bl_source_plus/`. All imports are relative, so only the install module id changed; the underlying Blender Source Tools logic is untouched for now.
- `update.py` still self-updates from the original Blender Source Tools server and extracts into the package's parent directory; it is effectively non-functional for this project until repointed.
- `README.md` is empty and there is no `CONTRIBUTING`, `docs/`, CI, or root `LICENSE`.
- Licensing is mixed: most add-on files are GPL-2.0-or-later; `datamodel.py` and `ordered_set.py` are MIT.
