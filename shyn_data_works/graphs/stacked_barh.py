import seaborn as sns
import matplotlib.pyplot as plt

def draw_stacked_barh(df, top=None, colors='pastel', y_invert=False):
    """
    A wrapper for drawing plt's barh
    """
    if top is None:
        df.plot(kind='barh', stacked=True, color=colors)
    else:
        palette = sns.color_palette(colors)
        df[:top].plot(kind='barh', stacked=True, color=palette)
    
    if y_invert: plt.gca().invert_yaxis()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))