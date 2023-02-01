import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from typing import Union, Optional

class HighlightProvince:
    """
    # Params
    - geo_source: Nếu là url -> dùng requests serialize thành python dict
    - map_center: Tuple(lat, long)
    - id_property: self.geo_data['features'][i]['properties'].keys() - thường là id hoặc cartodb_id
    - name_property: Là label của province
    - zoom: map zoom level
    - hue_column: Hue *MUST* has index as `province` 
    """
    def __init__(self, geo_source: Union[dict, str], map_center:tuple, id_property:str, name_property:str = 'name', zoom=2, hue_column:Optional[pd.Series]=None) -> None:
        self.geo_source = geo_source
        self.id_property = id_property
        self.name_property = name_property
        self.hue_column = hue_column
        self.map_center = map_center
        self.zoom = zoom
        
    def get_geo_data(self):
        self.geo_data: dict = dict()
        if type(self.geo_source) == str:
            response = requests.get(self.geo_source, timeout=15)
            json_data: dict = response.json()
            self.geo_data = json_data
        else:
            self.geo_data = self.geo_source
            
    def create_df(self):
        province = [self.geo_data['features'][i]['properties'][self.name_property] for i in range(0, len(self.geo_data['features']))]
        id_ = [self.geo_data['features'][i]['properties'][self.id_property] for i in range(0, len(self.geo_data['features']))]
        
        self.df = pd.DataFrame({
            'province': province,
            'id_': id_
        })
    
    def add_hue(self):
        if self.hue_column is not None:
            self.hue_column.name = 'hue'
            new_df = self.df.merge(self.hue_column, how='inner', left_on='province', right_index=True)
            self.df = new_df

        else:
            self.df['hue'] = 0
            
    def setup_plot_params(self):
        if self.hue_column is not None:
            customdata = np.stack(self.df['province'], axis=-1)
            self.params = {
                'geojson': self.geo_data,
                'locations': self.df['id_'],
                'z': self.df['hue'],
                'featureidkey': f'properties.{self.id_property}',
                'colorscale': 'Blues',
                'customdata': customdata,
                'hovertemplate': '<b>%{customdata}</b>',
                'hoverinfo': 'z'
            }
        else:
            self.params = {
                'geojson': self.geo_data,
                'locations': self.df['id_'],
                'featureidkey': f'properties.{self.id_property}',
                'z': self.df['hue'],
                'colorscale': 'Blues',
            }
            
    def draw_plot(self, save=False, name='file'):
        fig = go.Figure(go.Choroplethmapbox(**self.params))


        fig.update_layout(mapbox_style="white-bg", mapbox_center={'lat': self.map_center[0], 'lon': self.map_center[1]}, mapbox_zoom=self.zoom)
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
        )
        fig.update_traces(marker_line_width=1)
        fig.show()
        
        if save is True:
            fig.write_html(f"{name}.html")
            
    def __call__(self):
        self.get_geo_data()
        self.create_df()
        self.add_hue()
        self.setup_plot_params()