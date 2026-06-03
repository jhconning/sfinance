# Project Handoff: Social Finance Model & Parameter Synchronizations

This handoff document captures the current state, active context, key mathematical derivations, completed milestones, and immediate next steps for the **Social Finance** research project workspace. Use this file to resume the conversation seamlessly on another computer.

---

## 1. Active Workspace Context
*   **Workspace Directory:** `y:\jpapers\siv\social-finance` (Persistent virtual mapping to GDrive)
*   **Active Notebooks:**
    1.  [2-socfin_m.ipynb](file:///y:/jpapers/siv/social-finance/notebooks/2-socfin_m.ipynb) — Base Model, Crossover Kink, Subsidy Impact.
    2.  [5-endogenous-NK.ipynb](file:///y:/jpapers/siv/social-finance/notebooks/5-endogenous-NK.ipynb) — Endogenous Intermediary Capital ($K$) & Borrowers ($N$) with Heterogeneous Returns.
    3.  [4-selfish-equity.ipynb](file:///y:/jpapers/siv/social-finance/notebooks/4-selfish-equity.ipynb) — Commercial ROE hurdles, leverage rationing, and General Equilibrium capital market clearing solver.
*   **Active Library Module:** [socialfinance.py](file:///y:/jpapers/siv/social-finance/socialfinance/socialfinance.py)
*   **Active LaTeX Paper Draft:** [main.tex](file:///y:/jpapers/siv/social-finance/paper/main.tex)
*   **Obsidian Master Worklog:** [master_worklog.md](file:///Y:/B/notable/Main%20notes/gemini/master_worklog.md)

---

## 2. Completed Milestones in this Session

### A. Crossover Kink Parameter Sync ($\beta = 1.10$)
To make the first contract space diagram visually clearer and show the distinct "kink" (crossover point $m_{cross}$) between the equity-only and leveraged collateral boundaries:
1.  **Initialization:** The baseline `Bank` model in `2-socfin_m.ipynb` (Cell 7) now starts with `beta = 1.10 > gamma = 1.0`.
2.  **Cell 14 & 15 Mathematical Synchronization:** 
    *   Updated the code in **Cell 14** to print the true *equity-only* zero-monitoring collateral boundary `mfi.AMe(0)` (which now correctly prints `140.0` due to `beta = 1.1`), rather than `mfi.AM(0)` (which printed `130.0` using $\gamma=1.0$).
    *   Updated **Cell 15**'s markdown to: *"The bank is asking for \$140 security for a \$100 loan"* to match the mathematical output.
3.  **Cell 32 & 34 Parameter Sync:**
    *   To match your text *"Suppose $\beta = 1.2 \cdot \gamma$, then:"*, updated the code in **Cell 34** to set `mfi.beta = 1.2` (printing `Ame(0) = 150.0  Am(0) = 130.0`) and then immediately reset `mfi.beta = 1.0` right after.
    *   This keeps the rest of the first half evaluated under the standard Social Finance benchmark ($\beta = \gamma = 1.0$), ensuring that subsequent borrower returns and reach curves are consistent with Section 3's baseline.
4.  **Structural Pruning:** Removed redundant moral hazard explanations in Cell 10, consolidated duplicate groups tables, and cleaned up formatting.
5.  **KaTeX Patches:** Double-escaped all Jupyter-crashing single-escaped backslash sequences (e.g. `\right` to `\\right` in equations), ensuring that KaTeX parses and renders beautifully.

### B. Analytical Formulations (WACC & Fixed Cost Pricing)
1.  **Borrower-Specific WACC:** Derived and implemented the endogenous Weighted Average Cost of Capital per borrower:
    $$WACC_i = \gamma + (\beta - \gamma) w_e^i, \quad \text{where } w_e^i = \frac{I^m}{I + F}$$
2.  **Fixed Cost Financing Nuance:** Proved analytically that under monitor incentive compatibility, tangible fixed costs ($F$) are priced at the debt rate ($+ \gamma F$), preserving simulation tractability. Conversely, sunk operational costs in debt-starved poor neighborhoods scale with the equity premium ($+ \beta F$), creating MFI entry barriers.

### C. Endogenous $N$ & $K$ Model Extension (`5-endogenous-NK.ipynb`)
1.  **Model Mechanics:** Implemented within-neighborhood project return heterogeneity $X_s \sim \text{Uniform}[\underline{X}, \bar{X}]$ to make borrower credit demand downward-sloping. Created a new `BankHetX` class in `socialfinance.py` to analytically solve:
    *   Optimal monitoring $m^*(A_j, X_s)$ and marginal return cutoff $X_s^*(A_j, \beta)$.
    *   Vectorized capital demand per neighborhood: $K_j(\beta) = N \cdot \left[ I^m \cdot \text{fraction\_served} + F \right]$.
2.  **General Equilibrium:** Implemented a general equilibrium solver that clears the capital market for MFI monitoring equity $\beta^*$ across capital supplies ($K_{total}$), demonstrating how "mission drift" occurs both via cream-skimming high returns within neighborhoods and the total exclusion of poorer neighborhoods.

---

## 3. Current Numerical Parameters & Reference Outputs
For the baseline zone (`beta = 1.1`, `gamma = 1.0`, `f = 30`, `I = 100`, `X = 200`, `p = 0.97`, `q = 0.82`, `alpha = 0.5`):
*   **Equity-only zero-monitoring collateral $A^e(0)$:** `140.0`
*   **Leveraged zero-monitoring collateral $A(0)$:** `130.0`
*   **Crossover monitoring intensity $m_{cross}$:** `20.122`
*   **Crossover collateral boundary $A(m_{cross})$:** `95.061`
*   **Max feasible monitoring $m_{max}$:** `54.0`
*   **Lowest feasible collateral limit $A_{min}$:** `19.4`

---

## 4. Immediate Next Steps for the Next Session

1.  **Sync Findings into `paper/main.tex`:**
    *   Incorporate the borrower-specific WACC equation and the operational fixed cost pricing narrative ($+ \gamma F$ vs. $+ \beta F$) into the paper draft.
    *   Use the new `figs/fig-Am.png` showing the explicit `beta = 1.1` crossover kink in place of the older flat-intersection figure.
2.  **Refine the Handoff between Notebooks:**
    *   Validate that any subsequent slides or briefings reference the updated collateral levels (\$140 for equity-only zero-monitoring, \$130 for leveraged zero-monitoring, and the \$95 crossover).
3.  **Validate General Equilibrium Comparative Statics:**
    *   Explore how changing the width of the project return distribution ($\bar{X} - \underline{X}$) impacts general equilibrium return on equity $\beta^*$ and the total number of borrowers reached.
