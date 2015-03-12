#!/usr/bin/env python

import romkan
import os
import sys
import cPickle as pickle
from fish import Fish, Location

def generate_defaults():
    res = {}
    fish_image_folders = next(os.walk('web/images/sakana'))[1]
    for fish_image_folder in fish_image_folders:
        kana = romkan.to_kana(fish_image_folder)#.decode("utf-8")
        res[fish_image_folder] = Fish(romaji = fish_image_folder, kana = kana)
    return res

def fish_data():
    f = open("fish_data.txt", "r")
    return f.read().split("\n\n")

def string_to_location(string):
    string = string.strip().lower()
    if string == "zyou" or string == "jou":
      return Location.ZYOU
    if string == "tyuu" or string == "chuu":
      return Location.CHUU
    if string == "ge":
      return Location.GE 
    if string == "kakou" or string == "ka":
      return Location.KAKOU
    raise Exception("Invalid location: " + string)

def clean_romaji(romaji):
    romaji = romaji.replace("zy", "j")
    romaji = romaji.replace("si", "shi")
    return romaji

def parse_fish(fish_string):
    lines = fish_string.split('\n')
    fish = Fish(romaji = "")
    for line in lines:
        try:
            line = line.decode('utf-8')
        except Exception:
            pass
        split_line = line.strip().lower().split(":")
        if len(split_line) != 2:
            raise Exception("Fish with malformed field specification in line " + line)
        field, data = split_line
        field = field.strip()
        data = data.strip()
        if field == "name":
            fish.romaji = clean_romaji(data)
            fish.kana = romkan.to_kana(data)
        elif field == "latin" or field == "gakumei":
            fish.latin = data
        elif field == "rarity":
            fish.rarity = int(data)
        elif field == "genus" or field == "zoku":
            fish.genus = data
        elif field == "family" or field == "ka":
            fish.family = data
        elif field == "takatsu" or field == "takatu":
            fish.location.set_takatsu(map(string_to_location, filter(lambda string: len(string.strip()) > 0, data.split(","))))
        elif field =="masuda":
            fish.location.set_masuda(map(string_to_location, filter(lambda string: len(string.strip()) > 0, data.split(","))))
        else:
            raise Exception("Unrecognized field in line " + line)
    if fish.romaji == "":
        raise Exception("Fish generated from string " + fish_string + " lacks a name field.")
    return fish

defaults = generate_defaults()
unseen_fish = set(defaults.keys())
parsed_fish = map(parse_fish, fish_data())
for fish in parsed_fish:
    if fish.romaji in unseen_fish:
        unseen_fish.remove(fish.romaji)
    else:
        print("The following fish lacks an image, or has data specified twice: " + fish.romaji)
    defaults[fish.romaji] = fish

if len(unseen_fish) > 0:
    print "The following fish did not have data specified in fish_data.txt:"
    as_list = list(unseen_fish)
    as_list.sort()
    for fish in as_list:
        print fish

final_fish_list = defaults.values()
final_fish_list.sort(key = lambda fish: fish.romaji)

pickle.dump(final_fish_list, open("fish_list.pkl", "wb", pickle.HIGHEST_PROTOCOL))

def write_dart(fish_list):
    f = file("web/fish_list.dart", "w");
    f.write("part of fish;\n\n")
    f.write("List<Fish> fish_list = [")
    for fish in fish_list:
        fishString = u"""new Fish("%s", "%s", "%s", "%s", "%s",
            %d, %s, %s, %s, %s, %s, %s, %s, %s)""" % (fish.latin, fish.family,
            fish.genus, fish.romaji, fish.kana, fish.rarity, fish.takatsu_zyou(),
            fish.takatsu_chuu(), fish.takatsu_ge(), fish.takatsu_kakou(), fish.masuda_zyou(),
            fish.masuda_chuu(), fish.masuda_ge(), fish.masuda_kakou())
        fishString = fishString.replace('True', 'true')
        fishString = fishString.replace('False', 'false')
        f.write(fishString.encode('utf8'))
        f.write(",\n")
    f.write("];\n\n")
    f.write("""Map<String, Fish> fish_map = new Map.fromIterable(fish_list,
    key: (fish) => fish.romaji);""")
    f.close()

write_dart(final_fish_list)
