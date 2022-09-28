"""
Supported data types are:
PNG, JSON, HTML, Others as binary.
"""
import pathlib
import os

from collections import defaultdict
from datetime import datetime

import jinja2
import yaml


REPORT_INPUTS_PATH = pathlib.Path("report_input.yml")
DATA_PATH = "data"
TEMPLATE_PATH = "templates"
STATIC_PATH = "static"


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader([TEMPLATE_PATH, STATIC_PATH]),
)

if REPORT_INPUTS_PATH.exists():
    with open(REPORT_INPUTS_PATH, "r") as fh:
        inputs = yaml.safe_load(fh)
else:
    inputs = defaultdict(list)
    for fl in sorted(os.listdir(DATA_PATH), key=lambda e: e.lower()):
        element =  {"src": DATA_PATH+"/"+fl}
        if fl.endswith(".png"):
            inputs["image"].append({"id": "image_"+str(len(inputs["image"])), **element, "label": fl[:-4]})
        elif fl.endswith(".json"):
            inputs["json"].append({"id": "json_"+str(len(inputs["json"])), **element, "label": fl[:-5]})
        elif fl.endswith(".html"):
            inputs["html"].append({"id": "html_"+str(len(inputs["html"])), **element, "label": fl[:-5]})
        else:
            inputs["others"].append({"id": "others_"+str(len(inputs["others"])), **element, "label": fl})

if not inputs.get('title'):
    inputs["title"] = "Smart Report"

inputs["report_time"] = datetime.now()

# print(dict(inputs))

main_tpl = env.get_template("main.html")

out = main_tpl.render(inputs=dict(inputs))

print(out)
