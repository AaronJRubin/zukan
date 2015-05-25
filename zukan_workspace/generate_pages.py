# -*- coding: utf-8 -*-
# This script is called appropriately by the Rakefile; do not execute it directly, but feel free to edit it.

import os
import jinja2
import cPickle as pickle
import sys
import glob
import re

dest = "web"

# Set up templating infrastructure

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

# a Jinja2 filter that gets the name of the current file, without .html
def title(self):
    quoted = re.findall('\'([^\']*)\'', str(self))
    if quoted:
        path = quoted[0]
        basename = path.split("/")[-1]
        return basename.replace(".html", "")
    else:
        return None

jinja_env.filters['title'] = title

try:
    animal_list = pickle.load(open("animal_list.pkl", "rb", pickle.HIGHEST_PROTOCOL))
except IOError:
    print("To run this script, you need to first generate the file animal_list.pkl by running generate_animal_list.py")
    exit()

animal_map = { animal.romaji : animal for animal in animal_list }

data = { "animals" : animal_list }

def is_animal_page(path): 
    return "pages/ikimono/" in path and "ichiran.html" not in path

def render_page(template_path):
    relative_path = template_path.replace("templates/", "")
    template = jinja_env.get_template(relative_path)
    if is_animal_page(template_path):
        animal_name = os.path.splitext(os.path.basename(template_path))[0]
        animal = animal_map[animal_name] 
        rendered = template.render(animal = animal).encode('utf8')
    else:
        rendered = template.render(animals = animal_list).encode('utf8')
    destination = template_path.replace("templates/pages/", "web/")
    destination_dir = os.path.dirname(destination)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    f = file(destination, "w")
    f.write(rendered)
    f.close()
   
page_template_paths = [path for path in glob.glob("templates/pages/**/*") + glob.glob("templates/pages/*") if not os.path.isdir(path)]

for page_template_path in page_template_paths:
    render_page(page_template_path)
