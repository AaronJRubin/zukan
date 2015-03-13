#Overview

This repository contains the source code for the site hosted at www.takatsugawa-zukan.appspot.com, a visual encyclopedia of the fish inhabitating the Takatsu and Masuda rivers that flow through Masuda City, Shimane Prefecture, Japan. Upon checkout of the repository, running the [clean_build.sh](clean_build.sh) script will 
build the site from uncompressed images, templates, SCSS, and Dart code in the [zukan_workspace](zukan_workspace) directory, moving the output (in the form of compressed/resized images, HTML documents, CSS, and Javascript) to [site/static](site/static). The contents of [site/static](site/static) are a purely static website that can be hosted on any platform without any server-side dependencies, though the various files in [site](site) are those necessary for a deployment to Google App Engine.

#Dependencies for Compilation

You will need the following tools installed and on your PATH:

* [Sass](http://sass-lang.com/) with [Compass](http://compass-style.org/)
* [The Dart SDK](https://www.dartlang.org/tools/sdk/). You will most likely need to manually add dark-sdk/bin/ (contained within the Dart installation directory) to your PATH.
* [ImageMagick](http://www.imagemagick.org/)
* [Python 2.7](https://www.python.org/download/releases/2.7/), with the [jinja2](http://jinja.pocoo.org/docs/dev/) and [sh](https://pypi.python.org/pypi/sh) libraries installed.

# How to Work on this Project

As you work on this project, you will be spending most of your time in the [zukan_workspace](zukan_workspace) directory. When you need to update the data for a particular species of fish, you will be modifying fish_data.txt, and then running generate_fish_list.py, followed by generate_pages.py, for your changes to be reflected in the rest of the project. When you need to modify fish articles, you will be modifying the templates in [zukan_workspace/templates/base/sakana/](zukan_workspace/templates/base/sakana/), and then running generate_pages.py.
The [zukan_workspace](zukan_workspace) directory can be opened as a projet within Dart Editor.


