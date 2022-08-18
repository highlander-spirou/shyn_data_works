import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px

from typing import Literal

def plot_countplot(data, volume:str, order_list:list=None, **kwargs:Literal['x_label', 'y_label', 'title']):
    """
    # Plot bargrpah
    
    - Volume: cột cần dùng countplot
    - order_list: Ngày trong tuần (2-cn), tháng trong năm, ...
    """
    if order_list is not None:
        sns.countplot(x=data[volume], data=data, order = order_list)
    else:
        sns.countplot(x=data[volume], data=data)
    plt.title(kwargs['title']) if 'title' in kwargs else None
    plt.xlabel(kwargs['x_label']) if 'x_label' in kwargs else None
    plt.ylabel(kwargs['y_label']) if 'y_label' in kwargs else None
    plt.show()
    
    
def plot_heatmap_calender(data, x_column, y_column, figsize = (30,10), title=None, **heatmap_kwargs):
    """
    - `x_column` will hold each hour of each day of week
    - `y_column` will hold the day
    """
    cross_data = pd.crosstab(data[x_column], data[y_column])
    fig, ax = plt.subplots(figsize = figsize)
    sns.heatmap(cross_data, ax = ax, fmt='g', **heatmap_kwargs)
    plt.xticks(rotation=0)
    plt.title(title)
    plt.show()
    
    
def plot_features_grid(data, cols, grid_cols=3, figsize=(20, 20), hue=None):
    """
    # Hàm này dùng để plot countplot của các column có trong `cols` thành 1 grid 
    """
    num_rows = round(len(cols)/grid_cols)
    fig, axes = plt.subplots(num_rows, grid_cols, figsize=figsize, sharey=False)
    fig.tight_layout()
    for col, ax in zip(cols, axes.ravel()):
        sns.countplot(data=data, x=col, ax=ax, hue=hue)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.show()
    
    
def plot_density_on_map(data, hue=None, size=None):
    """
    # Hàm này dùng để plot 2 tập dữ liệu trên map
    
    ### MUST HAVE "longitude" and "latitude" in dataframe
    """
    fig = px.scatter_mapbox(data, lat = 'latitude', lon = 'longitude', color = hue,
                        size = size, color_continuous_scale = px.colors.sequential.Bluered,
                        size_max = 15, zoom = 5, height = 800)
    fig.update_layout(mapbox_style = 'open-street-map')
    fig.show()