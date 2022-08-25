import matplotlib.pyplot as plt

def draw_boxplot_percentile_comparision(data, xlabels:list):
    fig, ax = plt.subplots(figsize=(8,6))
    ax.boxplot(data,labels=xlabels,showfliers=False,showmeans=True,patch_artist=True,
           boxprops=dict(facecolor='whitesmoke'),medianprops=dict(color='lightcoral',linewidth=2.5),meanprops=dict(markerfacecolor='teal',markeredgecolor='teal',markersize=8))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(left=False)
    ax.grid(axis='y')
    
    return fig, ax