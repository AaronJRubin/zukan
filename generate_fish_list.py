#!/usr/bin/env python

import romkan
import os
import sys
sys.path.insert(0, './zukan-site')
from fish import Fish, Location

def generate_defaults():
    res = {}
    for subdir, dirs, files in os.walk("zukan-site/static/low-res/ichiran/"):
        for file in files:
            if file.endswith(".jpg"):
                romaji = file.replace(".jpg", "")
                kana = romkan.to_kana(romaji)#.decode("utf-8")
                res[romaji] = Fish(romaji = romaji, kana = kana)
    return res

def fish_data():
    f = open("fish_data.txt", "r")
    return f.read().split("\n\n")

def string_to_location(string):
    string = string.strip().lower()
    if string == "zyou":
      return Location.ZYOU
    if string == "chuu":
      return Location.CHUU
    if string == "ge":
      return Location.GE 
    if string == "kakou":
      return Location.KAKOU
    raise Exception("Invalid location: " + string)


def parse_fish(fish_string):
    lines = fish_string.split('\n')
    fish = Fish()
    for line in lines:
        split_line = line.strip().split(": ")
        if len(split_line) != 2:
            raise Exception("Fish with malformed field specification in line " + line)
        field, data = split_line
        if field == "name":
            fish.romaji = data
            fish.kana = romkan.to_kana(data)
        if field == "rarity":
            fish.rarity = int(data)
        if field == "takatsu":
            fish.location.set_takatsu(map(string_to_location, data.split(", ")))
    return fish

defaults = generate_defaults()

print defaults
print map(parse_fish, fish_data())


