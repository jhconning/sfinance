# Project Handoff: Social Finance Paper & Code Synchronization

This document serves as a complete handoff guide to initialize your next conversation, designed to help a new agent immediately grasp the consolidated structure, files, and workflows of the **Social Finance** project.

---

## 1. Project Background
*   **Goal:** Revisit, deeply revise, and synchronize a long-standing academic paper tentatively titled *"Social Finance"* (written by Jonathan Conning at Hunter College/CUNY and Jonathan Morduch at NYU) with its active Python simulation notebooks.
*   **Core Economic Focus:** Applied micro-theory contracts modeling the funding structures of microfinance institutions (MFIs), comparing equity-only/unleveraged MFIs vs. leveraged MFIs under moral hazard, and examining the role of "smart subsidies" and social investors in expanding scale and output.

---

## 2. Definitive Workspace Architecture
The project has been consolidated from multiple historic directories (including Dropbox) into a single, definitive, git-tracked workspace located on the user's **Y drive** to prevent path issues and sync conflicts:

📁 **Local Workspace Directory:** `Y:\jpapers\siv\social-finance`

### Unified Directory Layout
*   [socialfinance/](file:///Y:/jpapers/siv/social-finance/socialfinance/) — **Core Code Package**
    *   `socialfinance.py` — Contains the core contract equations, parameters, borrower return profiles, and plotting classes (`class Bank(object)`).
*   [notebooks/](file:///Y:/jpapers/siv/social-finance/notebooks/) — **Active Jupyter Notebooks**
    *   `2-socfin_m.ipynb` — The primary modeling and simulation notebook (updated Jan 22, 2026).
    *   `3-basicmodel.ipynb` — Secondary active modeling notebook.
    *   `1-results.md` — Active modeling analysis outputs.
    *   *Archive folder:* Loose duplicates, old slide files, and exports have been neatly cleared out and retired to `notebooks/archive/` to keep this root pristine.
*   [paper/](file:///Y:/jpapers/siv/social-finance/paper/) — **Active LaTeX Paper Source** (Local & Overleaf Sync Only)
    *   `main.tex` — Core modernized LaTeX paper body (dated Jan 2026).
    *   `Notes2024.tex` — Active draft notes and newer sections contributed by co-author Jonathan Morduch (dated Jan 22, 2026).
    *   `references.bib` — Active references bibliography.
    *   *Archive folder:* Pre-2022 loose drafts, Word files, and loose image files have been safely isolated in `paper/archive/` to avoid confusion.
*   [log/](file:///Y:/jpapers/siv/social-finance/log/) — Meeting logs and diaries (kept local-only).
*   [data/](file:///Y:/jpapers/siv/social-finance/data/) — Data folders including World Bank Findex datasets (kept local-only).

---

## 3. High-Efficiency Dual-Remote Workflow
To keep development frictionless, the local repository connects to **two independent git remotes**.

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

### Remote 1: GitHub (`origin`)
Used exclusively for tracking python code, Jupyter notebooks, slide decks, and configuration files. 
*   **Remote URL:** `https://github.com/jhconning/sfinance.git`
*   **Gitignore Hygiene:** The `paper/` directory, `log/` folder, and large `data/` files are explicitly git-ignored on the `origin` remote to keep the repository extremely lightweight and clean.
*   **Push Command:**
    ```powershell
    git pull origin main
    git push origin main
    ```

### Remote 2: Overleaf (`overleaf`)
Used exclusively for tracking LaTeX paper source files, sharing text changes cleanly with your co-author Jonathan Morduch.
*   **Remote URL:** `https://git@git.overleaf.com/62167876d91ea90954bfaf60`
*   **Credentials:** Authenticated securely via **Overleaf Git Token** (entered in place of standard password and cached securely in the Windows Credential Manager).
*   **Gitignore Hygiene:** Local build auxiliary files (`.aux`, `.log`, `.synctex.gz`) are git-ignored locally via `paper/.gitignore` to prevent polluting the Overleaf workspace.
*   **Push & Pull Commands:**
    ```powershell
    # Pull co-author's edits from Overleaf master branch:
    git pull overleaf master

    # Push your local main branch changes directly to Overleaf compiler:
    git push overleaf main:master
    ```

---

## 4. Website and Slide Auto-Deployment
Pushes targeting GitHub's `main` branch trigger a custom GitHub Action workflow ([.github/workflows/deploy.yml](file:///Y:/jpapers/siv/social-finance/.github/workflows/deploy.yml)):
1.  Compiles the interactive notebooks into a MyST Markdown book.
2.  Bypasses Jekyll processing via `.nojekyll` configuration.
3.  Runs Marp CLI to compile slide presentations to PDF.
4.  Deploys the static site to GitHub Pages:
    👉 **[https://jhconning.github.io/sfinance/](https://jhconning.github.io/sfinance/)**

---

## 5. Next Steps for the Next Conversation
Provide these exact starting cues to the incoming agent in the new thread:
1.  **Inspect Active Notebooks:** Open and run `Y:\jpapers\siv\social-finance\notebooks\2-socfin_m.ipynb` using the local Jupyter kernel to verify equation outputs.
2.  **Compare Paper & Code:** Read the model definitions in the LaTeX source (`Y:\jpapers\siv\social-finance\paper\main.tex`) and cross-reference them with the classes/methods defined inside the core package (`Y:\jpapers\siv\social-finance\socialfinance\socialfinance.py`).
3.  **Draft Revision Plan:** Integrate Jonathan Morduch's newer text inside `Notes2024.tex` directly into the paper's core general equilibrium equations.
