library plant;

part 'plant_list.dart';

class Plant {

  String latin;
  String ka;
  String zoku;
  String romaji;
  String kana;
  int rarity;
  int saitei;
  int saikou;
  List<String> iro;

  Plant(this.latin, this.ka, this.zoku, this.romaji, this.kana, this.rarity, this.saitei, this.saikou, this.iro) {
  }

}
