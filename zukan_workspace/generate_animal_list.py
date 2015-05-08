#!/usr/bin/env python
# This script is called appropriately by the Rakefile; do not execute it directly, but feel free to edit it.

import romkan
import os
import sys
import cPickle as pickle
from animal import Animal, Location

def generate_defaults():
    res = {}
    animal_image_folders = next(os.walk('master-images/ikimono'))[1]
    for animal_image_folder in animal_image_folders:
        kana = romkan.to_kana(animal_image_folder)
        res[animal_image_folder] = Animal(romaji = animal_image_folder, kana = kana)
    return res

def animal_data():
    f = open("animal_data.txt", "r")
    return f.read().strip().split("\n\n")

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

def parse_animal(animal_string):
    lines = animal_string.split('\n')
    animal = Animal(romaji = "")
    for line in lines:
        try:
            line = line.decode('utf-8')
        except Exception:
            pass
        split_line = line.strip().split(":")
        if len(split_line) != 2:
            continue
            #raise Exception("Animal, " + str(lines) + " with malformed field specification in line " + line)
        field, data = split_line
        field = field.strip()
        data = data.strip()
        if field == "name":
            animal.romaji = clean_romaji(data)
            animal.kana = romkan.to_kana(data)
        elif field == "latin" or field == "gakumei":
            animal.latin = data
        elif field == "rarity":
            animal.rarity = int(data)
        elif field == "genus" or field == "zoku":
            animal.genus = data
        elif field == "family" or field == "ka":
            animal.family = data
        elif field == "takatsu" or field == "takatu":
            animal.location.set_takatsu(map(string_to_location, filter(lambda string: len(string.strip()) > 0, data.split(","))))
        elif field =="masuda":
            animal.location.set_masuda(map(string_to_location, filter(lambda string: len(string.strip()) > 0, data.split(","))))
        else:
            raise Exception("Unrecognized field in line " + line)
    if animal.romaji == "":
        raise Exception("Animal generated from string " + animal_string + " lacks a name field.")
    return animal

defaults = generate_defaults()
unseen_animals = set(defaults.keys())
parsed_animals = map(parse_animal, animal_data())
for animal in parsed_animals:
    if animal.romaji in unseen_animals:
        unseen_animals.remove(animal.romaji)
    else:
        print("The following animal lacks an image, or has data specified twice: " + animal.romaji)
    defaults[animal.romaji] = animal

if len(unseen_animals) > 0:
    print "The following animal did not have data specified in animal_data.txt:"
    as_list = list(unseen_animals)
    as_list.sort()
    for animal in as_list:
        print animal

final_animal_list = defaults.values()
final_animal_list.sort(key = lambda animal: animal.kana)

pickle.dump(final_animal_list, open("animal_list.pkl", "wb", pickle.HIGHEST_PROTOCOL))

def write_dart(animal_list):
    f = file("web/animal_list.dart", "w");
    f.write("part of animal;\n\n")
    f.write("List<Animal> animal_list = [")
    for animal in animal_list:
        animalString = u"""new Animal("%s", "%s", "%s", "%s", "%s",
            %d, %s, %s, %s, %s, %s, %s, %s, %s)""" % (animal.latin, animal.family,
            animal.genus, animal.romaji, animal.kana, animal.rarity, animal.takatsu_zyou(),
            animal.takatsu_chuu(), animal.takatsu_ge(), animal.takatsu_kakou(), animal.masuda_zyou(),
            animal.masuda_chuu(), animal.masuda_ge(), animal.masuda_kakou())
        animalString = animalString.replace('True', 'true')
        animalString = animalString.replace('False', 'false')
        f.write(animalString.encode('utf8'))
        f.write(",\n")
    f.write("];\n\n")
    f.write("""Map<String, Animal> animal_map = new Map.fromIterable(animal_list,
    key: (animal) => animal.romaji);""")
    f.close()

write_dart(final_animal_list)
