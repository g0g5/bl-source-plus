---
name: blender-cli
description: Drive a local Blender headless from the shell: scaffold, build, animate, verify, render and export 3D scenes with JSON in and JSON out. Use when a task needs Blender without a GUI, an MCP server or an add-on.
---

# blender-cli 0.8.1

Run `blender-cli doctor` first. Every command prints ONE JSON object on stdout and exits 1 exactly when `ok` is false; add `-H` to pretty-print. Nothing persists unless you pass `--save` (scene state) or an output path (`render`, `export`, `snapshot`).

## The loop

1. Build: `new`, `import`, `add`, `material`, `keyframe`, or `exec` for anything else bpy can do (gate it with `--check` / `--safe`).
2. Look: `scene` (state), `verify` (lint), `snapshot` (multi-view contact sheet with coverage stats).
3. Deliver: `render` (still or `--animation`; `--detach` then `job wait` for long ones), `export` (with a fidelity census).

## Commands

| usage | effects | what it does |
|---|---|---|
| `blender-cli diff <before.blend> <after.blend> [--frame N] [--tolerance N] [--fail-on-change]` | read | Read-only comparison of object names, hierarchy, transforms, evaluated geometry, bounds, material assignments and scene settings. |
| `blender-cli assets search [query] [--type hdri|texture|model] [--category name] [--limit N] [--refresh]` | network, files | Discover Poly Haven IDs by name, category and tags before importing; returns source URL and license. |
| `blender-cli receipt verify <receipt.json>` | read | Recheck a passing acceptance receipt against its current source, spec and optional snapshot SHA-256 and size. |
| `blender-cli doctor` | read | Locate Blender, verify headless bpy, report version support, import/export formats, engines, GPU devices, enabled add-ons and API generation. Run first. |
| `blender-cli new <name> [--save f.blend]` | files | Scaffold a clean project (camera + key light + 1080p) and save it. |
| `blender-cli exec "<bpy>" [--blend f] [--save f] [--check] [--safe] [--unsafe] [--expect-sha256 hex] [--diff] [--detach]` | code, scene | Run agent-authored bpy; keys set on result come back as JSON. A failure on a known API move carries api_drift hints; --expect-sha256 binds a run to reviewed code. |
| `blender-cli run <script.py> [--blend f] [--save f] [--check] [--safe] [--unsafe] [--expect-sha256 hex] [--diff] [--detach]` | code, scene | Same as exec, from a .py file. |
| `blender-cli scene [--blend f]` | read | Dump objects (transforms, F-curve and keyframe counts), frame range, engine, resolution, materials, cameras and lights as JSON. |
| `blender-cli nodes find [--kind geometry|shader|compositor|all] [--search pattern] [--limit N] | nodes inspect [--group pattern] [--blend f]` | read | Discover node types (id, label, description) from the running Blender or inspect bounded node/link graphs from a scene. |
| `blender-cli camera [name] [--blend f] [--frame N]` | read | Report camera intrinsics K, Blender and OpenCV extrinsics, pixel/sensor metadata, coordinate convention and a principal-point reprojection check. |
| `blender-cli verify [--blend f] [--tolerance 0.001] [--fail-on error|warn|none] [--no-mesh]` | read | Lint the scene: missing camera, empty meshes, bad transforms, real overlaps, off-camera objects, plus mesh health (loose geometry, non-manifold, zero-area faces, winding, convex colliders, modifier order). |
| `blender-cli snapshot [--blend f] --out sheet.png [--views front,right,top,persp] [--res 512x384] [--shading random|material|solid] [--frame N]` | files | Cheap multi-view Workbench capture tiled into one PNG, with per-view coverage, occupied bbox, luminance and a blank flag, so the build can be checked without a full render. |
| `blender-cli accept <acceptance.json> --blend scene.blend [--receipt result.json]` | read, files | Apply declarative object/type/frame/verify/snapshot requirements and write a receipt bound to the spec, source scene and visual evidence hashes. |
| `blender-cli add <kind> [--name N] [--at x,y,z] [--rot x,y,z] [--size N] [--scale x,y,z] [--look-at x,y,z] [--type T] [--energy N] [--color c] [--text T] [--lens mm] [--blend f] [--save f] | add --json "[...]"` | scene | Add a primitive (cube sphere icosphere plane cylinder cone torus monkey), camera, light, empty or text by name, in one Blender launch; returns the resulting objects. |
| `blender-cli keyframe <object> --frame N [--prop location|rotation|scale|<data.path>] [--value x,y,z] [--interp linear|bezier|constant] [--no-extend] [--blend f] [--save f] | keyframe --json "[...]"` | scene | Set a property and insert a keyframe on a named object (rotation in degrees); works on both legacy and slotted actions; returns per-object keyframe counts. |
| `blender-cli material <object> [--name M] [--color r,g,b|#hex] [--roughness 0..1] [--metallic 0..1] [--alpha 0..1] [--emission r,g,b|#hex] [--emission-strength N] [--blend f] [--save f]` | scene | Create or update a Principled BSDF material and assign it to a named object, using the 4.0+ socket names with fallbacks. |
| `blender-cli import <file | polyhaven:id> [--blend f] [--save f] [--type hdri|texture|model] [--res 1k|2k|4k] [--maps a,b] [--pack] | import --batch "assets/*.glb"` | scene, network | Import local assets or fetch Poly Haven assets; reports the arrived objects with their parents and roots, and fails when an import adds nothing. |
| `blender-cli generate "<prompt>" | generate --image ref.png [--out f.glb] [--import] [--pack] [--allow-empty] [--blend f] [--save f] [--wait sec] [--backend meshy]` | network, files, scene | Text- or image-to-3D via Meshy (needs MESHY_API_KEY); downloads the GLB, optionally imports it. |
| `blender-cli export <out.glb|gltf|obj|fbx|stl|ply|usd> [--blend f] [--selected] [--no-verify] [--strict] [--animations on|off] | export <dir> --batch "b/*.blend" --format glb` | files | Write the scene out, hash it, read it back and report format-aware fidelity across geometry, material slots, UVs, colour-channel variance, shape keys and animation. |
| `blender-cli render [--blend f] --out p.png [--frame N] [--res WxH] [--engine E] [--device auto|cpu|cuda|optix|metal|hip|oneapi] [--threads N] [--samples N] [--denoise on|off] [--detach] | render --animation --out clip.mp4 [--frames 1..48] [--fps 24] | render --batch "shots/*.blend" --out dir/` | files, process | Render a still, video or sequence with non-empty artifact proof, SHA-256, actual format/codec metadata, and an optional fail-closed acceptance gate. |
| `blender-cli job list | status <id> | wait <id> [--timeout sec] [--poll sec] [--stall-after sec] | cancel <id>` | process | Inspect, wait for or cancel detached renders/execs; status reports frames done (and percent when the range is known), seconds since the last output, or the final result. |
| `blender-cli addon list [--all] | enable <module> [--no-persist] | disable <module> [--no-persist] | install <file.py|.zip> [--enable] [--no-persist]` | prefs, files | List, enable, disable or install add-ons and extensions headless; enable persists to user preferences unless --no-persist. |
| `blender-cli install codex|claude|all|doctor [--global]` | files | Idempotently install or verify the generated skill for Codex and Claude Code. |
| `blender-cli schema [--command a,b] [--effects read,files] [--compact] [--skill] [--out file]` | read | Machine-readable command manifest, optionally filtered or compacted to fit an agent context, or rendered as a drop-in skill. |
| `blender-cli version` | read | Print name and version. |

## Effects

- **read**: inspects only; writes nothing
- **scene**: mutates the loaded scene in memory; persisted only with --save
- **files**: writes files at the paths you give (overwrites)
- **code**: executes agent-authored Python inside Blender; gate it with --check / --safe
- **network**: calls an external service
- **prefs**: changes Blender user preferences on this machine
- **process**: starts or stops a background Blender process

Common flags on every Blender-running command: `--blender <path>`, `--timeout <sec>`, `--addons <a,b>`, `--human`. Machine-readable version of this file: `blender-cli schema`.
