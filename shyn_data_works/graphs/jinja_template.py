from IPython.display import display, HTML # type: ignore
from jinja2 import Environment

class HTMLRenderEngine:
    def __init__(self, template) -> None:
        self.template:str = template
        environment = Environment()
        self.renderer = environment.from_string(template)
        
    def render_template(self, **kwargs):
        html_str = self.renderer.render(**kwargs)
        self.html_str:str = html_str
    
    def save_template(self, destination):
        """
        destination = Path + file.html
        """
        with open(destination, "w") as f:
            f.write(self.html_str)
            
    def show(self):
        display(HTML(self.html_str))  
        
        
