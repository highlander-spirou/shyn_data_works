import json
import numpy as np
from prodict import Prodict
from typing import TypedDict, List, Tuple
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


def sns_gradient(cmap:str, min_num, max_num):
    """
    Six color gradient from sns.color_palette
    """
    bins = np.linspace(min_num, max_num, 7)
    palette = sns.color_palette(cmap).as_hex() # type:ignore
    i = 0
    return_list = []
    while i < len(bins)-1:
        return_list.append((bins[i], bins[i+1], palette[i]))
        i = i+1
    return return_list


def tailwind_gradient_oneside(palette:list, min_num, max_num):
    """
    The negative and positive use the same color palette
    """
    bins = np.linspace(min_num, max_num, 11)
    i = 0
    return_list = []
    while i < len(bins) - 1:
        return_list.append((bins[i], bins[i + 1], palette[i]))
        i = i + 1
    return return_list


def tailwind_gradient_twosides(color_codes: Tuple[list, list], min_num, max_num):
    """
    The negative and positive use different hue palette
    """
    if min_num < 0:
        bins_negative = np.linspace(min_num, 0, 10)
        bins_positive = np.linspace(0, max_num, 10)[1:]
        bins = np.concatenate((bins_negative, bins_positive))
    else:
        bins = np.linspace(min_num, max_num, 10)

  
    palette = color_codes[0][::-1] + color_codes[1][1:]
    i = 0
    return_list = []
    while i < len(bins)-1:
        return_list.append((bins[i], bins[i+1], palette[i]))
        i = i+1
    return return_list

class GradientToApexRange:
    def __init__(self, fn, palette, min_num, max_num):
        self.fn = fn
        self.palette = palette
        self.min_num = min_num
        self.max_num = max_num

    def render_color(self):
        self.schema = self.fn(self.palette, self.min_num, self.max_num)

    def apex_range(self):
        ranges = []
        for i in self.schema:
            ranges.append({'from': i[0], 'to': i[1], 'color': i[2]})
        return ranges

    def __call__(self):
        self.render_color()
        return self.apex_range()