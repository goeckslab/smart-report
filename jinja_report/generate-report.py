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
        label = self.label or self.src[:-self.suffix] if self.src.endswith(self.suffix) else self.src
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
        label = self.label or self.src[:-len(self.suffix)] if self.src.endswith(self.suffix) else self.src
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
        label = self.label or self.src[:-len(self.suffix)] if self.src.endswith(self.suffix) else self.src
        df = pd.read_csv(self.src)
        return {
            "src": self.src,
            "label": label,
            "title": self.title or label,
            "caption": self.caption,
            "headers": df.columns,
            "values": df.values.tolist(),
        }


@resources_registry()
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
                inputs["image"].append({
                    "id": "image_"+str(len(inputs["image"])),
                    **element,
                    "label": fl[:-4],
                })
            elif fl.endswith(".json"):
                inputs["json"].append({
                    "id": "json_"+str(len(inputs["json"])),
                    **element,
                    "label": fl[:-5],
                })
            elif fl.endswith(".html"):
                inputs["html"].append({
                    "id": "html_"+str(len(inputs["html"])),
                    **element,
                    "label": fl[:-5],
                })
            elif fl.endswith(".csv"):
                inputs["csv"].append({
                    "id": "csv"+str(len(inputs["csv"])),
                    **element,
                    "label": fl[:-4],
                })
            else:
                inputs["others"].append({
                    "id": "others_"+str(len(inputs["others"])),
                    **element,
                    "label": fl,
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
