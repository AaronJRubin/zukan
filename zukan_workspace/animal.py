#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PIL import Image

class Animal:

    def __init__(self, latin = "", ka = "", zoku = "", romaji = "", kana = "",
            rarity = 3, display_name = "", masuda = None, takatsu = None):
        self.romaji = romaji
        try:
            self.kana = kana.decode('utf-8')
        except Exception:
            self.kana = kana
        self.masuda = masuda if masuda else []
        self.takatsu = takatsu if takatsu else []
        self.latin = latin if latin else ""
        self.ka = ka if ka else ""
        self.zoku = zoku if zoku else ""
        self.rarity = rarity if rarity else 3
        self.display_name = display_name if display_name else self.kana

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
