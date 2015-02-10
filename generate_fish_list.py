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
    fish = Fish(romaji = "")
    for line in lines:
        split_line = line.strip().split(": ")
        if len(split_line) != 2:
            raise Exception("Fish with malformed field specification in line " + line)
        field, data = split_line
        if field == "name":
            fish.romaji = data
            fish.kana = romkan.to_kana(data)
        elif field == "rarity":
            fish.rarity = int(data)
        elif field == "takatsu":
            fish.location.set_takatsu(map(string_to_location, data.split(", ")))
        elif field =="masuda":
            fish.location.set_masuda(map(string_to_location, data.split(', ')))
        else:
            raise Exception("Unrecognized field in line " + line)
    if fish.romaji == "":
        raise Exception("Fish generated from string " + fish_string + " lacks a name field.")
    return fish

defaults = generate_defaults()
unseen_fish = set(defaults.keys())
parsed_fish = map(parse_fish, fish_data())
for fish in parsed_fish:
    unseen_fish.remove(fish.romaji)
    defaults[fish.romaji] = fish

if len(unseen_fish) > 0:
    print "The following fish did not have date specified in fish_data.txt:"
    as_list = list(unseen_fish)
    as_list.sort()
    for fish in as_list:
        print fish

final_fish_list = defaults.values()
final_fish_list.sort(key = lambda fish: fish.romaji)
