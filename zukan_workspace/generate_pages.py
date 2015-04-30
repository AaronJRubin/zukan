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

try:
	fish_list = pickle.load(open("fish_list.pkl", "rb", pickle.HIGHEST_PROTOCOL))
except IOError:
	print("To run this script, you need to first generate the file fish_list.pkl by running generate_fish_list.py")
	exit()

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

# a Jinja2 filter that gets the name of the current file, without .html
def filename(self):
    quoted = re.findall('\'([^\']*)\'', str(self))
    if quoted:
        path = quoted[0]
        basename = path.split("/")[-1]
        return basename.replace(".html", "")
    else:
        return None

jinja_env.filters['filename'] = filename

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def write(path, string):
	f = file(path, "w")
	f.write(string)
	f.close()

# End set up templating infrastructure

# Build templates and write them to destination

def maybe_mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

maybe_mkdir(os.path.join(dest, "ikimono"))

ichiran = render_str("base/ichiran.html", fish = fish_list)
write(os.path.join(dest, "ikimono/ichiran.html"), ichiran.encode('utf8'))

def render_static_page(name):
	page = render_str("base/" + name + ".html")
	write(os.path.join(dest, name + ".html"), page.encode('utf8'))

render_static_page("home")
render_static_page("about")
render_static_page("sankoubunken")

for fish in fish_list:
	template = os.path.join("base/sakana", fish.romaji + ".html")
	template_path = os.path.join("templates", template)
	if os.path.exists(template_path):
		page = render_str(template, fish = fish, background_class = fish.starting_location())
		write(os.path.join(dest, "ikimono", fish.romaji + ".html"), page.encode('utf8'))
	else:
                print("No article found for " + fish.romaji)
		page = render_str("base/sakana/generic.html", fish = fish, background_class = fish.starting_location())
		write(os.path.join(dest, "ikimono", fish.romaji + ".html"), page.encode('utf8'))

mamechishiki_pages = [path.replace("templates/", "")  for path in glob.glob("templates/base/mamechishiki/*.html")]

maybe_mkdir(os.path.join(dest, "mamechishiki"))

for mamechishiki_page in mamechishiki_pages:
    page = render_str(mamechishiki_page)
    write(os.path.join(dest, "mamechishiki", os.path.basename(mamechishiki_page)), page.encode('utf8'))
