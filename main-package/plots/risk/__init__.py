import pandas as pd
from scientific.risk import *

class DCP_Dist_Moments_Report:
    """
    Generates a retport for the DCP Distribution moments for calculating the risk
    """
    def __init__(self, data) -> None:
        self.data = data
        
    def calc_moments(self):
        """
        Simple moments function from pd method
        """
        volatility = self.data.std()
        volatility.name = 'volatility ⬇'
        kurtosis = self.data.kurt(axis=0)
        kurtosis.name = 'kurtosis ⬇'
        
        self.volatility = volatility
        self.kurtosis = kurtosis
    
    def calc_lambda(self, confidence):
        VaR = self.data.apply(lambda x: value_at_risk_single(x, confidence))
        VaR.name = f'VaR (at {confidence}) ⬆'
        CVaR = self.data.apply(lambda x: expected_shortfall(x, confidence))
        CVaR.name = f'CVaR (at {confidence}) ⬆'
        mdd = self.data.apply(lambda x: max_drawdown(x))
        mdd.name = 'MDD ⬆'
        
        self.VaR = VaR
        self.CVaR = CVaR
        self.mdd = mdd
        
    def output(self):
        a = pd.concat([self.volatility, self.kurtosis, self.VaR, self.CVaR, self.mdd], axis=1).transpose()
        return a
    
    @staticmethod
    def make_pretty(styler):
        styler.set_caption('⬇ means the lower the better, ⬆ otherwise')
        styler.format('{:.3f}')
        styler.bar(align=0, height=50, width=60, color=['red', 'blue'], props="width: 120px; border-right: 1px solid black;")
        return styler
    
    def __call__(self, confidence):
        self.calc_moments()
        self.calc_lambda(confidence=confidence)
        df = self.output()
        
        return df.style.pipe(self.make_pretty)