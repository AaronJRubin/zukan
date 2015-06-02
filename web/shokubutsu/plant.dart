library plant;

part 'plant_list.dart';

class Plant {

  String latin;
  String romaji;
  String kana;
  String type;
  List<String> seiikubasho;
  List<String> bunpu;
  List<int> kaki;
  String ganpenType;

  Plant({this.latin, this.romaji, this.kana, this.type, this.seiikubasho, this.bunpu, this.kaki, this.ganpenType: null}) {
  }

}
