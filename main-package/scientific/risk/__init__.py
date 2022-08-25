def value_at_risk_single(data, confidence):
    
    """
    # Calculate value at risk of a single asset 
    ## Confidence on scale 100 
    """
    return data.quantile(1- confidence/100)


def expected_shortfall(data, confidence):
    """
    Expected Shortfall hay CVaR đc định nghĩa là mean của các dữ liệu vượt ngoài VaR
    """
    var_value = value_at_risk_single(data, confidence)
    
    return data[data <= var_value].mean()


def max_drawdown(data):
    cum_return = (1+data).cumprod()
    peak = cum_return.expanding(min_periods=1).max()
    drawdown = (cum_return/peak) - 1
    return drawdown.min()