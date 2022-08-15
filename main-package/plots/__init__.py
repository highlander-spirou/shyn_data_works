import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.figure_factory as ff
from typing import List


def grid_catplot_cols(df, cols:List[str], plot_func, grid_cols=3, figsize=(8, 6), grid=False, **kwargs):
    """
    # Tạo 1 grid và plot dữ liệu theo plot_func của từng column in `cols`
    ### `plot_func` only accepts `x` that is also columns in `cols`
    - so only uses methods like sns.barplot, sns.boxplot: https://seaborn.pydata.org/generated/seaborn.catplot.html
    - for **continuous data** only use sns.kdeplot: https://seaborn.pydata.org/tutorial.html
    
    :params **kwargs: Injected directly into plot_func
    """
    num_rows = round(len(cols)/grid_cols)
    fig, axes = plt.subplots(num_rows, grid_cols, figsize=figsize)
    fig.tight_layout()
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    for col, ax in zip(cols, axes.ravel()): # gán mỗi column trong cols_list to an ax-canvas
        plot_func(col, data=df, ax=ax, **kwargs)
        plt.xlabel(col)
        if grid==False:
            ax.grid(None)
        else:
            ax.grid(which="both", axis="y")
    fig.delaxes(axes[1,2])
    
    
def lineplot_comparison(df_1, df_2, x_axis, cols, legend, grid_cols=3, x_step=3, figsize=(8, 6)):
    """
    # Compare each column in the `cols` from two dataframes in line plot
    
    - The two dataframes **MUST** share the same `x_axis` name
    - `x_axis` **MUST BE** numerical
    
    """
    
    num_rows = round(len(cols)/grid_cols)
    fig, axes = plt.subplots(num_rows, grid_cols, figsize=figsize)
    fig.suptitle("Comparison plots")
    fig.tight_layout()
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    for col, ax in zip(cols, axes.ravel()): # gán mỗi column trong cols_list to an ax-canvas
        sns.lineplot(x=x_axis, y=col, data=df_1, ax=ax, ci=None)
        sns.lineplot(x=x_axis, y=col, data=df_2, ax=ax, linestyle='--', ci=None)
        ax.set(xlabel = "", ylabel="", title = col, 
               xticks = np.arange(df_1[x_axis].min(), df_1[x_axis].max()+1, x_step),  # dùng df.max + 1 vì np.arrange là [start, stop)
               )
        ax.grid(axis="x")
    fig.legend(legend)
    fig.delaxes(axes[1,2])
    
    
def draw_plotly_f_cluster(df, ticks, orient='left', color_threshold=15, layout=(800, 1500)):
    """
    # Vẽ f-cluster hierarchical to investigate the `color_threshold` params cho thuật toán phân cụm
    
    Dataframe **MUST BE** 1 pivot table. Có
    - `pd.pivot(index=['target_of_cluster, e.g city, region ...'], values=['some_numeric_column'], columns=['hue, e.g year, sex ....'])`
    - Ticks == list(df.index)
    
    - layout in format of (width, height)
    
    MUST CALL fig.show() to show the image
    """
    fig = ff.create_dendrogram(df,labels=ticks,orientation=orient,color_threshold=color_threshold)
    fig.update_layout(width=layout[0], height=layout[1])
    return fig