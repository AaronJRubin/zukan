#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PIL import Image

class Animal:

    def __init__(self, latin = "piscis maximus", ka = u"魚科", zoku = u"魚属", romaji = "ayu", kana = u"アユ",
            rarity = 3, masuda = None, takatsu = None):
        self.romaji = romaji
        try:
            self.kana = kana.decode('utf-8')
        except Exception:
            self.kana = kana
        self.masuda = masuda if masuda else []
        self.takatsu = takatsu if takatsu else []
        self.latin = latin
        self.ka = ka
        self.zoku = zoku
        self.rarity = rarity

    def get_link(self):
        return "/ikimono/" + self.romaji + ".html"

    def image(self, suffix):
        return os.path.join("/images/ikimono", self.romaji, self.romaji + "-" + suffix + ".jpg")

    def takatsu_inhabits(self, ryuuiki):
        return ryuuiki in self.takatsu

    def masuda_inhabits(self, ryuuiki):
        return ryuuiki in self.masuda

    def starting_location(self):
        locations = self.locations()
        return locations[0] if locations else ""

    def locations(self):
        return ["takatsu-" + ryuuiki for ryuuiki in self.takatsu] + ["masuda-" + ryuuiki for ryuuiki in self.masuda]

    def rarity_stars(self):
        return ("&#x2605;" * self.rarity) + ("&#x2606;" * (5 - self.rarity))

    def is_long(self):
        ichiran_img = os.path.join("web", self.image('ichiran')[1:]) # remove root slash  
        width, height = Image.open(ichiran_img).size
        return height * 1.99 <= width

    def display_name(self):
        if self.kana == u'ミシシッピアカミミガメ':
            return u'アカミミガメ'
        else:
            return self.kana
