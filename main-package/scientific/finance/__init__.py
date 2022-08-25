import numpy as np

sharpe_ratio = lambda data, risk_free_rate=0: (data.mean() - risk_free_rate) / data.std()
sortino_ratio = lambda data, risk_free_rate=0: (data.mean() - risk_free_rate) / data[data<0].std()
m2_ratio = lambda data, benchmark_returns, risk_free=0: (sharpe_ratio(data, risk_free) * benchmark_returns.std()) + risk_free

def information_ratio(data, benchmark_returns):
    return_difference = data - benchmark_returns
    volatility = return_difference.std()
    if volatility == 0:
        return np.nan
    return return_difference.mean() / volatility


def value_at_risk_single(data, confidence):
    
    """
    # Calculate value at risk of a single asset 
    ## Confidence on scale 100 
    """
    return data.quantile(1- confidence/100)


def expected_shortfall(data, confidence):
    """
    # Expected Shortfall hay CVaR đc định nghĩa là mean của các dữ liệu vượt ngoài VaR
    ## Confidence on scale 100 
    """
    var_value = value_at_risk_single(data, confidence)
    
    return data[data <= var_value].mean()


def max_drawdown(data):
    cum_return = (1+data).cumprod()
    peak = cum_return.expanding(min_periods=1).max()
    drawdown = (cum_return/peak) - 1
    return drawdown.min()