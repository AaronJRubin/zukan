#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class Plant:

    def __init__(self, latin = "", ka = "", zoku = "", romaji = "", kana = "",
            rarity = 3, display_name = "", saitei = 6, saikou = 10, iro = None):
        self.romaji = romaji
        try:
            self.kana = kana.decode('utf-8')
        except Exception:
            self.kana = kana
        self.iro = iro if iro else []
        self.latin = latin if latin else ""
        self.ka = ka if ka else ""
        self.zoku = zoku if zoku else ""
        self.rarity = rarity if rarity else 3
        self.saitei = saitei if saitei else 6
        self.saikou = saikou if saikou else 10
        self.display_name = display_name if display_name else self.kana

    def get_link(self):
        return "/shokubutsu/" + self.romaji + ".html"

    def image(self, suffix):
        return os.path.join("/images/shokubutsu", self.romaji, self.romaji + "-" + suffix + ".jpg")

    def rarity_stars(self):
        return ("&#x2605;" * self.rarity) + ("&#x2606;" * (5 - self.rarity)) 
