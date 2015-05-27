library animal;

part 'animal_list.dart';

class RiverHabitat {

  bool zyou;
  bool chuu;
  bool ge;
  bool kakou;
  String name;

  RiverHabitat(this.zyou, this.chuu, this.ge, this.kakou, this.name) {
    this.zyou = zyou;
    this.chuu = chuu;
    this.ge = ge;
    this.kakou = kakou;
  }

  bool contains(String habitat) {
    switch (habitat) {
      case "zyou":
        return zyou;
      case "chuu":
        return chuu;
      case "ge":
        return ge;
      case "kakou":
        return kakou;
      default:
        print("Error: a non-existing habitat was searched for, with string " + habitat);
        return false;
    }
  }

}

class Animal {

  String scientific;
  String family;
  String genus;
  String romaji;
  String kana;
  int rarity;
  RiverHabitat takatsu;
  RiverHabitat masuda;

  Animal(this.scientific, this.family, this.genus, this.romaji, this.kana, this.rarity, bool takatsu_up, bool takatsu_central, bool takatsu_down, bool takatsu_mouth, bool masuda_up, bool masuda_central, bool masuda_down, bool masuda_mouth) {
    this.takatsu = new RiverHabitat(takatsu_up, takatsu_central, takatsu_down, takatsu_mouth, "takatsu");
    this.masuda = new RiverHabitat(masuda_up, masuda_central, masuda_down, masuda_mouth, "masuda");
  }

}
