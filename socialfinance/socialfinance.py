# socialfinance.py  -- module for modeling contracts and bank funding structures

import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Markdown, display, Math
from scipy.integrate import quad
from scipy.optimize import root_scalar, brentq




class Bank(object):
    ''' A Bank in a 'neighborhood' or 'zone'  where the representative 
        borrower has pledgeable assets A.  The bank will have (derived) 
        attributes including the terms of contract, monitoring intensity, 
        and its own funding structure.
    '''

    def __init__(self, A, beta, **kwargs): 
        self.A = A         # pledgeable assets (as array)
        self.gamma = 1.0   # cost of uninformed capital (1 + ru)
        self.beta = beta   # cost of equity capital (1 + re)
        self.B0 = 30       # itercept monitoring intensity function
        self.alpha = 0.5   # slope monitoring intensity function
        self.X = 200       # project success return
        self.I = 100       # lump-sum investment
        self.p = 0.97      # prob. of success if diligent
        self.q = 0.82      # prob. of success if not-diligent
        self.F = 0         # Fixed cost per neighborhood
        self.f = 20        # Fixed cost per loan
        self.K = 10000     # Intermediary capital in each neighborhood.
        #self.M = self.minmon(A)
        self.Amax = 140    # used for plot limits

        # Override attributes using kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def B(self, m):
        '''Monitoring intensity function: B(m) is the private benefit borrower 
        could capture via non-diligence'''
        return self.B0 - self.alpha * m
    
    def FC(self, N):  # Avg fixed cost per borrower if bank has N borrowers
        return self.F / N + self.f

    def AMe(self, m): 
        '''Minimum collateral for non-leveraged or equity-only MFI '''
        p, q, I, X, beta,f = self.p, self.q, self.I, self.X, self.beta, self.f    
        return (p/(p-q)) * self.B(m)  - (p * X - beta * I) + m + beta * f

    def AM(self, m):
        '''Minimum collateral for leveraged MFI '''
        p, q, I, X, gam, beta, f= self.p, self.q, self.I, self.X, self.gamma, self.beta, self.f  
   
        return (p/(p-q)) * self.B(m) - (p * X - gam * I) + m  \
                  + ((beta - gam) / beta) * (q * m / (p - q)) + beta * f

    def Abest(self, m):
        '''Lower of the two collateral requirements'''
        return np.minimum(self.AMe(m), self.AM(m))

    def Im(self, m):
        '''Minimum required equity investment by monitor'''
        incentive_equity = (1/self.beta) * self.q * m / (self.p - self.q)
        raw_eq = np.maximum(0.0, incentive_equity)
        return np.minimum(self.I, raw_eq)

    def mcross(self):
        '''Monitoring level where equity only AMe and levered AM lines cross'''
        return self.beta * self.I * (self.p - self.q) / self.q

    def Across(self):
        return self.AM(self.mcross())

    def mmax(self):
        '''Maximal monitoring at which equity-only monitor can just break even'''
        return self.p * self.X - self.beta * (self.I + self.f)

    def Amin(self):
        '''Lowest possible collateral requirement - at max feasible monitoring'''
        return self.AMe(self.mmax())

    def mon(self, A):
        '''optimal monitoring in leveraged MFI
           Zero if >A(0)'''
        AHI = self.AM(0) 
        return ( (AHI - A) * (self.beta * (self.p - self.q)) / 
                 ((self.alpha - 1) * self.beta * self.p + self.gamma * self.q)   )

    def monE(self, A):
        '''optimal monitoring in equity-only MFI'''
        AHI = self.AMe(0)
        return ( (AHI - A) * 
                ((self.p - self.q) / (self.q + (self.alpha-1) * self.p))   )

    def minmon(self, A):
        return np.minimum(self.monE(A), self.mon(A))

    def breturn(self, A):
        ''' array of borrower returns by A'''
        X, p, q, I, f, gam, beta = self.X, self.p, self.q, self.I, self.f, self.gamma, self.beta

        br = []
        for a in A:
            if a > self.AM(0):
                br.append(p * X - gam * I - beta * f)
            elif (a <= self.AM(0)) and (a > self.Across()):
                m = self.mon(a)
                Im = self.Im(m)
                repayment = gam * (I - Im) + beta * (Im + f) + m
                br.append(p * X - repayment)
            elif (a <= self.Across()) and (a >= self.Amin()):
                br.append(p * X - beta * (I + f) - self.monE(a))
            else:
                br.append(0)
        return np.array(br)


    def print_params(self):
        """
        Display scalar parameters alphabetically
        """
        params = sorted(vars(self).items())
        params_to_print = [f"{key} = {value}" for key, value in params if np.isscalar(value)]
        for i in range(0, len(params_to_print), 6):
            print(', '.join(params_to_print[i:i+6]))

    

    def nreach(self,A):
        '''number of borrowers reached with K of intermediary capital at different A'''
        K, I, f = self.K, self.I, self.f

        nr = np.zeros(len(A)) 
        for i, a in enumerate(A):
            if a > self.AM(0):
                nr[i] = np.nan
            elif (a <= self.AM(0)) and (a > self.Across()):
                nr[i] = K / (self.Im(self.mon(a)) + f)
            elif (a <= self.Across()) and (a >= self.Amin()):
                nr[i] = K / (I + f)
            else:
                nr[i] = 0
        return nr
    
    def plotA(self):
        '''Plot minimum collateral requirements'''
        mc, mx = self.mcross(), self.mmax()
        Am0, Amc, Amx = self.AM(0), self.AM(mc), self.AMe(mx)
        mm, mm_ = np.linspace(0, self.Amax), np.linspace(0, mx)
        
        fig, ax = plt.subplots(1)
        ax.plot(mm, self.AMe(mm), label='equity only MFI', linestyle=':')
        ax.plot(mm, self.AM(mm), label='leveraged MFI', linestyle=':')
        ax.plot(mm_, self.Abest(mm_), linewidth=3.3) 
        
        ax.set(xlim=(0, 80), ylim=(0, self.AMe(0)), 
               title='Minimum Collateral requirement', 
               xlabel='monitoring intensity $m$', ylabel='pledgeable asset $A (m)$')
        
        ax.text(1, Am0+5, 'No monitor', rotation='vertical', verticalalignment='bottom')
        ax.text(1, (Amc+Am0)/2, 'Interme-\n diated', rotation='vertical', verticalalignment='center')
        ax.text(1, (Amx+Amc)/2, 'Equity-only', rotation='vertical', verticalalignment='center')
        ax.text(1, Amx/2, 'No Loan', rotation='vertical', verticalalignment='center')
        ax.text(mx*1.1, self.AMe(mx)*0.9, r'$A^e(m)$')
        ax.text(mx*1.1, self.AM(mx), r'$A(m)$')
        
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        ax.vlines([mc, mx], ymin=0, ymax=[Amc, Amx], linestyle =':')
        ax.hlines([Amc, Amx], xmin=0, xmax=[mc, mx], linestyle =':')
        
        ax.legend(loc='upper right')
        ax.set_ylim(0, self.AMe(0)+20)
    
    def plotIm(self):
        '''
        plot total investment share by intermediary and uninformed lenders'''
        I, f, beta = self.I, self.f, self.beta
        mc, mx = self.mcross(), self.mmax()
        Amc, Amx = self.AM(mc), self.Amax

        amin = self.Amin()
        A_ = np.linspace(amin, Amx, 100)  # color only loans
        m_vals = np.maximum(0, self.minmon(A_))
        Im = np.array([self.Im(m) for m in m_vals])
        Iu = I - Im

        fig, ax = plt.subplots()
        ax.plot(A_, Im, label=r'$I^m$ - monitoring equity')
        ax.plot(A_, Iu, label=r'$I^u$ - uninformed debt')
        ax.plot(A_, m_vals, label=r'$m$ - monitoring')

        ax.set_title(r'Required monitoring m and investment $I^m$')
        ax.set_xlabel('A -- pledgeable assets')
        ax.set_ylim(0, I + 10)
        ax.set_xlim(amin-10, max(A_))

        ax.text(amin - 5, I, r'$I$')
        ax.text(amin + 2, I - 5, r'$I^m$')
        ax.text(amin + 2, self.monE(amin), 'm(A)')
        ax.text(amin + 2, 2, r'$I^u =I-I^m$')

        ax.axvline(x=amin, linestyle=':')
        ax.axvline(x=Amc, linestyle=':')
        ax.axvline(x=self.AM(0), linestyle=':')
        ax.axhline(y=I, linestyle=':')


    def plotDE(self,beta):
        '''plot outside debt to MFI equity (I-Im)/(Im+f) ratio as a function of A'''
        amin = self.Amin()
        A_ = np.linspace(amin, self.AM(0), 100)[:-1]  # remove Im=0 point
        p,q, I, f = self.p, self.q, self.I, self.f
        plt.title('Debt to equity ratio:  ' + r'$\frac{I-I^m}{I^m+f}$')
        
        m_vals = self.minmon(A_)
        Im = np.zeros_like(A_)
        for idx, a_val in enumerate(A_):
            Im[idx] = self.Im(m_vals[idx])
            
        de = np.divide(I - Im, Im + f, out=np.zeros_like(Im), where=(Im+f)>0)
        plt.plot(A_, de)
        plt.xlabel('A -- pledgeable assets')
        
        # Enrich vertical lines to show all 3 thresholds clearly
        plt.axvline(x=self.Amin(), color='grey', linestyle=':', alpha=0.7, label=r'Exclusion limit $A_{min}$')
        plt.axvline(x=self.AM(self.mcross()), color='blue', linestyle=':', alpha=0.7, label=r'Leverage crossover $A_{cross}$')
        plt.axvline(x=self.AM(0), color='green', linestyle=':', alpha=0.7, label=r'Direct credit limit $A^m(0)$')
        
        plt.axhline(y=0, linestyle=':');
        
        max_de = I / f
        plt.axhline(y=max_de, color='red', linestyle='--', alpha=0.7, 
                    label=f'Max Leverage ({max_de:.1f})')
            
        plt.legend(loc='upper left', fontsize=9)
        y_max = max_de * 1.25
            
        plt.xlim(amin - 15, 140);
        plt.ylim(0, y_max);

    def get_Im_vectorized(self, A_array):
        """
        Computes the MFI's required total equity stake Im + f for a vectorized array of asset levels A.
        Handles all piecewise credit regimes (Excluded, Equity-Only, Leveraged, Unmonitored).
        """
        m_lev = self.mon(A_array)
        Im_lev = self.Im(m_lev) + self.f
        
        # Piecewise conditions matching model limits
        conds = [
            A_array < self.Amin(),    # Excluded
            A_array > self.AM(0),     # Unmonitored commercial lending
            A_array <= self.Across()  # Equity-only MFI lending
        ]
        choices = [
            0.0,
            0.0,
            self.I + self.f  # Enforces MFI funding 100% of loan + fixed operational cost
        ]
        return np.select(conds, choices, default=Im_lev)

    def capital_demand_grid(self, A_grid, N_potential=20.0):
        """
        Aggregates the total demand for MFI monitoring capital across the wealth distribution.
        """
        Im_vals = self.get_Im_vectorized(A_grid)
        return np.sum(N_potential * Im_vals)

    @classmethod
    def solve_equilibrium(cls, A_grid, K_total, N_potential=20.0, bracket=[1.0, 3.0], **kwargs):
        """
        Solves for the market-clearing equilibrium return on equity beta* 
        that clears the capital market for MFI monitoring equity.
        """
        def eq_solve(beta):
            inst_kwargs = kwargs.copy()
            if cls == BankHetX and 'N_pop' not in inst_kwargs:
                inst_kwargs['N_pop'] = N_potential
            tb = cls(A_grid, beta=beta, **inst_kwargs)
            return tb.capital_demand_grid(A_grid, N_potential=N_potential) - K_total
            
        try:
            sol = root_scalar(eq_solve, bracket=bracket)
            return sol.root
        except ValueError:
            raise ValueError("Market collapsed: Intermediary capital demand cannot match supply in this range.")


