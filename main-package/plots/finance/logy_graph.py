import matplotlib.pyplot as plt
import seaborn as sns

from typing import NamedTuple, Tuple


class SeabornFn(NamedTuple):
    plot_fn:str
    kwargs: dict 


class LogYGraph:
    """
    # This class add a side-by-side log-y scale to the graph
    """
    def __init__(self, fn:Tuple[SeabornFn]):
        self.fn = fn
        
    
    def draw(self, figsize=(15,5)):
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=figsize)
        for i in self.fn:
            getattr(sns, i.plot_fn)(**i.kwargs, ax=ax1)
        plt.yscale('log')
        for i in self.fn:
            getattr(sns, i.plot_fn)(**i.kwargs, ax=ax2)
        ax1.legend()
        ax2.legend()
        return fig, ax1, ax2