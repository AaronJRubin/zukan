import 'dart:html';
import 'plant.dart';
import 'package:takatsugawa_zukan/ichiran_utils.dart';

//ElementList<CheckboxInputElement> includeCheckboxes;
//ElementList<CheckboxInputElement> excludeCheckboxes;
TextInputElement articleSearch;
NumberInputElement heightSearch;
ElementList<LIElement> plantTiles;

void main() {
  setUpSearchAreaToggle();
  //includeCheckboxes = document.querySelectorAll(".search-checkbox.include");
  //excludeCheckboxes = document.querySelectorAll(".search-checkbox.exclude");
  articleSearch = document.querySelector("#article-search");
  heightSearch = document.querySelector("#height-search");
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
  articleSearch.onChange.listen((e) => refresh());
  articleSearch.onKeyUp.listen((e) => refresh());
  heightSearch.onChange.listen((e) => refresh());
  heightSearch.onKeyUp.listen((e) => refresh());
  refresh(); // maybe things were clicked before script was loaded
}

void toggleCheckboxChanged(CheckboxInputElement self, CheckboxInputElement partner) {
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
  String searchHeight = heightSearch.value.trim();
  if (searchHeight.length > 0) {
    int intVal = int.parse(searchHeight);
    filter.add((plant) => plant.saikou > intVal && plant.saitei < intVal);
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
