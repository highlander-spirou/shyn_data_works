from scipy.stats import linregress

class RollingSlope:
    def __init__(self, df, x, y, window=5):
        self.df = df
        self.x = x
        self.y = y
        self.window = window
        
    def __call__(self):
        trend = []
        lower = 0
        upper = self.window
        n = len(self.df) - 1
        while upper <= n:
            slope , _, _, _, _ = linregress(self.df.iloc[lower:upper][self.x], self.df.iloc[lower:upper][self.y])
            trend.append(slope >=0)
            lower = lower + self.window
            upper = upper + self.window
        else:
            slope , _, _, _, _ = linregress(self.df.iloc[lower:n][self.x], self.df.iloc[lower:n][self.y])
            trend.append(slope >=0)
            
        return trend