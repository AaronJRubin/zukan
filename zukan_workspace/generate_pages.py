# -*- coding: utf-8 -*-

import os
import jinja2
import cPickle as pickle
import sys

dest = "web"

# Set up templating infrastructure

fish_list = pickle.load(open("fish_list.pkl", "rb", pickle.HIGHEST_PROTOCOL))

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

latin_ryuuiki = ["zyou", "chuu", "ge", "kakou"]
latin_seisokuchi = ["takatsu-" + iki for iki in latin_ryuuiki] + ["masuda-" + iki for iki in latin_ryuuiki]
kanji_ryuuiki = [u"上流", u"中流", u"下流", u"河口"]
kanji_seisokuchi = [u"高津川" + iki for iki in kanji_ryuuiki] + [u"益田川" + iki for iki in kanji_ryuuiki]
seisokuchi = zip(latin_seisokuchi, kanji_seisokuchi)
ryuuiki = zip(latin_ryuuiki, kanji_ryuuiki)
# map(lambda string: string.decode('utf8'),
ichiran = render_str("base/sakana-ichiran.html", fish = fish_list, seisokuchi = seisokuchi, ryuuiki = ryuuiki)
write(os.path.join(dest, "ichiran.html"), ichiran.encode('utf8'))
index = render_str("base/index.html");
write(os.path.join(dest, "index.html"), index.encode('utf8'))
index = render_str("base/contact.html");
write(os.path.join(dest, "contact.html"), index.encode('utf8'))

for fish in fish_list:
	template = os.path.join("base/sakana", fish.romaji + ".html")
	template_path = os.path.join("templates", template)
	if os.path.exists(template_path):
		page = render_str(template, fish = fish, background_class = fish.starting_location())
		write(os.path.join(dest, "sakana", fish.romaji + ".html"), page.encode('utf8'))
	else:
		page = render_str("base/sakana/generic.html", fish = fish, background_class = fish.starting_location())
		write(os.path.join(dest, "sakana", fish.romaji + ".html"), page.encode('utf8'))

