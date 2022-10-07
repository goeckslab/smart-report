"""
Supported data types are:
PNG, JSON, HTML, Others as binary.
"""
import csv
import pathlib
import os

from collections import defaultdict
from datetime import datetime

import jinja2
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

    def __init__(self, src: str, label: str = None, title: str = None) -> None:
        super().__init__(src)
        self.label = label
        self.title = title

    @property
    def labelToRender(self):
        label = self.label
        if not label:
            label = self.src[:-len(self.suffix)]\
                if self.suffix and self.src.endswith(self.suffix) else self.src
            if "/" in label:
                label = label[label.rindex("/")+1 :]
        return label

    def render(self) -> dict:
        label = self.labelToRender
        return {
            "src": self.src,
            "label": label,
            "title": self.title or label,
        }


@register_resources()
class Text(Image):
    type = "text"
    suffix = ".txt"

    def render(self) -> dict:
        label = self.labelToRender
        with open(self.src, "r") as fh:
            text = fh.read()
        return {
            "text": text,
            "label": label,
            "title": self.title or label,
        }


@register_resources()
class HTML(Image):
    type = "html"
    suffix = ".html"


@register_resources()
class JSON(Image):
    type = "json"
    suffix = ".json"


@register_resources()
class Table(Image):
    type = "table"
    suffix = ".csv"

    def __init__(
        self,
        src: str,
        label: str = None,
        title: str = None,
        caption: str = None,
    ) -> None:
        super().__init__(src)
        self.label = label
        self.title = title
        self.caption = caption

    def render(self) -> dict:
        label = self.labelToRender
        with open(self.src, newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = list(next(reader))
            values = list(reader)
        return {
            "label": label,
            "title": self.title or label,
            "caption": self.caption,
            "headers": headers,
            "values": values,
        }


@register_resources()
class Unclassified(Image):
    type = "unclassified"
    suffix = ""


def main():
    if REPORT_INPUTS.exists():
        with open(REPORT_INPUTS, "r") as fh:
            inputs = yaml.safe_load(fh)

        id_counter = defaultdict(int)
        for key, section in inputs.items():
            if key == "title":
                continue
            for ix, item in enumerate(section):
                itype = item.pop("type")
                section[ix] = {
                    "id": itype + "_" + str(id_counter[itype]),
                    "type": itype,
                }
                section[ix].update(resources_registry[itype](**item).render())
                id_counter[itype] += 1
    else:
        inputs = defaultdict(list)
        suffix_to_resources = {
            cls.suffix: cls for cls in resources_registry.values() if cls.suffix}
        suffix_to_sections = {
            ".png": "All Images",
            ".html": "Interactive Plots",
            ".txt": "Plain Texts",
            ".csv": "Pretty Tables",
            ".json": "Raw JSONs",
        }
        for fl in sorted(os.listdir(DATA), key=lambda e: e.lower()):
            element =  {"src": DATA + "/" + fl}
            for suffix, cls in suffix_to_resources.items():
                if fl.endswith(suffix):
                    section = suffix_to_sections[suffix]
                    inputs[section].append({
                        "id": cls.type + "_" + str(len(inputs[section])),
                        "type": cls.type,
                        **cls(**element).render(),
                    })
                    break
            else:
                inputs["Miscellaneous"].append({
                    "id": Unclassified.type + "_" +str(len(inputs["Miscellaneous"])),
                    "type": Unclassified.type,
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
