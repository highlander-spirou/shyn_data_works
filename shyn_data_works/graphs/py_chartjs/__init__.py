import json
from ..jinja_template import HTMLRenderEngine
from ..convert_rgba import convert_rgba
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
  </head>
  <body>
    <div class="chart-container">
      <canvas id="myChart" width="{{width}}" height="{{height}}"></canvas>
    </div>

    <script>
      var data = JSON.parse(
        {{chartData}}
      )
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
                "plugins": {},
                "scale": {}
            }
        }
    
        
    def add_chart_type(self, chart_type):
        self.core['type'] = chart_type
        return self
      
    def add_axis_label(self, axis_label:list):
        self.core['data']['labels'] = axis_label 
        return self
    
    def add_dataset(self, label, data, colors:Optional[List[str]] = None, alpha=0.2, **kwargs):
        dataset = dict()
        dataset['label'] = label
        dataset['data'] = data
        
        if colors is not None:
            borderColors = colors
            backgroundColors = [convert_rgba(i, alpha) for i in colors] #type: ignore
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
        

    def serialize(self):
        self.template_data = "'" + json.dumps(self.core) + "'"
        self.render_template(chartData=self.template_data, width=self.width, height=self.height)
        return self.html_str