import shutil
import os
import jinja2
import cPickle as pickle
import sys
sys.path.insert(0, './zukan-site')

src = "zukan-site"
dest = "static_site/web"

# Copy images

def copy_tree_overwrite(src, dest):
	if os.path.exists(dest):
		shutil.rmtree(dest)
	shutil.copytree(src, dest)

fish_img_src = os.path.join(src, "static/low-res")
fish_img_dest = os.path.join(dest, "low-res")

copy_tree_overwrite(fish_img_src, fish_img_dest)

seisokuchi_img_src = os.path.join(src, "static/seisokuchi")
seisokuchi_img_dest = os.path.join(dest, "seisokuchi")

copy_tree_overwrite(seisokuchi_img_src, seisokuchi_img_dest)

# End copy images

# Copy CSS

shutil.copy(os.path.join(src, "static/main.css"), os.path.join(dest, "main.css"))

# End Copy CSS

# Set up templating infrastructure

fish_list = pickle.load(open("zukan-site/fish_list.pkl", "rb", pickle.HIGHEST_PROTOCOL))

template_dir = os.path.join(os.path.dirname(__file__), "zukan-site/templates")
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

ichiran = render_str("base/sakana-ichiran.html", fish = fish_list)
write(os.path.join(dest, "index.html"), ichiran.encode('utf8'))

for fish in fish_list:
	template = os.path.join("base/sakana", fish.romaji + ".html")
	template_path = os.path.join("zukan-site/templates", template)
	if os.path.exists(template_path):
		page = render_str(template, fish = fish, background_class = fish.starting_location())
		write(os.path.join(dest, "sakana", fish.romaji + ".html"), page.encode('utf8'))
