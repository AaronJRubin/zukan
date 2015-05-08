import 'dart:html';
import 'animal.dart';
import 'article.dart';

ElementList<CheckboxInputElement> includeCheckboxes;
ElementList<CheckboxInputElement> excludeCheckboxes;
TextInputElement articleSearch;
ElementList<LIElement> animalTiles;

void main() {
  includeCheckboxes = document.querySelectorAll("#include .search-checkbox");
  excludeCheckboxes = document.querySelectorAll("#exclude .search-checkbox");
  articleSearch = document.querySelector("#article-search");
  animalTiles = document.querySelectorAll("ol.animal-tiles li");
  SpanElement dropdownCaret = document.querySelector("#dropdown-caret");
  DivElement searchArea = document.querySelector("#search-area");
  SpanElement dropdownLabel = document.querySelector("#dropdown-label");
  dropdownCaret.onClick.listen((e) {
    searchArea.classes.toggle("collapsed");
    dropdownCaret.classes.toggle("collapsed");
    if (searchArea.classes.contains("collapsed")) {
      dropdownLabel.text = "検索エリアを表示";
    } else {
      dropdownLabel.text = "検索エリアを隠す";
    }
  });
  for (CheckboxInputElement checkbox in new List.from(includeCheckboxes)..addAll(excludeCheckboxes)) {
    checkbox.onChange.listen((e) => refresh());
  }
  articleSearch.onChange.listen((e) => refresh());
  articleSearch.onKeyUp.listen((e) => refresh());
  refresh(); // maybe things were clicked before script was loaded
}

typedef bool FilterFunction(Animal animal);

class Filter {

  List<FilterFunction> filterFunctions = [];

  Filter();
  bool filter(Animal animal) {
    return filterFunctions.map((function) => function(animal)).fold(true, (bool1, bool2) => bool1 && bool2);
  }

  void add(FilterFunction func) {
    filterFunctions.add(func);
  }
}

Filter buildFilter() {
  Filter filter = new Filter();
  String searchText = articleSearch.value.trim();
  if (searchText.length > 0) {
    filter.add((animal) => article_map[animal.romaji].text.contains(searchText));
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
