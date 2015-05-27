import 'dart:html';
import 'animal.dart';
import 'article.dart';
import 'ichiran_utils.dart';

ElementList<CheckboxInputElement> includeCheckboxes;
ElementList<CheckboxInputElement> excludeCheckboxes;
TextInputElement articleSearch;
ElementList<LIElement> animalTiles;

void main() {
  setUpSearchAreaToggle();
  includeCheckboxes = document.querySelectorAll(".search-checkbox.include");
  excludeCheckboxes = document.querySelectorAll(".search-checkbox.exclude");
  articleSearch = document.querySelector("#article-search");
  animalTiles = document.querySelectorAll("ol.tiles li");
  for (int i = 0; i < includeCheckboxes.length; i++) {
    CheckboxInputElement includeCheckbox = includeCheckboxes[i];
    CheckboxInputElement excludeCheckbox = excludeCheckboxes[i];
    includeCheckbox.onChange.listen((e) {
      toggleCheckboxChanged(includeCheckbox, excludeCheckbox);
    });
    excludeCheckbox.onChange.listen((e) {
      toggleCheckboxChanged(excludeCheckbox, includeCheckbox);
    });
  }
  articleSearch.onChange.listen((e) => refresh());
  articleSearch.onKeyUp.listen((e) => refresh());
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

Filter<Animal> buildFilter() {
  Filter<Animal> filter = new Filter<Animal>();
  String searchText = articleSearch.value.trim();
  if (searchText.length > 0) {
    filter
        .add((animal) => article_map[animal.romaji].text.contains(searchText));
  }
  for (CheckboxInputElement checkbox in includeCheckboxes) {
    if (checkbox.checked) {
      String area = checkbox.id.split("-")[1];
      if (checkbox.id.startsWith("takatsu")) {
        filter.add((animal) => animal.takatsu.contains(area));
      } else if (checkbox.id.startsWith("masuda")) {
        filter.add((animal) => animal.masuda.contains(area));
      }
    }
  }
  for (CheckboxInputElement checkbox in excludeCheckboxes) {
    if (checkbox.checked) {
      String area = checkbox.id.split("-")[1];
      if (checkbox.id.startsWith("takatsu")) {
        filter.add((animal) => !animal.takatsu.contains(area));
      } else if (checkbox.id.startsWith("masuda")) {
        filter.add((animal) => !animal.masuda.contains(area));
      }
    }
  }
  return filter;
}

void refresh() {
  Filter filter = buildFilter();
  for (LIElement tile in animalTiles) {
    Animal animal = animal_map[tile.attributes["data-animal-name"]];
    if (!filter.filter(animal)) {
      tile.classes.add('hidden');
    } else {
      tile.classes.remove('hidden');
    }
  }
}
