import pickle
import numpy as np

from dataframes.graph_transform import BarGraphWithColumAsX_axis
from plots.broken_axis import BrokenAxis
with open('cache_df.pickle', 'rb') as f:
    data = pickle.load(f)
    
# process: eleminate some redundant column
data.drop(columns=['close_sp500', 'close_btc', 'gold_usd', 'cpi_us'], inplace=True)
data.fillna(0, inplace=True)
data.reset_index(inplace=True)

bar_graph_cls = BarGraphWithColumAsX_axis(data, column_as_hue='assets', column_as_x_axis='date', value_label='pct_change')
transfomed_data = bar_graph_cls()

broken_ax = BrokenAxis()
cfg_br_ax = broken_ax.generate_kwargs()

cfg_br_ax['figheight'] = 6
cfg_br_ax['figwidth'] = 6
cfg_br_ax['height_ratio'] = 4
cfg_br_ax['suptitle'] = 'Hello world'
cfg_br_ax['legend_title'] = 'Legend'
cfg_br_ax['x_axis_title'] = 'common x title'
cfg_br_ax['y_axis_title'] = 'common y title'
cfg_br_ax['rotation'] = 30

sns_kwarg = {'x':'date', 'y':'pct_change', 'hue':'assets', 'data': transfomed_data}
broken_ax.add_kwarg_attr(**cfg_br_ax)
broken_ax.draw_plot('barplot', sns_kwarg, (-1, 0.5), (10, 12), np.linspace(2014, 2021, 2021-2014+1), )


