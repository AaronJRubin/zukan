# -*- coding: utf-8 -*-
# This script is called appropriately by the Rakefile; do not execute it directly, but feel free to edit it.

import os
import jinja2
import cPickle as pickle
import sys
from glob import glob
import yaml

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

try:
    animal_list = pickle.load(open("animal_list.pkl", "rb", pickle.HIGHEST_PROTOCOL))
except IOError:
    print("To run this script, you need to first generate the file animal_list.pkl by running generate_animal_list.py")
    exit()

animal_map = { animal.romaji : animal for animal in animal_list }

data_files = glob("data/general/*")

def parse_yaml_file(path):
    file = open(path, "r")
    contents = file.read()
    file.close()
    return yaml.load(contents)

def destructively_merge_dicts(dict_a, dict_b):
    dict_a.update(dict_b)
    return dict_a

data = reduce(destructively_merge_dicts, map(parse_yaml_file, data_files))

data.update({ "animals" : animal_list, "animal_map" : animal_map })

def render_page(template_path):
    relative_path = template_path.replace("templates/", "")
    template = jinja_env.get_template(relative_path)
    page_name = os.path.splitext(os.path.basename(template_path))[0]
    rendered = template.render(data, page_name = page_name).encode('utf8')
    destination = template_path.replace("templates/pages/", "web/")
    destination_dir = os.path.dirname(destination)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    f = file(destination, "w")
    f.write(rendered)
    f.close()
   
page_template_paths = [path for path in glob("templates/pages/**/*") + glob("templates/pages/*") if not os.path.isdir(path)]

for page_template_path in page_template_paths:
    render_page(page_template_path)
