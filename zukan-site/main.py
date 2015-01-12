#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class FishTile:

    def __init__(self, romaji = "ayu", label = "アユ"):
        #if label == None:
        #    label = romkan.to_katakana(romaji)
        self.label = label.decode('utf-8');
        self.link = "sakana/" + romaji
        self.image = "static/low-res/ichiran/" + romaji + ".jpg"

    def render(self):
        return render_str("fish-tile.html", fish = self)

class Fish:

    def __init__(self, latin = "piscis maximus", genus = u"魚科", romaji = "ayu", kana = u"アユ", location = u"高津川"):
        self.romaji = romaji
        self.kana = kana
        self.latin = latin
        self.genus = genus
        self.location = location

fish_tiles = [FishTile(romaji = "abehaze", label = "アベハゼ"),
FishTile(romaji = "aburabote", label = "アブラボテ"),
FishTile(romaji = "akaza", label = "アカザ"),
FishTile(romaji = "amago", label = "アマゴ"),
FishTile(romaji = "ayu", label = "アユ"),
FishTile(romaji = "ayukake", label = "アユカケ"),
FishTile(romaji = "bora", label = "ボラ"),
FishTile(romaji = "dojou", label = "ドジョウ"),
FishTile(romaji = "donnko", label = "ドンコ"),
FishTile(romaji = "gigi", label = "ギギ"),
FishTile(romaji = "gogi", label = "ゴギ"),
FishTile(romaji = "gokurakuhaze", label = "ゴクラクハゼ"),
FishTile(romaji = "himehaze", label = "ヒメハゼ"),
FishTile(romaji = "hinahaze", label = "ヒナハゼ"),
FishTile(romaji = "hirasuzuki", label = "ヒラスズキ"),
FishTile(romaji = "huna", label = "フナ"),
FishTile(romaji = "ishidojou", label = "イシドジョウ"),
FishTile(romaji = "ishidonko", label = "イシドンコ"),
FishTile(romaji = "itomoroko", label = "イトモロコ"),
FishTile(romaji = "kajika", label = "カジカ"),
FishTile(romaji = "kamatuka", label = "カマツカ"),
FishTile(romaji = "kawaanago", label = "カワアナゴ"),
FishTile(romaji = "kawamutu", label = "カワムツ"),
FishTile(romaji = "kawayoshinobori", label = "カワヨシノボリ"),
FishTile(romaji = "koi", label = "コイ"),
FishTile(romaji = "kurodai", label = "クロダイ"),
FishTile(romaji = "magoti", label = "マゴチ"),
FishTile(romaji = "mahaze", label = "マハゼ"),
FishTile(romaji = "medaka", label = "メダカ"),
FishTile(romaji = "mimizuhaze", label = "ミミズハゼ"),
FishTile(romaji = "mugituku", label = "ムギツク"),
FishTile(romaji = "namazu", label = "ナマズ"),
FishTile(romaji = "numatitibu", label = "ヌマチチブ"),
FishTile(romaji = "oikawa", label = "オイカワ"),
FishTile(romaji = "ooyosinobori", label = "オオヨシノボリ"),
FishTile(romaji = "oyanirami", label = "オヤニラミ"),
FishTile(romaji = "ribbinngo", label = "リッビンゴ"),
FishTile(romaji = "sakuramasu", label = "サクラマス"),
FishTile(romaji = "shimadojou", label = "シマドジョウ"),
FishTile(romaji = "shimaisaki", label = "シマイサキ"),
FishTile(romaji = "shirogisu", label = "シロギス"),
FishTile(romaji = "shirouo", label = "シロウオ"),
FishTile(romaji = "sumiukigori", label = "スミウキゴリ"),
FishTile(romaji = "sunayatume", label = "スナヤツメ"),
FishTile(romaji = "suzuki", label = "スズキ"),
FishTile(romaji = "tairikubaratanago", label = "タイリクバラタナゴ"),
FishTile(romaji = "titibu", label = "チチブ"),
FishTile(romaji = "touyoshinobori", label = "トウヨシノボリ"),
FishTile(romaji = "ugui", label = "ウグイ"),
FishTile(romaji = "ukigori", label = "ウキゴリ"),
FishTile(romaji = "unagi", label = "ウナギ"),
FishTile(romaji = "urohaze", label = "ウロハゼ"),
FishTile(romaji = "yamame", label = "ヤマメ")]

#fish_tiles = [FishTile() for _ in range(80)]

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(**params)

    def render(self, template, **params):
        self.write(self.render_str(template, **params).encode('utf-8'))

class MainHandler(Handler):
    def get(self):
        self.render("sakana-ichiran.html", fish_tiles = fish_tiles);

class FishPageHandler(Handler):
    def get(self, FISH_RE):
        print("Calling FishPageHandler")
        self.render("sakana" + FISH_RE + ".html", fish = Fish()) # later on look up the actual fish

FISH_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/sakana' + FISH_RE, FishPageHandler)
], debug=True)
