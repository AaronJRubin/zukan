# -*- coding: utf-8 -*-

import romkan

class Fish:

	def __init__(self, latin = "piscis maximus", genus = u"魚科", romaji="oozakana"):
		self.latin = latin
		self.genus = genus
		self.romaji = romaji
		self.kana = romkan.to_katakana(romaji)

	def to_string(self):
		return u"Fish(%s, %s, %s, %s)" % (self.latin, self.genus, self.romaji, self.kana)

all_fish = [Fish() for _ in range(80)]

print "[",
for fish in all_fish:
	print fish.to_string() + ","

