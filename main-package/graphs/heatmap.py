import numpy as np
import seaborn as sns

def draw_heatmap(df, cmap='vlag'):
    mask = np.triu(np.ones_like(df.reset_index().corr()))
    sns.heatmap(df.reset_index().corr(), cmap=cmap, mask = mask)