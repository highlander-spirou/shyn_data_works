import matplotlib.pyplot as plt

def barh_index_highlight(df, x, y='index', highlight:list=None, y_inverted=False): #type: ignore
    fig, ax = plt.subplots()
    if y == 'index':
        ax.barh(y=df.index, width=df[x])
    else:
        ax.barh(y=df[y], width=df[x])
    
    if y_inverted: ax.invert_yaxis()
    
    ## if the code is error, tries to uncomment the following code
    # ax.get_ymajorticklabels()
    
    if highlight is not None:
        for _, tick in enumerate(ax.yaxis.get_major_ticks()):
            if tick.label1.get_text() in highlight:
                tick.label1.set_color('r')
            else:
                tick.label1.set_color('b')