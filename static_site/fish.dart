library fish;

part 'fish_list.dart';

abstract class RiverHabitat {

  bool up;
  bool central;
  bool down;
  bool mouth;

  String _constructURL(String area);

  List<String> backgroundImages() {
    List<String> res = [];
      if (up) {
        res.add(_constructURL("up"));
      }
      if (central) {
          res.add(_constructURL("central"));
       }
      if (down) {
        res.add(_constructURL("down"));
      }
      if (mouth) {
        res.add(_constructURL("mouth"));
      }
      return res;
  }
}

class Takatsu extends RiverHabitat {

  Takatsu(bool up, bool central, bool down, bool mouth) {
   this.up = up;
   this.central = central;
   this.down = down;
   this.mouth = mouth;
  }

  String _constructURL(String area) {
    return "takatsu-" + area + ".jpg";
  }

}

class Masuda extends RiverHabitat {

  Masuda(bool up, bool central, bool down, bool mouth) {
   this.up = up;
   this.central = central;
   this.down = down;
   this.mouth = mouth;
  }

  String _constructURL(String area) {
    return "masuda-" + area + ".jpg";
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

  Fish(this.scientific, this.family, this.genus, this.romaji, this.kana, this.rarity,
      bool takatsu_up, bool takatsu_central, bool takatsu_down, bool takatsu_mouth,
      bool masuda_up, bool masuda_central, bool masuda_down, bool masuda_mouth);

}