# -*- coding: utf-8 -*-

import os
import jinja2
import cPickle as pickle
import sys

dest = "web"

# Set up templating infrastructure

try:
	fish_list = pickle.load(open("fish_list.pkl", "rb", pickle.HIGHEST_PROTOCOL))
except IOError:
	print("To run this script, you need to first generate the file fish_list.pkl by running generate_fish_list.py")
	exit()

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def write(path, string):
	f = file(path, "w")
	f.write(string)
	f.close()

# End set up templating infrastructure

# Build templates and write them to destination

ichiran = render_str("base/ichiran.html", fish = fish_list)
write(os.path.join(dest, "ichiran.html"), ichiran.encode('utf8'))

def render_static_page(name):
	page = render_str("base/" + name + ".html")
	write(os.path.join(dest, name + ".html"), page.encode('utf8'))

render_static_page("home")
render_static_page("contact")
render_static_page("sankoubunken")

"""
home = render_str("base/home.html");
write(os.path.join(dest, "home.html"), home.encode('utf8'))
contact = render_str("base/contact.html")
write(os.path.join(dest, "contact.html"), contact.encode('utf8'))
kaisetsu = render_str("base/kaisetsu.html")
write(os.path.join(dest, "kaisetsu.html"), kaisetsu.encode('utf8'))
"""
for fish in fish_list:
	template = os.path.join("base/sakana", fish.romaji + ".html")
	template_path = os.path.join("templates", template)
	if os.path.exists(template_path):
		page = render_str(template, fish = fish, background_class = fish.starting_location())
		write(os.path.join(dest, "sakana", fish.romaji + ".html"), page.encode('utf8'))
	else:
                print("No article found for " + fish.romaji)
		page = render_str("base/sakana/generic.html", fish = fish, background_class = fish.starting_location())
		write(os.path.join(dest, "sakana", fish.romaji + ".html"), page.encode('utf8'))

