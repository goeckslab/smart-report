"""
Supported data types are:
PNG, JSON, HTML, Others as binary.
"""
import pathlib
import os

from collections import defaultdict
from datetime import datetime

import jinja2
import pandas as pd
import yaml


REPORT_INPUTS = pathlib.Path("report_input.yml")
DATA = "data"
TEMPLATE = "templates"
STATIC = "static"

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader([TEMPLATE, STATIC]),
)


resources_registry = {}


def register_resources():
    def wrap(cls):
        resources_registry[cls.type] = cls
        return cls

    return wrap


class BaseResources:
    def __init__(self, src: str) -> None:
        self.src = src

    def render(self) -> dict:
        raise NotImplementedError("Base resources can not render!")

    def lint(self) -> None:
        raise NotImplementedError


@register_resources()
class Image(BaseResources):
    type = "image"
    suffix = ".png"

    def __init__(self, src: str, label: str = None, title: str = None, caption: str = None) -> None:
        super().__init__(src)
        self.label = label
        self.title = title
        self.caption = caption
        

    def render(self) -> dict:
        label = self.label
        if not label:
            label = self.src[:-len(self.suffix)] if self.suffix and self.src.endswith(self.suffix) else self.src
            if "/" in label:
                label = label[label.rindex("/")+1 :]
        return {
            "src": self.src,
            "label": label,
            "title": self.title or label,
            "caption": self.caption,
        }


@register_resources()
class Text(BaseResources):
    type = "text"
    suffix = ".txt"

    def __init__(self, src: str, label: str = None, title: str = None) -> None:
        super().__init__(src)
        self.label = label
        self.title = title

    def render(self) -> dict:
        label = self.label
        if not label:
            label = self.src[:-len(self.suffix)] if self.suffix and self.src.endswith(self.suffix) else self.src
            if "/" in label:
                label = label[label.rindex("/")+1 :]
        return {
            "src": self.src,
            "label": label,
            "title": self.title or label,
        }


@register_resources()
class HTML(Text):
    type = "html"
    suffix = ".html"


@register_resources()
class JSON(HTML):
    type = "json"
    suffix = ".json"


@register_resources()
class Table(Image):
    type = "table"
    suffix = ".csv"

    def render(self) -> dict:
        label = self.label
        if not label:
            label = self.src[:-len(self.suffix)] if self.suffix and self.src.endswith(self.suffix) else self.src
            if "/" in label:
                label = label[label.rindex("/")+1 :]
        df = pd.read_csv(self.src)
        return {
            "src": self.src,
            "label": label,
            "title": self.title or label,
            "caption": self.caption,
            "headers": list(df.columns),
            "values": df.values.tolist(),
        }


@register_resources()
class Unclassified(Text):
    type = "unclassified"
    suffix = ""


def main():
    if REPORT_INPUTS.exists():
        with open(REPORT_INPUTS, "r") as fh:
            inputs = yaml.safe_load(fh)

    else:
        inputs = defaultdict(list)
        for fl in sorted(os.listdir(DATA), key=lambda e: e.lower()):
            element =  {"src": DATA+"/"+fl}
            if fl.endswith(".png"):
                inputs["All Images"].append({
                    "id": "image_"+str(len(inputs["All Images"])),
                    **Image(**element).render()
                })
            elif fl.endswith(".json"):
                inputs["Raw JSONS"].append({
                    "id": "json_"+str(len(inputs["Raw JSONS"])),
                    **JSON(**element).render(),
                })
            elif fl.endswith(".html"):
                inputs["Interactive Plots"].append({
                    "id": "html_"+str(len(inputs["Interactive Plots"])),
                    **HTML(**element).render(),
                })
            elif fl.endswith(".csv"):
                inputs["Pretty Tables"].append({
                    "id": "table_"+str(len(inputs["Pretty Tables"])),
                    **Table(**element).render(),
                })
            elif fl.endswith(".txt"):
                inputs["Plain Texts"].append({
                    "id": "text_"+str(len(inputs["Plain Texts"])),
                    **Text(**element).render(),
                })
            else:
                inputs["Miscellaneous"].append({
                    "id": "misc_"+str(len(inputs["Miscellaneous"])),
                    **Unclassified(**element).render(),
                })

    if not inputs.get('title'):
        inputs["title"] = "Smart Report"

    inputs["report_time"] = datetime.now()

    # print(dict(inputs))

    main_tpl = env.get_template("main.html")

    out = main_tpl.render(inputs=dict(inputs))

    print(out)


if __name__ == "__main__":
    main()
