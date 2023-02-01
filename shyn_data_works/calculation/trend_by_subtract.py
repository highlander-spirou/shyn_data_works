import pandas as pd
from typing import Union

class TrendBySubtract:
    def __init__(self, series:Union[list, pd.Series]) -> None:
        if type(series) == list:
            self.series = series
        else:
            self.series = series.to_list() # type: ignore
    
    def __call__(self):
        stack = []
        for i in reversed(range(0, len(self.series))):
            if i > 0:
                stack.append((self.series[i] - self.series[i-1]) >= 0)
        return stack[::-1]