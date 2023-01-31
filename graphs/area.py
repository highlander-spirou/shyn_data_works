import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from typing import Optional, Literal, Union

class AreaChart:
    """
    A wrapper class to draw Plt's area chart, comparison with its scaled version 
    """
    def __init__(self, df, scaled_df:Optional[pd.DataFrame]=None):
        self.df = df
        self.scaled_df = scaled_df

    def init_fig(self, plot_type, figsize):
        if plot_type == "single" or plot_type == "scaled":
            fig, ax = plt.subplots(figsize=figsize)
            return fig, ax
        elif plot_type == "both":
            fig, ax = plt.subplots(ncols=2, figsize=figsize)
            return fig, ax
            
    @staticmethod
    def draw_area(ax, df, column_to_draw, colors):
        if column_to_draw is None:
            column_list = df.columns
            ax.stackplot(df.index, [df[i] for i in column_list], labels=column_list, alpha=0.8, colors=colors)
        else: 
            ax.stackplot(df.index, [df[i] for i in column_to_draw], labels=column_to_draw, alpha=0.8, colors=colors)

    @staticmethod  
    def legend_without_duplicate_labels(figure):
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        figure.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(.9, 0.5))

    def __call__(self, plot_type:Literal["single", "scaled", "both"], figsize=(12, 5), column_to_draw:Optional[list]=None, colors:Union[list, str]='pastel'):
        fig, ax = self.init_fig(plot_type, figsize)
        if type(colors) == str:
            cmap = sns.color_palette(colors)
        else:
            cmap = colors
        
        if plot_type == "single":
            self.draw_area(ax=ax, df=self.df, column_to_draw=column_to_draw, colors=cmap)
            ax.locator_params(axis="both", integer=True, tight=True)
            
        elif plot_type == "scaled":
            self.draw_area(ax=ax, df=self.scaled_df, column_to_draw=column_to_draw, colors=cmap)
            ax.locator_params(axis="both", integer=True, tight=True)
            
        elif plot_type == "both":
            self.draw_area(ax=ax[0], df=self.df, column_to_draw=column_to_draw, colors=cmap)
            self.draw_area(ax=ax[1], df=self.scaled_df, column_to_draw=column_to_draw, colors=cmap)
            
            ax[0].locator_params(axis="both", integer=True, tight=True)
            ax[1].locator_params(axis="both", integer=True, tight=True)
            plt.subplots_adjust(wspace=0.1)
            
        self.legend_without_duplicate_labels(fig)