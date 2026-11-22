# Add-on functional testing with Blender CLI

Run add-on functional tests with the standalone [`blender-cli`](https://github.com/renezander030/blender-cli) program and Blender 4.5 LTS. Follow the project’s [Blender CLI skill](../skills/blender-cli/SKILL.md) for commands and options.

1. Pick the smallest representative case for the change, such as add-on registration, SMD import, or DMX export. Define the expected result before running it.
2. Load and register `bl_source_plus` from the current checkout’s `src/` in an isolated Blender profile. For a packaging change, install and test the built ZIP in that profile.
3. Exercise the affected add-on entry point. For import, check the resulting scene data. For export, check the generated asset’s relevant contents. Use a temporary location for test outputs.
4. Report the `blender-cli` and Blender versions, the case exercised and the assertion results. Identify any GUI behavior or external Source Engine tools that still need verification.
