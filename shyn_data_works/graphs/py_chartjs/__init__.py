import json
from ..jinja_template import HTMLRenderEngine
from ..colors import convert_rgba
from typing import Optional, List

class PyChartJs(HTMLRenderEngine):
    """
    Thin wrapper that translate python's object to ChartJS Config object
    """
    def __init__(self, width, height) -> None:
        template = """<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-stacked100@1.3.0"></script>
  </head>
  <body>
    <div class="chart-container">
      <canvas id="myChart" width="{{width}}" height="{{height}}"></canvas>
    </div>

    <script>
      Chart.register(ChartDataLabels);
      Chart.register(ChartjsPluginStacked100.default)
      
      var data = JSON.parse(
        {{chartData}}
      )
      {{jsScript}}
      const ctx = document.getElementById('myChart');
      new Chart(ctx, data);
    </script>
  </body>
</html>
"""
        super().__init__(template)
        self.width= width
        self.height = height
        self.core = {
            "type": None,
            "data": {
                "labels": None,
                "datasets": []
            },
            "options": {
                "responsive": False,
                "interaction": {
                  "intersect": False,
                  "mode": 'nearest',
                  "axis": 'x'
                },
                "plugins": {
                  "datalabels": {
                    'display': False 
                  }
                },
                "scale": {}
            }
        }
        self.js = None
    
        
    def add_chart_type(self, chart_type):
        self.core['type'] = chart_type
        return self
      
    def add_axis_label(self, axis_label:list):
        self.core['data']['labels'] = axis_label 
        return self
    
    def add_dataset(self, label, data, colors:Optional[List[str]] = None, alpha=0.2, no_border=False, **kwargs):
        dataset = dict()
        dataset['label'] = label
        dataset['data'] = data
        
        if colors is not None:
          if no_border is True:
            dataset['backgroundColor'] = colors
          else:
                borderColors = colors
                backgroundColors = [convert_rgba(i, alpha) for i in colors]
                dataset['backgroundColor'] = backgroundColors
                dataset['borderColor'] = borderColors
            
        for index, item in kwargs.items():
            dataset[index] = item
        
        self.core['data']['datasets'].append(dataset)
        
        return self
    
    def add_plugins(self, plugin_dict):
        """
        Plugins including title, legend, ...
        """
        for index, item in plugin_dict.items():
          self.core['options']['plugins'][index] = item
        return self
    
    def add_scale(self, scale_dict):
        for index, item in scale_dict.items():
          self.core['options']['scale'][index] = item
        return self
        
    
    def add_title(self, title_dict):
        """
        Title dictionary
        """
        self.core['options']['plugins']['title'] = title_dict
        return self

    def turn_off_legend(self):
        self.core['options']['plugins']['legend'] = {'display': False}
        return self
    
    def turn_on_datalabels(self):
        self.core['options']['plugins']['datalabels'] = {
          'display': True,
          'color': 'white',
          'font': {
            'weight': 'bold',
            'size': 13,
          }
        }
        return self

    def change_datalabel_colors(self, colors: List[str]):
        self.core['options']['plugins']['datalabels']['color'] = colors
        return self
    
    def add_js(self, js):
        self.js = js
        return self

    def serialize(self):
        self.template_data = "'" + json.dumps(self.core) + "'"
        if self.js is not None:
          self.render_template(chartData=self.template_data, jsScript=self.js, width=self.width, height=self.height)
        else:
          self.render_template(chartData=self.template_data, width=self.width, height=self.height)
        return self.html_str