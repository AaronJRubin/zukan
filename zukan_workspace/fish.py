#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class Location:

    ZYOU, CHUU, GE, KAKOU = range(4)

    def __init__(self):
        self._dict = {"Takatsu" : {}, "Masuda" : {}}
        self._dict["Takatsu"] = set()
        self._dict["Masuda"] = set()

    def set_takatsu(self, locations):
        for location in locations:
            self._dict["Takatsu"].add(location)

    def set_masuda(self, locations):
        for location in locations:
            self._dict["Masuda"].add(location)

    def get_takatsu(self):
        return frozenset(self._dict["Takatsu"])

    def get_masuda(self):
        return frozenset(self._dict["Masuda"])

class Fish:

    def __init__(self, latin = "piscis maximus", family = u"魚科", genus = u"魚属", romaji = "ayu", kana = u"アユ",
        rarity = 3):
        self.romaji = romaji
        try:
            self.kana = kana.decode('utf-8')
        except Exception:
            self.kana = kana
        self.latin = latin
        self.family = family
        self.genus = genus
        self.location = Location()
        self.rarity = rarity

    def get_link(self):
        return "/ikimono/" + self.romaji + ".html"

    def image(self, suffix):
        return os.path.join("/images/ikimono", self.romaji, self.romaji + "-" + suffix + ".jpg")

    def takatsu_zyou(self):
        return Location.ZYOU in self.location.get_takatsu()

    def masuda_zyou(self):
        return Location.ZYOU in self.location.get_masuda()

    def takatsu_chuu(self):
        return Location.CHUU in self.location.get_takatsu()

    def masuda_chuu(self):
        return Location.CHUU in self.location.get_masuda()

    def takatsu_ge(self):
        return Location.GE in self.location.get_takatsu()

    def masuda_ge(self):
        return Location.GE in self.location.get_masuda()

    def takatsu_kakou(self):
        return Location.KAKOU in self.location.get_takatsu()

    def masuda_kakou(self):
        return Location.KAKOU in self.location.get_masuda()

    def starting_location(self):
        if self.takatsu_zyou():
            return "takatsu-zyou"
        if self.takatsu_chuu():
            return "takatsu-chuu"
        if self.takatsu_ge():
            return "takatsu-ge"
        if self.takatsu_kakou():
            return "takatsu-kakou"
        if self.masuda_zyou():
            return "masuda-zyou"
        if self.masuda_chuu():
            return "masuda-chuu"
        if self.masuda_ge():
            return "masuda-ge"
        if self.masuda_kakou():
            return "masuda-kakou"
        return ""

    def rarity_stars(self):
        return ("&#x2605;" * self.rarity) + ("&#x2606;" * (5 - self.rarity))
