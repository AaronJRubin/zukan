from datetime import datetime
import os

f = file("site/static/takatsugawa-zukan.appcache", "w")
f.write("CACHE MANIFEST\n")
f.write("# " + str(datetime.now()) + "\n")

for subdir, dirs, files in os.walk("site/static/"):
	subdir = subdir.replace("site/static/", "")
	for a_file in files:
		if a_file.endswith(".jpg"):
			f.write(os.path.join(subdir, a_file) + "\n")


f.write("stylesheets/main.css\n")
f.write("packages/browser/dart.js")
f.write("ichiran.dart.js")
f.write("sakana/fish_page.dart.js")

f.write("\nNETWORK:\n*")

f.close()