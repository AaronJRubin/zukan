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
import fish
import jinja_utils
import cPickle as pickle

fish_list = pickle.load(open("fish_list.pkl", "rb", pickle.HIGHEST_PROTOCOL))

fish_dict = {}
for fish in fish_list:
    fish_dict[fish.romaji] = fish

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render(self, template, **params):
        self.write(jinja_utils.render_str(template, **params).encode('utf-8'))

class MainHandler(Handler):
    def get(self):
        self.render("base/sakana-ichiran.html", fish = fish_list);

class FishPageHandler(Handler):
    def get(self, FISH_RE):
        try:
            self.render("base/sakana" + FISH_RE + ".html", fish = fish_dict[FISH_RE[1:]])
        except Exception:
            self.render("base/sakana/generic.html", fish = fish_dict[FISH_RE[1:]])

FISH_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/sakana' + FISH_RE, FishPageHandler)
], debug=True)
