library fish;

part 'fish_list.dart';

class RiverHabitat {

  bool up;
  bool central;
  bool down;
  bool mouth;
  String name;

  RiverHabitat(this.up, this.central, this.down, this.mouth, this.name) {
    this.up = up;
    this.central = central;
    this.down = down;
    this.mouth = mouth;
  }

  List<String> backgroundImageClasses() {
    List<String> res = [];
    if (up) {
      res.add(name + "-zyou");
    }
    if (central) {
      res.add(name + "-chuu");
    }
    if (down) {
      res.add(name + "-ge");
    }
    if (mouth) {
      res.add(name + "-kakou");
    }
    return res;
  }
}

class Fish {

  String scientific;
  String family;
  String genus;
  String romaji;
  String kana;
  int rarity;
  RiverHabitat takatsu;
  RiverHabitat masuda;

  Fish(this.scientific, this.family, this.genus, this.romaji, this.kana, this.rarity, bool takatsu_up, bool takatsu_central, bool takatsu_down, bool takatsu_mouth, bool masuda_up, bool masuda_central, bool masuda_down, bool masuda_mouth) {
    this.takatsu = new RiverHabitat(takatsu_up, takatsu_central, takatsu_down, takatsu_mouth, "takatsu");
    this.masuda = new RiverHabitat(masuda_up, masuda_central, masuda_down, masuda_mouth, "masuda");
  }

  List<String> backgroundImageClasses() {
    return takatsu.backgroundImageClasses()..addAll(masuda.backgroundImageClasses());
  }

}
