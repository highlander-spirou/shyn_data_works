from jinja2 import Environment, FileSystemLoader
from os import path
from typing import Literal, TypedDict

class ParamsDict(TypedDict):
    small_text: str
    big_text: str
    render_img: Literal['<img />', '<svg></svg>']


class CardComponent:
    def __init__(self, template:Literal["templates/file.html", "html str"], params:ParamsDict) -> None:
        self.template=template
        self.params = params
        
    def init_template(self):
        if path.exists(self.template):
            environment = Environment(loader=FileSystemLoader("templates/"))
            renderer = environment.get_template(self.template.split('/')[1])
        else:
            environment = Environment()
            renderer = environment.from_string(self.template)
            
        self.renderer = renderer
        
    def render_content(self):
        self.content = self.renderer.render(**self.params)
        return self.content
    
    def save_file(self, filename):
        with open(f"{filename}.html", mode="w", encoding="utf-8") as f:
            f.write(self.content)
            
    def __call__(self):
        self.init_template()
        return self.render_content()
            