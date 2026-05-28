# Changelog

## [Unreleased]

### Added
- Added a new slide for `fig-rmonitoring.png` in `slides.md`.
- Added the `overleaf` remote configuration using Git Authentication Token for seamless LaTeX integration.
- Integrated the latest `main.tex` and Jonathan Morduch's `Notes2024.tex` directly from Overleaf (dated Jan 2026).
- Created `project_notes.md` to document the workspace layout and git workflows.
- Configured `.nojekyll` inside `.github/workflows/deploy.yml` to prevent GitHub Pages build failures on MyST assets.

### Changed
- Updated `notebooks/2-socfin_m.ipynb` to include the generation of `Im.png` using `mfi.plotIm()`.
- Renamed and retired outdated 2022 draft materials into a dedicated subfolder `paper/archive/old_local_2022/`.
- Cleaned up python packaging files, pointing `setup.py` packages target directly to `socialfinance/`.

### Removed
- Removed redundant `src/` duplicate packages folder.
- Cleaned up local `.egg-info` directories and build-artifacts from git history.
- Untracked local-only folders `archive/`, `log/`, and `data/Findex/` from GitHub remote using `git rm --cached` while preserving them fully on local Y: drive.
