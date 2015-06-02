#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import romkan

class Plant:

    def __init__(self, latin = "", romaji = "", kana = "",
            display_name = "", type = "", kaki = None, seiikubasho = None, bunpu = None, ganpen_type = None):
        try:
            kana = kana.decode('utf-8')
        except Exception:
            pass
        if not romaji and kana:
            romaji = romkan.to_roma(kana)
        elif not kana and romaji:
            kana = romkan.to_kana(romaji)
        self.romaji = romaji
        self.kana = kana
        self.romaji = romaji
        self.latin = latin if latin else ""
        self.display_name = display_name if display_name else self.kana
        self.kaki = kaki if kaki else []
        self.bunpu = bunpu if bunpu else []
        self.ganpen_type = ganpen_type
        self.seiikubasho = seiikubasho if seiikubasho else []
        self.type = type if type else ""

    def get_link(self):
        return "/shokubutsu/" + self.romaji + ".html"

    def image(self, suffix):
        return os.path.join("/images/shokubutsu", self.romaji, self.romaji + "-" + suffix + ".jpg")
