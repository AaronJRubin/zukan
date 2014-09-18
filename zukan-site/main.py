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

    def __init__(self, label = "さけ", link = "sakana/sake", image = "static/sake.jpg"):
        self.label = label.decode('utf-8');
        self.link = link.decode('utf-8');
        if not image.startswith("static/"):
            image = "static/" + image
        self.image = image 

    def render(self):
        return render_str("fish-tile.html", fish = self)

fish_tiles = [FishTile() for _ in range(80)]

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
        self.render("sakana" + FISH_RE + ".html")

FISH_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/sakana' + FISH_RE, FishPageHandler)
], debug=True)
