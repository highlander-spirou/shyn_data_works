import matplotlib.pyplot as plt
import seaborn as sns

def draw_kde_plot(data, column, title):
    fig, ax = plt.subplots()
    sns.kdeplot(ax=ax, data=data, x=column)
    ax.axvline(data[column].mean(), linewidth=1, color='r')
    ax.set_ylabel("")
    ax.set_yticklabels([])
    plt.suptitle(title)