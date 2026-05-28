# Project Notes & Workflows

This document outlines the organization and development workflows for the **Social Finance** paper and codebase consolidation project.

---

## Workspace Structure

The project has been consolidated into a single definitive git-tracked workspace located on the **Y drive** (to prevent sync conflicts with Dropbox):

*   **Repository Location:** `y:\jpapers\siv\social-finance`
*   **Active Remote (GitHub):** `https://github.com/jhconning/sfinance.git`
*   **Overleaf Remote:** `https://git@git.overleaf.com/62167876d91ea90954bfaf60`

### Directory Layout

*   [paper/](file:///y:/jpapers/siv/social-finance/paper/) — Holds active modernized LaTeX source files and bibliography.
    *   `main.tex` — Active paper body (integrated from Overleaf 2026).
    *   `Notes2024.tex` — Active draft notes and sections written by Jonathan Morduch.
    *   `references.bib` — Active references bibliography.
    *   [paper/archive/old_local_2022/](file:///y:/jpapers/siv/social-finance/paper/archive/old_local_2022/) — Contains retired/archived 2022 draft variants to prevent confusion.
*   [notebooks/](file:///y:/jpapers/siv/social-finance/notebooks/) — Active Jupyter Notebooks modeling the paper contracts (`2-socfin_m.ipynb` and `3-basicmodel.ipynb`).
*   [socialfinance/](file:///y:/jpapers/siv/social-finance/socialfinance/) — Source Python package containing core contract equations and plotting methods (`socialfinance.py`).
*   [log/](file:///y:/jpapers/siv/social-finance/log/) — Meeting logs and diaries (kept locally, ignored by GitHub).
*   [archive/](file:///y:/jpapers/siv/social-finance/archive/) — Miscellaneous historical research notes (kept locally, ignored by GitHub).
*   [data/](file:///y:/jpapers/siv/social-finance/data/) — Data files including global Findex microdata (kept locally, ignored by GitHub).

---

## Dual-Remote Git Workflow

This project is configured with two git remotes: `origin` (GitHub) and `overleaf` (Overleaf). This allows you to work locally and push your Python code and site assets to GitHub while syncing your LaTeX edits instantly to Overleaf.

```
                  ┌───────────────┐
                  │   Overleaf    │
                  │ (LaTeX Paper) │
                  └───────▲───────┘
                          │ git push/pull overleaf
                          │
                  ┌───────▼───────┐
                  │  Y:\ Workspace│
                  └───────▲───────┘
                          │
                          │ git push/pull origin
                  ┌───────▼───────┐
                  │    GitHub     │
                  │(Code & Website)
                  └───────────────┘
```

### 1. Synchronizing with Overleaf

Always pull any changes made on Overleaf before editing the paper text locally, and push back immediately after editing to compile in the Overleaf browser:

*   **Pull latest changes from Overleaf:**
    ```powershell
    git pull overleaf master
    ```
*   **Push local changes back to Overleaf:**
    ```powershell
    git push overleaf main:master
    ```

### 2. Synchronizing with GitHub

Commit and push your changes to GitHub to back up your codebase, notebooks, and trigger the MyST website build:

*   **Push local changes to GitHub:**
    ```powershell
    git push origin main
    ```

---

## Local Git Rules (.gitignore)

To keep the remote GitHub repository clean and lightweight, the following local folders are **explicitly ignored** on GitHub but remain safely preserved on your `Y:\` drive:
*   `archive/` (Historical PDF/Tex notes)
*   `log/` (Meeting diaries)
*   `data/Findex/` (Large Findex microdata files)
*   `socialfinance.egg-info/`, `build/`, `dist/` (Python package build outputs)

To clean up or ignore new local-only directories without losing files:
```powershell
git rm -r --cached folder_name/
```

---

## Auto-Deployment to GitHub Pages
Any commit pushed to GitHub on the `main` branch automatically triggers a GitHub Action to rebuild and host your MyST interactive book and compiled Marp slide decks on:
👉 **[https://jhconning.github.io/sfinance/](https://jhconning.github.io/sfinance/)**
