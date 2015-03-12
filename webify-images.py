from sh import cd, mogrify, cp
import os
from collections import defaultdict

cp('-rf', 'master-images/', 'zukan_workspace/web/images/')

cd('zukan_workspace/web/images/sakana')

print("Resizing/compressing fish images...")

for directory in next(os.walk('.'))[1]:
	cd(directory)
	print("Resizing all images of " + directory)
	mogrify('-resize', 'x300', '-quality', '50', '*.jpg')
	cd('..')

print("Finished resizing/compressing fish images.")

cd('../seisokuchi')

quality_settings = defaultdict(lambda: '57')
quality_settings['takatsu-chuu.jpg'] = '75'

print("Resizing/compressing background images")
for directory, subdirectory, files in os.walk('.'):
	for f in filter(lambda f: f.endswith('.jpg'), files):
		mogrify('-resize', '960x', '-quality', quality_settings[f], f)
		if f.endswith('.jpg') and f.find('takatsu') != -1:
			cp(f, f.replace('takatsu', 'masuda'))
print("Finished resizing/compressing background images.")