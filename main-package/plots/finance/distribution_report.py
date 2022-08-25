import pandas as pd

from scientific.finance import *

class Dist_Moments_Report:
    """
    Generates a retport for the Distribution moments specialize for risk 
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
    
    
    
class CompareExtremeVaR:
    """
    VaR or CVaR at 80, 90, 95, 99 percentile to compare the incremental risk
    """
    def __init__(self, data, var_fn) -> None:
        self.data = data
        self.var_fn = var_fn
        
    def calc_VaR(self):
        self.es80 = self.var_fn(self.data, 80)
        self.es90 = self.var_fn(self.data, 90)
        self.es95 = self.var_fn(self.data, 95)
        self.es99 = self.var_fn(self.data, 99)

    def change_from_(self):
        self.change_es80 = (self.es80 - self.es80)/self.es80
        self.change_es90 = (self.es90 - self.es80)/self.es80
        self.change_es95 = (self.es95 - self.es90)/self.es90
        self.change_es99 = (self.es99 - self.es95)/self.es95
        
    def output(self):
        a = pd.concat([self.es80, self.es90, self.es95, self.es99, self.change_es80, self.change_es90, self.change_es95, self.change_es99], axis=1).transpose()
        a.index = ['CVaR at 80', 'CVaR at 90', 'CVaR at 95', 'CVaR at 99', 'PCT - 80', 'PCT - 90', 'PCT - 95', 'PCT - 99']
        return a  

    @staticmethod
    def make_pretty(styler):
        styler.format('{:.3f}')
        styler.bar(axis=0, align=0, height=50, width=60, color=['red', 'blue'], props="width: 120px; border-right: 1px solid black;")
        return styler
    

    def __call__(self):
        self.calc_VaR()
        self.change_from_()
        df = self.output()
        return df.style.pipe(self.make_pretty)