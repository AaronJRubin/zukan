import romkan
import os

for subdir, dirs, files in os.walk("zukan-site/static/low-res/ichiran/"):
	print "[",
	for file in files:
		if file.endswith(".jpg"):
			romaji = file.replace(".jpg", "")
			katakana = romkan.to_katakana(romaji)#.decode("utf-8")
			print 'FishTile(romaji = "%s", label = "%s"),' % (romaji, katakana)
