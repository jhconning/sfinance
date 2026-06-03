# Project Handoff: Syncing Capital Adequacy & Leverage across Notebooks

This document serves as a focused handoff guide to initialize a new conversation thread, designed to help an incoming agent immediately grasp the mathematical logic, recent notebook changes, and the exact next steps for this project.

---

## 1. Project Background & Mathematical Logic
The goal of this project is to model and simulate microfinance lending contracts under moral hazard and scarce capital. 
*   **The core dilemma:** Lenders must monitor borrowers to reduce private benefit from non-diligence. Richer borrowers (higher assets $A$) need less monitoring ($m$), whereas poorer borrowers need heavy monitoring.
*   **The funding constraint:** Monitoring is only credible if the MFI puts up a sufficient equity stake $I^m(A)$ to maintain skin-in-the-game. Richer borrowers require less monitoring, allowing the MFI to hold less equity ($I^m < I$) and leverage cheaper outside debt. Poorer borrowers require so much monitoring that the MFI must fund them using 100% equity ($I^m = I$).
*   **Regulatory Capital Adequacy Ratio (CAR):** To prevent leverage (outside debt to equity) from rising to infinity as monitoring drops to zero for very wealthy borrowers, we introduce a regulatory constraint:
    $$I^m(A) = \max \left( k \cdot (I + f), \frac{q \cdot m(A)}{\beta \Delta} \right)$$
    where $k = 0.10$ (10% CAR requirement). This strictly caps the maximum leverage ratio at:
    $$\text{Max D/E} = \frac{1-k}{k} = 9.0$$

---

## 2. Active Workspace Directory
📁 **Local Workspace Directory:** `Y:\jpapers\siv\social-finance`

*   [socialfinance/](file:///Y:/jpapers/siv/social-finance/socialfinance/) — **Core Python Package**
    *   `socialfinance.py` — Contains the `Bank` class holding contract equations, parameters, and plotting methods.
*   [notebooks/](file:///Y:/jpapers/siv/social-finance/notebooks/) — **Active Jupyter Notebooks**
    *   `2-socfin_m.ipynb` — The primary modeling and simulation notebook (fully cleaned, debugged, and synced).
    *   `4-selfish-equity.ipynb` — Market-clearing equilibrium solver and interactive dashboard.
    *   `5-endogenous-NK.ipynb` — Endogenous scale and funding structures.

---

## 3. Latest Accomplishments in Notebook 2
We completed a series of deep modeling updates and code cleanups in [2-socfin_m.ipynb](file:///Y:/jpapers/siv/social-finance/notebooks/2-socfin_m.ipynb):
1.  **Baseline MFI ROE:** Configured the baseline MFI return on equity to exactly `beta = 1.2` (Cell 7).
2.  **Regulatory CAR 10% Integration:**
    *   Updated the `Im(self, m)` method in `socialfinance.py` to enforce the 10% CAR floor on total assets funded ($I+f = 130$), successfully capping leverage at exactly `9.0`.
    *   Added a horizontal dashed limit line at `9.0` in both D/E ratio plots (Cell 39 and Cell 68) and set the $y$-axis limit to $1.25 \times 9.0 = 11.25$ to give it clean visual headroom.
3.  **Threshold Visualizations:**
    *   Enriched `plotDE(self, beta)` to draw three distinct dotted vertical lines in the interior of the chart for the critical model boundaries: Exclusion limit ($A_{min}$), Leverage crossover ($A_{cross}$), and Direct credit limit ($A^m(0)$).
    *   Shifted the $x$-axis start limit to `amin - 15` so that $A_{min}$ is beautifully visible in the interior rather than being cut off on the border.
4.  **Parameter Discrepancy Resolved (f vs F):**
    *   Synced all leverage and D/E equations to consistently use the loan-level administrative fixed cost `self.f = 30` instead of the neighborhood-level setup cost `self.F = 0`.
5.  **Exhaustive Math Validation:**
    *   Confirmed that the analytical equations for $m(A)$ and $m^e(A)$ are mathematically exact and fully compatible with $f > 0$; removed the `[CHECK THIS]` tag from the notebook.
6.  **Pristine Restructuring:**
    *   Relocated the credit capacity outreach $N(A)$ and borrower return landscape plots from notebook 4 into notebook 2 (before the subsidy section), providing detailed explanatory text about MFI capital capacity.

---

## 4. Next Task: Carrying the CAR to Notebook 4
Our next immediate task is to explore and improve [4-selfish-equity.ipynb](file:///Y:/jpapers/siv/social-finance/notebooks/4-selfish-equity.ipynb) to carry over the 10% CAR logic there:
1.  **Market-Clearing Equilibrium Solver:**
    *   Verify that `get_Im_vectorized(bank, A_array)` inside notebook 4 incorporates the `bank.CAR` constraint dynamically.
    *   Ensure that the global market-clearing equilibrium ROE $\beta^*$ is solved respecting the 10% capital adequacy constraint.
2.  **Interactive Capital Market Dashboard:**
    *   Verify and ensure that the interactive widget slider for `alpha` (monitoring effectiveness) and capital supply recalculates and Clears the Market under the 10% CAR floor, updating the demand-clearing diagram and contract envelopes accordingly.
3.  **Visual Consistency:**
    *   Ensure that all plots and sliders carry over the exact same parameter syncs ($f=30$, baseline beta=1.2) established in notebook 2.
