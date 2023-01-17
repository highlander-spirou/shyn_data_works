import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class MinMaxScaler_:
    """
    Wrapper of sklearn MinMaxScaler module
    """
    def __init__(self, df, preserve_index=False):
        self.df = df
        self.preserve_index = preserve_index
        
    def init_scaler(self):
        scaler = MinMaxScaler()
        scaler.fit(self.df)
        self.scaler = scaler
        
    def transform_df(self):
        features = self.scaler.get_feature_names_out()
        scaled_matrix = self.scaler.transform(self.df)
        scaled_df = pd.DataFrame()
        for a, b in zip(features, scaled_matrix.transpose()):
            scaled_df[a] = b
        if self.preserve_index:
            scaled_df.index = self.df.index
        return scaled_df
    
    def __call__(self):
        self.init_scaler()
        return self.transform_df()