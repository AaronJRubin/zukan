#Overview

This repository contains the source code for the site hosted at www.takatsugawa-zukan.appspot.com, a visual encyclopedia of the fish inhabitating the Takatsu and Masuda rivers that flow through Masuda City, Shimane Prefecture, Japan. Upon checkout of the repository, running `bundle install`, followed by `rake compile`, will 
build the site from uncompressed images, templates, SCSS, and Dart code in the [zukan_workspace](zukan_workspace) directory, moving the output (in the form of compressed/resized images, HTML documents, CSS, and Javascript) to site/static. The contents of site/static will be a purely static website that can be hosted on any platform without any server-side dependencies, though the various files in [site](site) are those necessary for a deployment to Google App Engine.

#Dependencies for Compilation

You will need the following tools installed and on your PATH. They can all be easily installed with HomeBrew on a Mac (google around for the details), except for the Python libraries, which should be installed via pip or easy_install, and uglifyjs, which should be installed via npm (npm install uglifyjs -g).

* [Ruby](https://www.ruby-lang.org/en/documentation/installation/), preferably with [Bundler](http://bundler.io/) installed via `gem install bundler` to manage dependencies.
* [The Dart SDK](https://www.dartlang.org/tools/sdk/). You will most likely need to manually add dark-sdk/bin/ (contained within the Dart installation directory) to your PATH.
* [ImageMagick](http://www.imagemagick.org/).
* [Python 2.7](https://www.python.org/download/releases/2.7/), with the [jinja2](http://jinja.pocoo.org/docs/dev/) and PIL libraries installed.
* [uglifyjs](https://github.com/mishoo/UglifyJS2).

# How to Work on this Project

As you work on this project, you will be spending most of your time in the [zukan_workspace](zukan_workspace) directory. As you modify the data in [fish_data.txt](zukan_workspace/fish_data.txt) (information encoding the habitats, rarities, and classification information of various fish), and as you modify the [templates](zukan_workspace/templates) to write new articles and change the layout of fish articles, run `rake build_workspace` to see those changes reflected in the HTML documents in the workspace. The [zukan_workspace](zukan_workspace) directory can be opened as a project within Dart Editor, and you will probably want to do that as you modify the scripts, such as [fish_page.dart](zukan_workspace/web/sakana/fish_page.dart) and [ichiran.dart](zukan_workspace/web/ichiran.dart), that add dynamicism to the pages. Compile the code with `rake compile` to get a static website that can be run in every browser and on any platform, stored in site/static. Note that generated files (i.e., files that you should not be editing) are appropriately marked as read-only to make it clear where you should be working.

Image files are stored in [zukan_workspace/master-images](zukan_workspace/master-images) and automatically compressed by Rake and moved into [zukan_workspace/web/images](zukan_workspace/web/images) when you run `rake build_workspace`.


