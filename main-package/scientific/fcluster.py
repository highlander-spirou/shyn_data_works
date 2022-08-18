from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler

from bases import BaseClass

from typing import Literal, Optional


class ScipyFcluster(metaclass=BaseClass):
    def __init__(self, data, normalize=True, method='complete'):
        """
        Create Z-linkage distance matrix from data params
        data must be an aggregated table that has unique index label
        data is normalized by sklearn.StdScaler
        """
        self.data = data
        self.normalize = normalize
        self.Z = linkage(data, method=method)
    
    @staticmethod
    def generate_dendrogram_params(kw_params: Optional[dict]=None, color_threshold=100, leaf_font_size=10, orientation='right'):
        """
        # Generate kw-arguments for drawing dendrogram
        """
        if kw_params is not None: return kw_params
        else:
            dn_params = {
                'color_threshold': color_threshold,
                'leaf_font_size': leaf_font_size,
                'orientation': orientation
            }
            return dn_params
    
    
    def normalize_data(self):
        scaler = StandardScaler()
        scaled_df = pd.DataFrame(scaler.fit_transform(self.data), index=self.data.index, columns=self.data.columns)
        scaled_df.dropna(inplace=True)
        self.data = scaled_df
        
    def __post_init__(self):
        if self.normalize:
            self.normalize_data()
        
    
    def draw_dendrogram(self, figsize=(20, 20), **kargs):
        fig, ax = plt.subplots(figsize=figsize)
        dn = dendrogram(self.Z, labels=self.data.index, **kargs)
        self.dn = dn
        plt.show()
        
    def get_clustered(self):
        index_list = zip(self.dn['ivl'], self.dn['leaves_color_list'])
        self.clustered_data = list(index_list)
        return list(index_list)
    
    def get_clustered_by_label(self, label):
        re = filter(lambda x: x[1] == label, self.clustered_data)
        return list(re)
        
    
    
        
        