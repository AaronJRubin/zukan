#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import romkan

def try_unicode(str):
    try:
        return str.decode('utf-8')
    except Exception:
        return str

class Plant:

    def __init__(self, latin = "", romaji = "", kana = "",
            display_name = "", type = "", kaki = None, seiikubasho = None, bunpu = None, kishibe_type = None):
        kana = try_unicode(kana)
        if not romaji and kana:
            romaji = romkan.to_roma(kana).replace("n'", "nn")
        elif not kana and romaji:
            kana = romkan.to_kana(romaji)
        self.romaji = romaji
        self.kana = kana
        self.latin = latin if latin else ""
        self.display_name = display_name if display_name else self.kana
        self.kaki = kaki if kaki else []
        self.bunpu = bunpu if bunpu else []
        self.kishibe_type = kishibe_type
        self.seiikubasho = seiikubasho if seiikubasho else []
        self.type = type if type else ""

    def get_link(self):
        return "/shokubutsu/" + self.romaji + ".html"

    def image(self, suffix):
        return os.path.join("/images/shokubutsu_", self.romaji, self.romaji + "-" + suffix + ".jpg")

    def blooms(self, month):
        return month in self.kaki

    def inhabits(self, basho):
        return basho in self.seiikubasho

    @staticmethod
    def dart_list(ls):
        return "[" + ", ".join(['"' + str + '"' for str in ls]) + "]"

    def dart_bunpu(self):
        return Plant.dart_list(self.bunpu)

    def dart_seiikubasho(self):
        return Plant.dart_list(self.seiikubasho)
