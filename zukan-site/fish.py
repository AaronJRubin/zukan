#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jinja_utils

class Location:

    ZYOU, CHUU, GE, KAKOU = range(4)

    def __init__(self):
        self._dict = {"Takatsu" : {}, "Masuda" : {}}
        self._dict["Takatsu"] = set()
        self._dict["Masuda"] = set()

    def set_takatsu(self, *locations):
        for location in locations:
            self._dict["Takatsu"].add(location)

    def set_masuda(self, *locations):
        for location in locations:
            self._dict["Masuda"].add(location)

    def get_takatsu(self):
        return frozenset(self._dict["Takatsu"])

    def get_masuda(self):
        return frozenset(self._dict["Masuda"])

class Fish:

    def __init__(self, latin = "piscis maximus", family = u"魚科", genus = u"魚族", romaji = "ayu", kana = u"アユ", location = Location(),
        rarity = 3):
        self.romaji = romaji
        try:
            self.kana = kana.decode('utf-8')
        except Exception:
            self.kana = kana
        self.latin = latin
        self.family = family
        self.genus = genus
        self.location = location
        self.rarity = rarity
        self.link = "sakana/" + romaji
        self.image = "static/low-res/ichiran/" + romaji + ".jpg"

    def render_tile(self):
        return jinja_utils.render_str("fish-tile.html", fish = self)

    def takatsu_zyou(self):
        return Location.ZYOU in self.location.get_takatsu()

    def masuda_zyou(self):
        return Location.ZYOU in self.location.get_masuda()

    def rarity_stars(self):
        return ("&#x2605" * self.rarity) + ("&#x2606" * (5 - self.rarity))

akaza_loc = Location()
akaza_loc.set_takatsu(Location.ZYOU)
akaza_loc.set_masuda(Location.ZYOU)
akaza = Fish(romaji = "akaza", kana = "アカザ", location = akaza_loc)

fish_list = [Fish(romaji = "abehaze", kana = "アベハゼ"),
Fish(romaji = "aburabote", kana = "アブラボテ"),
Fish(romaji = "akaza", kana = "アカザ"),
Fish(romaji = "amago", kana = "アマゴ"),
Fish(romaji = "ayu", kana = "アユ"),
Fish(romaji = "ayukake", kana = "アユカケ"),
Fish(romaji = "bora", kana = "ボラ"),
Fish(romaji = "dojou", kana = "ドジョウ"),
Fish(romaji = "donnko", kana = "ドンコ"),
Fish(romaji = "gigi", kana = "ギギ"),
Fish(romaji = "gogi", kana = "ゴギ"),
Fish(romaji = "gokurakuhaze", kana = "ゴクラクハゼ"),
Fish(romaji = "himehaze", kana = "ヒメハゼ"),
Fish(romaji = "hinahaze", kana = "ヒナハゼ"),
Fish(romaji = "hirasuzuki", kana = "ヒラスズキ"),
Fish(romaji = "huna", kana = "フナ"),
Fish(romaji = "ishidojou", kana = "イシドジョウ"),
Fish(romaji = "ishidonko", kana = "イシドンコ"),
Fish(romaji = "itomoroko", kana = "イトモロコ"),
Fish(romaji = "kajika", kana = "カジカ"),
Fish(romaji = "kamatuka", kana = "カマツカ"),
Fish(romaji = "kawaanago", kana = "カワアナゴ"),
Fish(romaji = "kawamutu", kana = "カワムツ"),
Fish(romaji = "kawayoshinobori", kana = "カワヨシノボリ"),
Fish(romaji = "koi", kana = "コイ"),
Fish(romaji = "kurodai", kana = "クロダイ"),
Fish(romaji = "magoti", kana = "マゴチ"),
Fish(romaji = "mahaze", kana = "マハゼ"),
Fish(romaji = "medaka", kana = "メダカ"),
Fish(romaji = "mimizuhaze", kana = "ミミズハゼ"),
Fish(romaji = "mugituku", kana = "ムギツク"),
Fish(romaji = "namazu", kana = "ナマズ"),
Fish(romaji = "numatitibu", kana = "ヌマチチブ"),
Fish(romaji = "oikawa", kana = "オイカワ"),
Fish(romaji = "ooyosinobori", kana = "オオヨシノボリ"),
Fish(romaji = "oyanirami", kana = "オヤニラミ"),
Fish(romaji = "ribbinngo", kana = "リッビンゴ"),
Fish(romaji = "sakuramasu", kana = "サクラマス"),
Fish(romaji = "shimadojou", kana = "シマドジョウ"),
Fish(romaji = "shimaisaki", kana = "シマイサキ"),
Fish(romaji = "shirogisu", kana = "シロギス"),
Fish(romaji = "shirouo", kana = "シロウオ"),
Fish(romaji = "sumiukigori", kana = "スミウキゴリ"),
Fish(romaji = "sunayatume", kana = "スナヤツメ"),
Fish(romaji = "suzuki", kana = "スズキ"),
Fish(romaji = "tairikubaratanago", kana = "タイリクバラタナゴ"),
Fish(romaji = "titibu", kana = "チチブ"),
Fish(romaji = "touyoshinobori", kana = "トウヨシノボリ"),
Fish(romaji = "ugui", kana = "ウグイ"),
Fish(romaji = "ukigori", kana = "ウキゴリ"),
Fish(romaji = "unagi", kana = "ウナギ"),
Fish(romaji = "urohaze", kana = "ウロハゼ"),
Fish(romaji = "yamame", kana = "ヤマメ")]

fish_dict = {}

for a_fish in fish_list:
    fish_dict[a_fish.romaji] = a_fish

fish_dict["akaza"] = akaza

fish_list = fish_dict.values()
fish_list.sort(key = lambda fish: fish.romaji)