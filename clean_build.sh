# Execute this file upon initial git checkout.
# You'll need, on your path:
# The Python libraries sh and jinja2.
# The ImageMagick utility (mogrify in particular, but you install it all at once).
# The Dart toolchain (pub build in particular).

cd zukan_workspace
# copy images from master-images to web/images, resizing and compressing
python webify-images.py 
# Read data from fish_data.txt, generating python (.pkl) and dart files necessary for the project
python generate_fish_list.py
# Generate html documents using the jinja2 template engine
python generate_pages.py
# compile SCSS into CSS, using the compass library
compass compile 
cd ..
# Run pub build to compile dart to javascript, and move resulting website
# to site/static for serving on Google App Engine.
bash compile.sh
