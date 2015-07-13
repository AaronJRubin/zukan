library plant;

part 'plant_list.dart';

class Plant {

  String latin;
  String romaji;
  String kana;
  String type;
  List<String> seiikubasho;
  List<String> bunpu;
  List<String> shokudoku;
  List<int> kaki;
  List<int> hanabiraKazu;
  String iro;
  String kishibeType;

  Plant({this.latin, this.romaji, this.kana, this.type, this.seiikubasho, this.bunpu, this.kaki, this.hanabiraKazu, this.iro, this.shokudoku, this.kishibeType: null}) {
  }

}
