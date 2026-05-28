# Project Notes & Workflows

This document outlines the organization and development workflows for the **Social Finance** paper and codebase consolidation project.

---

## Workspace Structure

The project has been consolidated into a single definitive workspace located on the **Y drive** (to prevent sync conflicts with Google Drive / Dropbox):

*   **Repository Location (Code/Root):** `Y:\jpapers\siv\social-finance`
*   **Repository Location (Paper/Subfolder):** `Y:\jpapers\siv\social-finance\paper`

### Directory Layout

*   [paper/](file:///Y:/jpapers/siv/social-finance/paper/) — **Independent Git Repository** holding active LaTeX source files and bibliography. Pushes directly to Overleaf.
    *   `main.tex` — Active paper body (integrated from Overleaf 2026).
    *   `Notes2024.tex` — Active draft notes and sections written by Jonathan Morduch.
    *   `references.bib` — Active references bibliography.
    *   `changelog.md` — Date-time stamped paper log of changes marked with initials (e.g. "JC").
    *   [paper/archive/old_local_2022/](file:///Y:/jpapers/siv/social-finance/paper/archive/old_local_2022/) — Contains retired/archived 2022 draft variants.
*   [notebooks/](file:///Y:/jpapers/siv/social-finance/notebooks/) — Active Jupyter Notebooks modeling the paper contracts (`2-socfin_m.ipynb` and `3-basicmodel.ipynb`).
*   [socialfinance/](file:///Y:/jpapers/siv/social-finance/socialfinance/) — Source Python package containing core contract equations and plotting methods (`socialfinance.py`).
*   [log/](file:///Y:/jpapers/siv/social-finance/log/) — Meeting logs and diaries (kept locally, ignored by GitHub).
*   [archive/](file:///Y:/jpapers/siv/social-finance/archive/) — Miscellaneous historical research notes (kept locally, ignored by GitHub).
*   [data/](file:///Y:/jpapers/siv/social-finance/data/) — Data files including global Findex microdata (kept locally, ignored by GitHub).

---

## Dual-Remote Git Workspace Architecture

To keep Python development clean and LaTeX compilation seamless, the workspace uses a **nested independent Git repository model**. The paper is git-ignored by the parent repository, allowing both repositories to coexist in the same folder structure without history or credential pollution.

```
                   ┌────────────────┐
                   │    Overleaf    │
                   │ (LaTeX Paper)  │
                   └────────▲───────┘
                            │ cd paper; git push/pull origin
                            │
               ┌────────────▼────────────┐
               │ Y:\ Workspace           │
               │   ├── socialfinance/    │
               │   ├── notebooks/        │
               │   └── paper/ (.git)     │
               └────────────▲────────────┘
                            │
                            │ git push/pull origin
                   ┌────────▼────────┐
                   │     GitHub      │
                   │ (Code & Book)   │
                   └─────────────────┘
```

### 1. Synchronizing Paper Changes (Overleaf)

All LaTeX paper sync operations must be performed **inside the `paper/` subdirectory**.

*   **Pull latest co-author changes from Overleaf:**
    ```powershell
    cd Y:\jpapers\siv\social-finance\paper
    git pull origin master
    ```
*   **Push local paper updates & changelog to Overleaf:**
    ```powershell
    cd Y:\jpapers\siv\social-finance\paper
    git add .
    git commit -m "Describe your paper modifications"
    git push origin master
    ```

### 2. Synchronizing Code & Notebooks (GitHub)

All code and website sync operations must be performed **inside the root directory**.

*   **Push local code changes to GitHub:**
    ```powershell
    cd Y:\jpapers\siv\social-finance
    git add .
    git commit -m "Describe your code updates"
    git push origin main
    ```

---

## Local Git Rules & Ignore Hygiene

*   The parent repository ignores the `paper/` directory entirely via the root `.gitignore`. This ensures that your private research paper draft is **never accidentally pushed to GitHub**.
*   The nested `paper/` repository ignores local LaTeX compilation artifacts (`.aux`, `.log`, `.synctex.gz`) via `paper/.gitignore` to prevent polluting the Overleaf workspace.

---

## Auto-Deployment to GitHub Pages
Any commit pushed to GitHub on the `main` branch automatically triggers a GitHub Action to rebuild and host your MyST interactive book and compiled Marp slide decks on:
👉 **[https://jhconning.github.io/sfinance/](https://jhconning.github.io/sfinance/)**
