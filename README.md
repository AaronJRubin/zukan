#Introduction

This repository contains the source code for two sites that share CSS, jinja2 templates, and a build process and asset pipeline. One of the sites is hosted at www.takatsugawa-zukan.appspot.com, and one is (to be) hosted at www.takatsugawa-shokubutsu-zukan.appspot.com. The sites are visual encyclopedias of the animals and plants, respectively, inhabitating the areas of the Takatsu and Masuda rivers that flow through Masuda City, Shimane Prefecture, Japan.

#Dependencies

Python 2.7, Ruby 2.0+, Dart, Node, and ImageMagick, as well as various packages/libraries/gems for some of them, are necessary to build this site. It's a lot of dependencies, but they should all be straightforward to install on OS X and Linux. Here's the basic procedure for Mac (if any of the shell commands below don't work the first time, try putting `sudo` in front of them). Linux should be similar; just use apt-get instead of Homebrew.

##Python

Get Python 2.7 installed however you want to, get pip installed with `easy_install pip` if you don't have it already, and run `pip install -r requirements.txt` in the root directory of this project.

##Ruby

Get Ruby 2.0 installed however you want to, get bundler installed with `gem install bundler`, and then run `bundle install` in the root directory of this project.

##Dart

The best way to get the Dart SDK installed and on your PATH is with Homebrew; google around for the details.

##Node

Get npm installed however you want to and run `npm install uglifyjs -g`.

##ImageMagick

Assuming that you have Homebrew installed, run `brew install imagemagick`.

#Architecture

These are statically generated sites, built using the Jinja2 template engine for Python, but using Ruby's Rake tool to manage the build process. If you've heard of Jekyll (the Ruby static site generator) or Hyde (the Python static site generator), that's basically the idea, though I don't use either of those technologies directly. Rake generates a lot of files when you build this site; so that you don't inadvertently edit a generated file, they are chmodded (chmoded?) to read-only upon generation.

##Templates

Templates are stored in templates/, with the files in templates/sites/{site-name} being "full" templates that go into the finished sites in a directory structure that mirrors that of the {site-name} directories, and the ones in templates/layouts, templates/macros, and template/includes being shared jinja2 layouts, macros, and includes that are accessible to both sites.

##Data

The data (represented via YAML) that goes into the templates is stored in data/, and there are two types, automatically processed and manually proccessed, in appropriately named subdirectories. Automatically processed data should consist of yaml files that are, at the top-level, maps; the keys of these maps will be the variables that you will have access to in template files, and the values will be what those variables represent. Manually processed data is data that needs to be processed through Python code in some way and then manually passed to templates in generate_pages.py; this can be useful in cases where (for example) we want the templates to have the data in the form of Python objects, rather than maps.

##Images

Images are stored in master-images, in subdirectories for each site; you will notice that these images (with maybe one or two exceptions) are neither cropped, resized, nor compressed. These images are processed by the Rakefile in the mostly appropriately named compress_images task. Image cropping can be done by adding ".crp" files to the same folder as an image; for an image named abehaze.html, the files that specifies how that image should be cropped should be called abehaze.crp. The syntax of the crop specification is an ImageMagick geometry object (if this description is confusing, look around the contents of master-images/ikimono for an example). Resizing and quality compression is handled (at this point) manually in the Rakefile (by making calls to ImageMagick) on a directory-by-directory basis; using ".rsz" files or ".qual" files would be an interesting idea, however, and it is one that I am considering. One thing to bear in mind with images is that independently of ImageMagick compression, you should be using ImageOptim or some other image optimizer on any new images that you want to add to the site, before you even add them to the repository!

##CSS

I use SCSS and Compass. Run `rake compass_watch` as you edit sass/main.scss to see any changes that you make compiled to CSS, and thereby reflected in both sites, immediately.

##Scripting

I use Javascript for super simple scripts, and Dart for the search functionality on the ichiran.html pages in both sites. The dart files ending in _list.dart are generated programmatically and should not be edited (animal_list.dart and plant_list.dart are generated from jinja2 templates, and the article_list.dart file for both sites is generated by the Rakefile based on the contents of the articles that were produced from templates at a previous stage of the build process.

#Build Process

To build the sites for local testing, run `rake build_web`; to view the sites in a local server, run `rake serve_plants` or `rake serve_animals`; to produce something that will run on Google App Engine (and that is fully minified), run `rake compile`; to deploy to Google App Engine (assuming that you have the credentials), run `rake deploy_plants` or `rake deploy_animals`. You may occasionally need to run `rake clean` or `rake clean_nonimage` if you delete a template or image, but see it still showing up on the site. Unless you were messing with images, favor `rake clean_nonimage` because it's a lot faster (you don't have to recompress and re-resize images again on the next build). You are unlikely to want to run the other Rake tasks in isolation, but nothing will break if you do.
