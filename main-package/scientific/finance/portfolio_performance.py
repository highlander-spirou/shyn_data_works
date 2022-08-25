import pandas as pd
import numpy as np

class PortfolioPerformance:
    
    def __init__(self, data:pd.DataFrame, weights:np.array) -> None:
        self.data = data
        self.weights = weights

    def get_data(self):
        pct_returns = self.data.pct_change()
        mean_returns = pct_returns.mean()
        cov_matrix = pct_returns.cov()
        return pct_returns, mean_returns, cov_matrix
    
    def portfolio_performance(self):
        pct_returns, _, cov_matrix = self.get_data()
        weighted_returns = np.sum(pct_returns*self.weights)
        weighted_std = np.sqrt(np.dot( self.weights.T, np.dot(cov_matrix, self.weights) ))
        return weighted_returns, weighted_std
        
    def calc_portfolio_pct(self):
        pct_returns, _, _ = self.get_data()
        returned_data = self.data.copy(deep=True)
        returned_data['portfolio_pct'] = pct_returns.dot(self.weights)
        return returned_data