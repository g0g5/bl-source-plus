# Repository maintenance notes

The add-on retains upstream package history, update code, and source license notices.

- The upstream `io_scene_valvesource/` package was renamed to `src/bl_source_plus/`, which sets the installed module ID to `bl_source_plus`. Intra-package imports are relative.
- `update.py` still fetches updates from the original Blender Source Tools server and extracts archives into the parent of the installed package. It needs a project-specific update source to update Blender Source Plus.
- Most add-on source files are GPL-2.0-or-later. `datamodel.py` and `ordered_set.py` are MIT. See the source headers for the notices.
- `README.md` is empty. The repository has no `CONTRIBUTING`, `docs/`, CI configuration, or root `LICENSE`.
