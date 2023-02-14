import json
from prodict import Prodict
from typing import TypedDict, List
from ..jinja_template import HTMLRenderEngine


class ChartTypeInterface(Prodict):
    type: str

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.toolbar: dict = {'show': False}
        
class SeriesInterface(TypedDict):
    name: str
    data: list

class ApexChartInterface(Prodict):
    chart: ChartTypeInterface
    xaxis: dict
    series: List[SeriesInterface]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if 'series' not in kwargs: self.series = []
        if 'chart' not in kwargs: self.chart = ChartTypeInterface()
        if 'xaxis' not in kwargs: self.xaxis = {}


class PyApexCharts(HTMLRenderEngine):
    def __init__(self, **kwargs) -> None:
        self.apex = ApexChartInterface(**kwargs)
        self.css = None
        self.js = None
        template = """
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
  </head>
  <style>
    {{cssStyling}}
  </style>
  <body>
    <div id="chart"></div>
    <script defer>
      var options = JSON.parse(
        {{chartData}}
      )
      {{jsScript}}
      var chart = new ApexCharts(document.querySelector("#chart"), options);

      chart.render();
    </script>
  </body>
</html>
"""
        super().__init__(template)
        
    def add_css(self, css:str):
        self.css = css
        
    def add_js(self, js:str):
        self.js = js
    
    def serialize(self):
        self.template_data = "'" + json.dumps(self.apex) + "'"
        
        if self.css is not None:
            if self.js is not None:
              self.render_template(chartData=self.template_data, cssStyling=self.css, jsScript=self.js)
            else:
              self.render_template(chartData=self.template_data, cssStyling=self.css)
        else:
            if self.js is not None:
              self.render_template(chartData=self.template_data, jsScript=self.js)
            else:
              self.render_template(chartData=self.template_data)
            
        return self.html_str
    