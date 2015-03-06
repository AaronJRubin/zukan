import 'dart:html';
import 'fish.dart';

List<CheckboxInputElement> includeCheckboxes;
List<CheckboxInputElement> excludeCheckboxes;
List<DivElement> fishTiles;

/*checkbox.onClick.listen((e) {
      if (ch.classes.contains("selected")) {
        button.classes.remove("selected");
        button.classes.add("unselected");
      } else if (button.classes.contains("unselected")) {
        button.classes.remove("unselected");
        button.classes.add("selected");
      }*/

void main() {
  includeCheckboxes = document.querySelectorAll("#include .search-checkbox");
  excludeCheckboxes = document.querySelectorAll("#exclude .search-checkbox");
  fishTiles = document.querySelectorAll(".fish-tile");
  for (CheckboxInputElement checkbox in new List.from(includeCheckboxes)..addAll(excludeCheckboxes)) {
    checkbox.onChange.listen((e) => refresh());
  }
}

typedef bool FilterFunction(Fish fish);

class Filter {

  List<FilterFunction> filterFunctions = [];

  Filter();
  bool filter(Fish fish) {
    return filterFunctions.map((function) => function(fish)).fold(true, (bool1, bool2) => bool1 && bool2);
  }

  void add(FilterFunction func) {
    filterFunctions.add(func);
  }
}

Filter buildFilter() {
  Filter filter = new Filter();
  for (CheckboxInputElement checkbox in includeCheckboxes) {
    if (checkbox.checked) {
      String area = checkbox.id.split("-")[1];
      if (checkbox.id.startsWith("takatsu")) {
        filter.add((fish) => fish.takatsu.contains(area));
      } else if (checkbox.id.startsWith("masuda")) {
        filter.add((fish) => fish.masuda.contains(area));
      }
    }
  }
  for (CheckboxInputElement checkbox in excludeCheckboxes) {
    if (checkbox.checked) {
      String area = checkbox.id.split("-")[1];
      if (checkbox.id.startsWith("takatsu")) {
        filter.add((fish) => !fish.takatsu.contains(area));
      } else if (checkbox.id.startsWith("masuda")) {
        filter.add((fish) => !fish.masuda.contains(area));
      }
    }
  }
  return filter;
}

void refresh() {
  Filter filter = buildFilter();
  for (DivElement tile in fishTiles) {
    Fish fish = fish_map[tile.attributes["data-fishname"]];
    if (!filter.filter(fish)) {
      tile.hidden = true;
    } else {
      tile.hidden = false;
    }
  }
}
