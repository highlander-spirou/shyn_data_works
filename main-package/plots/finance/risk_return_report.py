import pandas as pd

from scientific.finance import *
from scientific.finance.portfolio_performance import PortfolioPerformance

class Risk_Return_Ratio_Report:
    """
    # Generates a retport for the Risk-return ratio
    
    ## Input args
    - benchmark: usually a stock market index or reference fund 
    """
    def __init__(self, data, benchmark:pd.Series,risk_free=0) -> None:
        self.data = data
        self.benchmark = benchmark
        self.risk_free = risk_free
        
    def calc_benchmark_indepent(self):
        self.sharpe = self.data.apply(lambda x: sharpe_ratio(x, self.risk_free))
        self.sortino = self.data.apply(lambda x: sortino_ratio(x, self.risk_free))
        self.sharpe.name = 'Sharpe Ratio'
        self.sortino.name = 'Sortino Ratio'
    
    def calc_benchmark_depent(self):
        self.info_ratio = self.data.apply(lambda x: information_ratio(x, self.benchmark))
        self.m2 = self.data.apply(lambda x: m2_ratio(x, self.benchmark, self.risk_free))
        self.info_ratio.name = 'Information Ratio'
        self.m2.name = 'M2 Ratio'
        
        
    def output(self):
        a = pd.concat([self.sharpe, self.sortino, self.info_ratio, self.m2], axis=1).transpose()
        return a
    
    @staticmethod
    def make_pretty(styler):
        styler.format('{:.3f}')
        styler.set_caption('The higher the ratios the better')
        styler.bar(axis=1, align=0, height=50, width=60, color=['red', 'blue'], props="width: 120px; border-right: 1px solid black;")
        return styler
    
    def __call__(self):
        self.calc_benchmark_indepent()
        self.calc_benchmark_depent()
        df = self.output()
        
        return df.style.pipe(self.make_pretty)
    
    
class TwoVariablePortfolioReport:
    """
    # Display the ratio of two variable in a multiple assets portfolio
    ### assume all remains assets has equally weight
    """
    
    def __init__(self, data) -> None:
        self.data = data
        self.rp = {}
        
    def add_steps(self, var1, var2):
        self.var1 = var1
        self.var2 = var2
        
    def seed_weights(self, var1_weight, var2_weight):
        num_assets = len(self.data.columns)
        weights = np.zeros(num_assets)
        weights[0] = var1_weight
        weights[1] = var2_weight
        weights[2:] = ((1 - var1_weight - var2_weight) / (num_assets - 2))
        return weights
    
    def create_portfolio_stat(self):
        for i in self.var1:
            for j in self.var2:
                if i + j > 1:
                    rp = None
                else:
                    PP = PortfolioPerformance(self.data, weights=self.seed_weights(i, j))
                    rp = PP.calc_portfolio_pct()
                    rp.fillna(0, inplace=True)
                if i in self.rp:
                    self.rp[i].append((j, rp))
                else:
                    self.rp[i] = [(j, rp)]
    
    def create_volatility_rp(self, label1, label2):
        result_dict = {}
        for index, value in self.rp.items():
            renamed_index = f'{index*100:.0f}% {label1}'
            for i in value:
                if index + i[0] > 1:
                    volitality = np.nan
                else:
                    volitality = i[1]['portfolio_pct'].std()
                if renamed_index in result_dict:
                    result_dict[renamed_index].append(volitality)
                else:
                    result_dict[renamed_index] = [volitality]
                    
        df = pd.DataFrame(result_dict)
        df.index = [f'{i*100:.0f}% {label2}' for i in self.var2]
        return df.style.highlight_min(axis=None, color='gold').set_caption('Volitality report')
    
    def create_ratio_rp(self, ratio_fn, label1, label2, fn_label):
        result_dict = {}
        for index, value in self.rp.items():
            renamed_index = f'{index*100:.0f}% {label1}'
            for i in value:
                if index + i[0] > 1:
                    rp = np.nan
                else:
                    rp = ratio_fn(i[1]['portfolio_pct'])
                if renamed_index in result_dict:
                    result_dict[renamed_index].append(rp)
                else:
                    result_dict[renamed_index] = [rp]
                    
        df = pd.DataFrame(result_dict)
        df.index = [f'{i*100:.0f}% {label2}' for i in self.var2]
        return df.style.highlight_max(axis=None, color='gold').set_caption(f'{fn_label} report')
                
    def create_var_rp(self, var_fn, confidence, label1, label2, fn_label):
        result_dict = {}
        for index, value in self.rp.items():
            renamed_index = f'{index*100:.0f}% {label1}'
            for i in value:
                if index + i[0] > 1:
                    rp = np.nan
                else:
                    rp = var_fn(i[1]['portfolio_pct'], confidence)
                if renamed_index in result_dict:
                    result_dict[renamed_index].append(rp)
                else:
                    result_dict[renamed_index] = [rp]
                    
        df = pd.DataFrame(result_dict)
        df.index = [f'{i*100:.0f}% {label2}' for i in self.var2]
        return df.style.highlight_max(axis=None, color='gold').set_caption(f'{fn_label} at {confidence} percentile report')