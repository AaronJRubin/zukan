# -*- coding: utf-8 -*-
# This script is called appropriately by the Rakefile; do not execute it directly, but feel free to edit it.

import os
import jinja2
import sys
from glob import glob
import yaml
from animal import Animal
from plant import Plant

template_dirs = [os.path.join(os.path.dirname(__file__), "templates", directory) for directory in ["sites", "layouts", "macros", "includes"]]
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dirs))

def parse_yaml_file(path):
    file = open(path, "r")
    contents = file.read()
    file.close()
    return yaml.load(contents)

animal_data = parse_yaml_file("data/manually_processed/animal_data.yaml")

animal_list = sorted([Animal(romaji = romaji, **fields) for romaji, fields in animal_data.iteritems()], key = lambda animal: animal.kana)

animal_map = { animal.romaji : animal for animal in animal_list }

plant_data = parse_yaml_file("data/manually_processed/plant_data.yaml")

plant_list = sorted([Plant(romaji = romaji, **fields) for romaji, fields in plant_data.iteritems()], key = lambda plant: plant.kana)

plant_map = { plant.romaji : plant for plant in plant_list }

def destructively_merge_dicts(dict_a, dict_b):
    dict_a.update(dict_b)
    return dict_a

data_files = glob("data/automatically_processed/*")

data = reduce(destructively_merge_dicts, map(parse_yaml_file, data_files))

data.update({ "animals" : animal_list, "animal_map" : animal_map, "plants" : plant_list, "plant_map" : plant_map })

def render_page(template_path):
    relative_path = template_path.replace("templates/sites/", "")
    template = jinja_env.get_template(relative_path)
    page_name = os.path.splitext(os.path.basename(template_path))[0]
    rendered = template.render(data, page_name = page_name).encode('utf8')
    target_workspace = template_path.split("/")[2]
    path_within_web = os.path.join(*template_path.split("/")[3:]) 
    destination = os.path.join(target_workspace, "web", path_within_web)
    destination_dir = os.path.dirname(destination)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    f = file(destination, "w")
    f.write(rendered)
    f.close()
   
page_template_paths = [path for path in glob("templates/sites/**/*") + glob("templates/sites/**/**/*") if not os.path.isdir(path)]

for page_template_path in page_template_paths:
    render_page(page_template_path)
