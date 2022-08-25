import numpy as np
import pandas as pd

from scientific.finance.portfolio_performance import PortfolioPerformance
from scientific.finance import sortino_ratio


class SimulateEfficientFrontier:
    """
    # Simulate Efficient Frontier and set Sortino Ratio as color density
    """
    def __init__(self, data, n) -> None:
        self.data = data
        self.n = n
    
    @staticmethod
    def seed_random_weights(data):
        weights = np.random.random(len(data.columns))
        weights /= np.sum(weights)
        return weights
    
    def simulation_weight(self):
        np.random.seed(21)
        simul_weight = []
        for i in range(self.n):
            simul_weight.append(self.seed_random_weights(self.data))
            
        self.simul_weight = simul_weight
        
    def calculate_return(self):
        risk_return = []

        for i in self.simul_weight:
            PP = PortfolioPerformance(self.data, i)
            portfolio_pct = PP.calc_portfolio_pct()['portfolio_pct']
            mean_return = portfolio_pct.mean()
            volatility = portfolio_pct.std()
            sortino = sortino_ratio(portfolio_pct)
            weight_seeded = i
            risk_return.append([mean_return, volatility, sortino, weight_seeded])
            
        portfolio_df = pd.DataFrame(risk_return)
        portfolio_df.columns = ['mean', 'volatility', 'sortino ratio', 'weight seed']
        portfolio_df['index_col'] = np.arange(len(portfolio_df))
        
        return portfolio_df
    
    def __call__(self):
        self.simulation_weight()
        return self.calculate_return()