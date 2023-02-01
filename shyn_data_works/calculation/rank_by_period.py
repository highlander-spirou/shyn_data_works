import pandas as pd
class RankByPeriod:
    def __init__(self, df, rank_col, period_column='period') -> None:
        new_df = df.copy(deep=True)
        self.df = new_df
        self.rank_col = rank_col
        self.period_column = period_column
        
    def rank_by_period(self):
        periods = self.df[self.period_column].unique()
        ranked_period = []
        for i in periods:
            ranked = self.df[self.df[self.period_column] == i][self.rank_col].rank()
            ranked_period.append(pd.merge(self.df, ranked.rename('ranking'), how='inner', left_index=True, right_index=True, copy=False))
            
        self.ranked_period = ranked_period
        
    def merge_(self):
        product = pd.concat(self.ranked_period)
        return product
        
    def __call__(self):
        self.rank_by_period()
        return self.merge_()
    