import shutil
import os
import jinja2

dest = "static_site"

img_src = "zukan-site/static/low-res"
img_dest = os.path.join(dest, "low-res")

if os.path.exists(img_dest):
	shutil.rmtree(img_dest)

shutil.copytree(img_src, img_dest)

template_dir = "zukan-site/templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

ichiran = render_str("base/sakana-ichiran.html")

file(os.path.join(dest, "ichiran.html"), "w").write(ichiran).close()