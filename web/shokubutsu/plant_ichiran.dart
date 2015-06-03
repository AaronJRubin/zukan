import 'dart:html';
import 'plant.dart';
import 'package:takatsugawa_zukan/ichiran_utils.dart';

//ElementList<CheckboxInputElement> includeCheckboxes;
//ElementList<CheckboxInputElement> excludeCheckboxes;
TextInputElement articleSearch;
NumberInputElement kakiSearch;
ElementList<LIElement> plantTiles;
ElementList<RadioButtonInputElement> typeSearchBoxes;

void main() {
  setUpSearchAreaToggle();
  //includeCheckboxes = document.querySelectorAll(".search-checkbox.include");
  //excludeCheckboxes = document.querySelectorAll(".search-checkbox.exclude");
  articleSearch = document.querySelector("#article-search");
  kakiSearch = document.querySelector("#kaki-search");
  typeSearchBoxes = document.querySelectorAll("#type-search input");
  plantTiles = document.querySelectorAll("ol.tiles li");
  /*for (int i = 0; i < includeCheckboxes.length; i++) {
    CheckboxInputElement includeCheckbox = includeCheckboxes[i];
    CheckboxInputElement excludeCheckbox = excludeCheckboxes[i];
    includeCheckbox.onChange.listen((e) {
      toggleCheckboxChanged(includeCheckbox, excludeCheckbox);
    });
    excludeCheckbox.onChange.listen((e) {
      toggleCheckboxChanged(excludeCheckbox, includeCheckbox);
    });
  }*/
  textSearchListen(articleSearch);
  textSearchListen(kakiSearch);
  typeSearchBoxes.forEach((el) => el.onChange.listen((e) => refresh()));
  refresh(); // maybe things were clicked before script was loaded
}

void textSearchListen(InputElement field) {
  field.onChange.listen((e) => refresh());
  field.onKeyUp.listen((e) => refresh());
}

void toggleCheckboxChanged(
    CheckboxInputElement self, CheckboxInputElement partner) {
  if (self.checked) {
    if (partner.checked) {
      partner.checked = false;
    }
  }
  refresh();
}

Filter<Plant> buildFilter() {
  Filter<Plant> filter = new Filter<Plant>();
  String searchText = articleSearch.value.trim();
  /*if (searchText.length > 0) {
    filter
        .add((plant) => article_map[plant.romaji].text.contains(searchText));
  }*/
  String searchKaki = kakiSearch.value.trim();
  if (searchKaki.length > 0) {
    int intVal = int.parse(searchKaki);
    filter.add((plant) => plant.kaki.contains(intVal));
  }
  RadioButtonInputElement checkedTypeInput =
      typeSearchBoxes.firstWhere((el) => el.checked, orElse: () => null);
  if (checkedTypeInput != null && checkedTypeInput.value != 'all') {
    filter.add((plant) => plant.type == checkedTypeInput.value);
  }
  /*
  for (CheckboxInputElement checkbox in includeCheckboxes) {
    if (checkbox.checked) {
      String area = checkbox.id.split("-")[1];
      if (checkbox.id.startsWith("takatsu")) {
        filter.add((plant) => plant.takatsu.contains(area));
      } else if (checkbox.id.startsWith("masuda")) {
        filter.add((plant) => plant.masuda.contains(area));
      }
    }
  }
  for (CheckboxInputElement checkbox in excludeCheckboxes) {
    if (checkbox.checked) {
      String area = checkbox.id.split("-")[1];
      if (checkbox.id.startsWith("takatsu")) {
        filter.add((plant) => !plant.takatsu.contains(area));
      } else if (checkbox.id.startsWith("masuda")) {
        filter.add((plant) => !plant.masuda.contains(area));
      }
    }
  }*/
  return filter;
}

void refresh() {
  Filter filter = buildFilter();
  for (LIElement tile in plantTiles) {
    Plant plant = plant_map[tile.attributes["data-plant-name"]];
    if (!filter.filter(plant)) {
      tile.classes.add('hidden');
    } else {
      tile.classes.remove('hidden');
    }
  }
}
