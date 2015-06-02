#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class Plant:

    def __init__(self, latin = "", romaji = "", kana = "",
            display_name = ""):
        self.romaji = romaji
        try:
            self.kana = kana.decode('utf-8')
        except Exception:
            self.kana = kana 
        self.latin = latin if latin else ""
        self.display_name = display_name if display_name else self.kana

    def get_link(self):
        return "/shokubutsu/" + self.romaji + ".html"

    def image(self, suffix):
        return os.path.join("/images/shokubutsu", self.romaji, self.romaji + "-" + suffix + ".jpg")