class BankHetX(Bank):
    """
    Extends Bank to allow heterogeneous project returns X_s
    within each neighborhood. Supports Uniform and Pareto distributions.
    """

    def __init__(self, A, beta, dist_type='uniform', X_lo=160, X_hi=240, 
                 X_m=160, alpha_pareto=3.0, N_pop=100, **kwargs):
        super().__init__(A, beta, **kwargs)
        self.dist_type = dist_type
        self.X_lo = X_lo
        self.X_hi = X_hi
        self.X_m = X_m
        self.alpha_pareto = alpha_pareto
        self.N_pop = N_pop
        self.F = 0              # Fixed cost per neighborhood (kept for compatibility)
        
        # Adjust bounds based on distribution
        if self.dist_type == 'pareto':
            self.X_lo = self.X_m
            self.X_hi = np.inf

    def pdf_Xs(self, x):
        """Probability density function of project returns X_s."""
        if self.dist_type == 'uniform':
            if x < self.X_lo or x > self.X_hi:
                return 0.0
            return 1.0 / (self.X_hi - self.X_lo)
        elif self.dist_type == 'pareto':
            if x < self.X_m:
                return 0.0
            return self.alpha_pareto * (self.X_m ** self.alpha_pareto) / (x ** (self.alpha_pareto + 1))
        else:
            raise ValueError(f"Unknown distribution type: {self.dist_type}")

    # ---- Core Methods for Heterogeneous X_s ----

    def AM0_Xs(self, X_s):
        """Zero-monitoring collateral requirement for project return X_s.
        A_bar(0, X_s) = p*B0/Delta - [p*X_s - gamma*I] + f
        """
        p, q, gam, B0, f = self.p, self.q, self.gamma, self.B0, self.f
        Delta = p - q
        return p * B0 / Delta - (p * X_s - gam * self.I) + f

    def m_opt_Xs(self, A_j, X_s):
        """Optimal monitoring for a leveraged MFI serving borrower (A_j, X_s).
        Returns 0 if A_j >= A_bar(0, X_s), i.e. no monitoring needed.
        """
        p, q, gam, beta, alpha = self.p, self.q, self.gamma, self.beta, self.alpha
        AM0 = self.AM0_Xs(X_s)
        gap = AM0 - A_j
        if np.isscalar(gap):
            if gap <= 0:
                return 0.0
        else:
            gap = np.maximum(gap, 0.0)
        denom = (alpha - 1) * beta * p + gam * q
        return gap * beta * (p - q) / denom

    def Im_Xs(self, m):
        """MFI equity stake per loan given monitoring level m.
        I^m = (1/beta) * q*m / Delta
        """
        return (1.0 / self.beta) * self.q * m / (self.p - self.q)

    def borrower_surplus_Xs(self, A_j, X_s):
        """Net expected surplus to a borrower (A_j, X_s) under leveraged lending.
        """
        p, q, gam, beta, f = self.p, self.q, self.gamma, self.beta, self.f
        Delta = p - q
        m = self.m_opt_Xs(A_j, X_s)
        m_cost_factor = 1.0 + (beta - gam) / beta * q / Delta
        surplus = p * X_s - gam * self.I - m * m_cost_factor - f
        if np.isscalar(surplus):
            return max(surplus, 0.0) if m >= 0 else 0.0
        else:
            return np.where(m >= 0, np.maximum(surplus, 0.0), 0.0)

    def X_star(self, A_j):
        """Marginal project return cutoff: minimum X_s to be profitably served.
        Solves borrower_surplus(A_j, X_s) = 0 for X_s.
        """
        p, q, gam, beta, alpha, B0, I, f = (self.p, self.q, self.gamma,
            self.beta, self.alpha, self.B0, self.I, self.f)
        Delta = p - q
        
        D = (alpha - 1) * beta * p + gam * q
        c = beta * Delta / D
        cost_m = 1.0 + (beta - gam) / beta * q / Delta
        
        numerator = gam * I + f + c * cost_m * (p * B0 / Delta + gam * I + f - A_j)
        denominator = p * (1.0 + c * cost_m)
        
        X_star_val = numerator / denominator
        lo_bound = self.X_m if self.dist_type == 'pareto' else self.X_lo
        hi_bound = np.inf if self.dist_type == 'pareto' else self.X_hi
        return np.clip(X_star_val, lo_bound, hi_bound)

    def X_no_monitoring(self, A_j):
        """Project return above which no monitoring is needed (m*=0)."""
        p, q, gam, B0, I, f = self.p, self.q, self.gamma, self.B0, self.I, self.f
        Delta = p - q
        return (p * B0 / Delta + gam * I + f - A_j) / p

    def frac_served(self, A_j):
        """Fraction of neighborhood population served (between 0 and 1)."""
        xs = self.X_star(A_j)
        if self.dist_type == 'uniform':
            if xs >= self.X_hi:
                return 0.0
            return (self.X_hi - xs) / (self.X_hi - self.X_lo)
        elif self.dist_type == 'pareto':
            return (self.X_m / xs) ** self.alpha_pareto
        return 0.0

    def N_served(self, A_j):
        """Number of borrowers served in neighborhood A_j."""
        return self.N_pop * self.frac_served(A_j)

    def K_demand_nbhd_numerical(self, A_j):
        """Total MFI equity capital demanded in neighborhood A_j via numerical integration."""
        xs = self.X_star(A_j)
        X_no_mon = self.X_no_monitoring(A_j)
        X_mon_upper = min(X_no_mon, self.X_hi)
        
        result_mon = 0.0
        if xs < X_mon_upper:
            def integrand(x):
                m = self.m_opt_Xs(A_j, x)
                return self.Im_Xs(m) * self.pdf_Xs(x) * self.N_pop
            result_mon, _ = quad(integrand, xs, X_mon_upper)
            
        result_f = self.f * self.N_served(A_j)
        return result_mon + result_f

    def K_demand_nbhd_analytical_pareto(self, A_j):
        """Closed-form capital demand for Pareto X_s distribution in neighborhood A_j."""
        p, q, gam, beta, alpha, B0, I, f, X_m, alpha_pareto, N_pop = (
            self.p, self.q, self.gamma, self.beta, self.alpha, self.B0, self.I, self.f,
            self.X_m, self.alpha_pareto, self.N_pop
        )
        Delta = p - q
        D = (alpha - 1) * beta * p + gam * q
        c = beta * Delta / D
        C = q / D
        cost_m = 1.0 + (beta - gam) / beta * q / Delta
        
        AM0_const = p * B0 / Delta + gam * I + f
        numerator = gam * I + f + c * cost_m * (AM0_const - A_j)
        denominator_xs = p * (1.0 + c * cost_m)
        X_star = max(numerator / denominator_xs, X_m)
        
        X_nm = max((AM0_const - A_j) / p, X_m)
        
        frac_xs = (X_m / X_star) ** alpha_pareto
        K_j_f = N_pop * f * frac_xs
        
        K_j_mon = 0.0
        if X_star < X_nm:
            K0 = N_pop * C * alpha_pareto * (X_m ** alpha_pareto)
            A_0 = AM0_const - A_j
            
            def F_ant(x):
                term1 = - (A_0 / alpha_pareto) * (x ** -alpha_pareto)
                term2 = (p / (alpha_pareto - 1.0)) * (x ** -(alpha_pareto - 1.0))
                return K0 * (term1 + term2)
                
            K_j_mon = F_ant(X_nm) - F_ant(X_star)
            
        return max(K_j_mon + K_j_f, 0.0)

    def K_demand_nbhd_analytical(self, A_j):
        """Closed-form capital demand in neighborhood A_j."""
        if self.dist_type == 'pareto':
            return self.K_demand_nbhd_analytical_pareto(A_j)
            
        # Uniform distribution
        p, q, gam, beta, alpha, B0, I, f, X_lo, X_hi, N_pop = (
            self.p, self.q, self.gamma, self.beta, self.alpha, self.B0, self.I, self.f,
            self.X_lo, self.X_hi, self.N_pop
        )
        Delta = p - q
        D = (alpha - 1) * beta * p + gam * q
        c = beta * Delta / D
        cost_m = 1.0 + (beta - gam) / beta * q / Delta
        
        AM0_const = p * B0 / Delta + gam * I + f
        numerator = gam * I + f + c * cost_m * (AM0_const - A_j)
        denominator_xs = p * (1.0 + c * cost_m)
        X_star = np.clip(numerator / denominator_xs, X_lo, X_hi)
        
        X_nm = np.clip((AM0_const - A_j) / p, X_lo, X_hi)
        
        K_j_mon = 0.0
        if X_star < X_nm and X_star < X_hi:
            gap = AM0_const - A_j
            integral_m = c * (X_nm - X_star) * (gap - p / 2.0 * (X_nm + X_star))
            K_j_mon = N_pop / (X_hi - X_lo) * q / (beta * Delta) * integral_m
            
        K_j_f = N_pop * f * (X_hi - X_star) / (X_hi - X_lo)
        
        return max(K_j_mon + K_j_f, 0.0)

    def K_demand_nbhd(self, A_j, method='analytical'):
        """Computes MFI equity capital demanded in neighborhood A_j (analytical by default)."""
        if method == 'analytical':
            return self.K_demand_nbhd_analytical(A_j)
        else:
            return self.K_demand_nbhd_numerical(A_j)

    def capital_demand_grid(self, A_grid, N_potential=100.0, method='analytical'):
        """
        Aggregates total capital demand across a grid of neighborhoods for BankHetX.
        Overrides the base Bank method.
        """
        total = 0.0
        for A_j in A_grid:
            total += self.K_demand_nbhd(A_j, method=method)
        return total

    def avg_surplus_nbhd(self, A_j):
        """Average borrower surplus in neighborhood A_j (per potential borrower)."""
        xs = self.X_star(A_j)
        
        def integrand(x):
            return self.borrower_surplus_Xs(A_j, x) * self.pdf_Xs(x)
            
        hi_bound = np.inf if self.dist_type == 'pareto' else self.X_hi
        result, _ = quad(integrand, xs, hi_bound)
        return result

    def total_surplus_nbhd(self, A_j):
        """Total borrower surplus in neighborhood A_j."""
        return self.N_pop * self.avg_surplus_nbhd(A_j)


if __name__ == '__main__':
    """Sample use of the bankzone class """
    A = np.linspace(0, 140, 100)
    bank = Bank(A, beta=1.2)
    print(bank.breturn(A))
    bank.plotA()
    plt.show()


