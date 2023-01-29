from jinja2 import Environment, FileSystemLoader
from os import path
from typing import Literal, TypedDict

class ParamsDict(TypedDict):
    small_text: str
    big_text: str
    render_img: Literal['<img />', '<svg></svg>']


class CardComponent:
    def __init__(self, template:Literal["default", "templates/file.html", "html str"], params:ParamsDict) -> None:
        if template == "default":
            self.template = """
            <!DOCTYPE html>
<html lang="en">
  <style>
    @import url("https://fonts.googleapis.com/css2?family=Noto+Sans+Gujarati:wght@300;700;900&display=swap");

    boby {
      width: 450px;
      height: 150px;
    }
    .wrapper {
      position: relative;

      width: 300px;
      height: 123px;

      background-color: white;

      border: 0.75px solid rgba(0, 0, 0, 0.1);
      border-radius: 30px;
    }

    .circle {
      display: flex;
      justify-content: center;
      align-items: center;

      position: absolute;
      top: 19%;
      left: 10%;

      background-color: rgba(0, 0, 0, 0.1);
      width: 80px;
      height: 80px;

      border-radius: 50%;
    }

    .image {
      margin-top: 3px;
    }

    .image > img {
      width: 55px;
      height: 55px;
      border-radius: 50%;
    }
    .image > svg {
      width: 55px;
      height: 55px;
      background-color: inherit;
    }

    .box {
      display: flex;
      flex-direction: column;

      position: absolute;
      top: 25%;
      left: 45%;
    }

    .small-text {
      font-family: "Noto Sans Gujarati", sans-serif;
      font-size: 16px;
      font-weight: 300;
      color: rgb(100 116 139);
    }

    .big-text {
      margin-top: 10px;

      font-family: "Noto Sans Gujarati", sans-serif;
      font-size: 32px;
      font-weight: 700;
      color: rgb(68, 84, 104);
    }
  </style>
  <body>
    <div class="wrapper">
      <div class="circle">
        <div class="image">
          {{render_img}}
        </div>
      </div>
      <div class="box">
        <div class="small-text">{{small_text}}</div>
        <div class="big-text">{{big_text}}</div>
      </div>
    </div>
  </body>
</html>

            """
        else:
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
            