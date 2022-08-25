import pandas as pd
import plotly.graph_objects as go
import numpy as np

# from scientific.risk import *


def draw_candle_plotly(data, title):
    """
    ## Input shape 
    | date || open || high ||low || close
    """
    fig = go.Figure(data=[go.Candlestick(
                x=data['date'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'])])
    fig.update_layout(title=title)
    fig.show()


def draw_line_plotly(data, x_col, y_col, title):
    fig = go.Figure(go.Line(x=data[x_col], y=data[y_col]))
    fig.update_layout(title=title)
    fig.show()
    

def draw_ecdf(ax, data, label):
    N= len(data)
    x = np.sort(data)
    y = np.arange(N) / float(N)
    ax.plot(x, y, marker='o')
    ax.set_title(f'CDF of {label}')
    return ax
    

def draw_percentile_boundaries(data, ax, lower, upper, line_color='orange', fontsize=10):
    x_lower = np.percentile(data, lower)
    x_upper = np.percentile(data, upper)
    step_range = (x_upper - x_lower)/10 
    ax.axvline(x_lower, color=line_color)
    ax.axvline(x_upper, color=line_color)
    ax.annotate(f'<- {x_upper/x_lower:.2f} ->', (x_lower + step_range*2, 0.4), fontsize=fontsize)
    
