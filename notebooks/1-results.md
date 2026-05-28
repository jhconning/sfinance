---
title: "Summary"
subtitle: Social Finance summary and results
exports:
  - format: pdf
    template: springer
    output: exports/results.pdf
abstract: |
  A summary of main results of the paper.
---


## Framing

- Builds on models of financial intermediation and active monitoring including @holmstrom1997, @conning1999 and @tirole2006
- Simplifying assumptions and stylized model highlight key mechanisms.
- Extend framework to unexplored areas of social finance.

## Model

If lump sum $I$ is invested the project can be undertaken.  The project will produce $X_s$ if it succeeds and $X_f$ if it fails. 

The probability of success depends on borrower diligence.  If the borrower is diligent, the project succeeds with probability $p$. If the borrower is non-diligent, the project succeeds with probability $q<p$, but the borrower captures a private benefit $B(0)$.

A contract divides expected returns $(X_f, X_s)$ between returns to the borrower $(s_f, s_s)$ and returns to the lender $(X_f-s_f, X_s-s_s)$.


### Incentive Compatibility (IC)

- The borrower must expect to earn more from being diligent (probability of success $p$) than from being non-diligent (probability of success $q<p$)

$$
p \cdot s_s + (1-p) \cdot s_f \ge p \cdot s_s + (1-p) \cdot s_f + B(0)
$$

Re-arranging:

$$
s_s \ge s_f + \frac{B(0)}{p-q}
$$

- Practical implication: payout when project is successful $S_s$ must exceed payout when project fails $S_f$ by enough to make borrower indifferent between making effort and not making effort.

### Limited liability (LL)

$$
s_f \ge -A
$$

Where $A$ is available pledgeable assets. With IC and LL both binding, this implies that in expectation the borrower must earn a **minimum economic rent** of:

$$
E(s|p)= -A + \frac{pB(0)}{p-q}
$$

When the borrower is diligent the project succeeds with probability $p$ and generates expected returns $E(X|p)$ but these returns must cover:
 - $\gamma I$, lender cost of funds
 - $f$ loan fixed costs
 - $E(s|p)$ the borrower's minimum economic rent 

**Credit rationing** (exclusion) occurs when 

$$
E(S|p) < E(x|p) - \gamma I - f 
$$

**Pledgeable assets** or **collateral* $A$ provides a way for the borrower to commit to reduce the size of the economic rent that borrower must capture for incentives.

### Participation constraints

If we assume **competition** amongst lenders, banks will participate if they can break even (zero profit participation constraint).

Depending on whether the project fails or succeeds, the lender captures:

$$
\begin{aligned}
X_f& - \gamma I - f + A \\
X_s& - \gamma I - f + A - \frac{B(0)}{p-q}
\end{aligned}
$$

To participate the bank must expect to cover costs and earn at least zero profit:

$$
E[X|p] - \gamma I - f + A - \frac{pB(0)}{p-q} \ge 0
$$


### Minimum collateral requirement (zero monitoring)

We can derive the minimum collateral requirement as the level of $A$ that makes the bank just indifferent between participating or not:

$$
\underline A(0) = \frac{p \cdot B(0)}{p-q} 
 - \left[ {pX - \gamma I -  F} \right]
$$

#### Imperfect collateral (an aside)

We could think of collateral as own money that borrower is willing to put up.  Hence the borrower puts up $A$ in funds and the bank the difference $I-A$. But we'll stick to the interpretation of $A$ as a pledgeable asset that is (in effect) only seized in the event of default (e.g. equipment or property).  

As an aside, it's possible that the bank can only seize $\tau A$ of the value of the assets $A$ in the event of default, but the borrower suffers loss $A$.  This would be the case, for example, if the item seized is more valuable to the borrower than to the bank (e.g. a street cart), for example if there are transaction costs to the bank in seizing and re-selling the item.

The $IC$ constraint is as before, but the minimum collateral requirement is now:

$$
\underline A^{\tau}(0) =\frac{1}{\tau} \cdot \underline A(0)
$$

Though not analyzed below, this suggests another potential interesting avenue for how social investor subsidy might have multiplicative effects, because while each dollar of collateral from the borrower is worth only $\tau A$ to the lender, each dollar of subsidy/guarantee is valued dollar for dollar.


## Collateral and Monitoring

Suppose active monitoring $m$ on the part of the lender (or, shortly, an intermediary) can reduce the scope for moral hazard by directly reducing the borrower's private benefit $B(m)$.  We assume a very simple linear form to this monitoring:

$$
B(m) = B(0) - \alpha \cdot m
$$

We will assume monitoring can only be done by local lenders, who know the neighborhood. Their cost of funds is potentially higher, because local intermediary capital may be scarce. We assume that if the local intermediary invests $I$ the cost of funds is $\gamma I$ where $\beta \ge \gamma$. We take $\gamma$ as given now, but later determine it as an equilibrium quantity.

The minimum collateral requirement for the local monitoring (equity only) lender:

$$
\underline A^e(m) = \frac{p \cdot B(m)}{p-q} 
 - \left[ {pX - \gamma I -  F} \right] + m
 $$

Monitoring adds to the costs that must be covered out of expected returns, so it is only worthwhile in expanding access if it lowerş the limited liability rent faster than it expands costs.

This will be the case if it lowers the minimum collateral requirement, which happens when $\frac{d \underline A(m)}{dm}<0$ or $\alpha \gt \frac{p-q}{p}$.  

We also must make sure that

$$E[X|p] - \beta I - f - m \gt 0$$

Which determines a maximum feasible level of monitoring.

Let's assume this is the case. In the diagram below $p = 0.97$, $q = 0.82$ and $\alpha = 0.5$.

In the figure below $\underline A^e(m)$ is the minimum collateral requirement for the local monitoring lender.  

:::{figure} #fig-A
:label: figA
:remove-input: true
:remove-output: false
Monitoring expands access.
:::

### Intermediated lending



:::{figure} #fig-rmonitoring
:label: figrmonitor
:remove-input: true
:remove-output: false
Monitoring expands access.
:::



:::{figure} #fig-brcompare
:label: fig-brcompare
:remove-input: true
:remove-output: false
Monitoring expands access.
:::


:::{figure} #fig-brdiff
:label: fig-brdiff
:remove-input: true
:remove-output: false
Monitoring expands access.
:::
