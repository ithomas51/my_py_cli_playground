# Changelog

## [0.1.0] - 2025-11-07
### Added
- Initial packaging with `pyproject.toml` (hatchling).
- Console scripts: `ico-to-svg` (primary), `ico2svg` (alias).
- Subcommands: `convert` (raster/vector) and `info` (size listing, `--json`).
- Size selection logic (exact → nearest larger → largest; tie-break square then area).
- Default `--alpha-threshold` set to 16.
- Programmatic API `convert_ico_to_svg`.
- Deprecation shim `ico_to_svg.py` warning for legacy invocation.

### Removed
- Unused dependency `colorgram.py`.

### Notes
- Shim will be removed after two minor releases.
