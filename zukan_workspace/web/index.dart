import 'dart:html';
import 'fish.dart';

List<ButtonElement> includeButtons;
List<ButtonElement> excludeButtons;
List<DivElement> fishTiles;

void main() {
  includeButtons = document.querySelectorAll("#include .search-button");
  excludeButtons = document.querySelectorAll("#exclude .search-button");
  fishTiles = document.querySelectorAll(".fish-tile");
  for (ButtonElement button in new List.from(includeButtons)..addAll(excludeButtons)) {
    button.onClick.listen((e) {
      if (button.classes.contains("selected")) {
        button.classes.remove("selected");
        button.classes.add("unselected");
      } else if (button.classes.contains("unselected")) {
        button.classes.remove("unselected");
        button.classes.add("selected");
      }
      refresh();
    });
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
  for (ButtonElement button in includeButtons) {
    if (button.classes.contains("selected")) {
      String area = button.id.split("-")[1];
      if (button.id.startsWith("takatsu")) {
        filter.add((fish) => fish.takatsu.contains(area));
      } else if (button.id.startsWith("masuda")) {
        filter.add((fish) => fish.masuda.contains(area));
      }
    }
  }
  for (ButtonElement button in excludeButtons) {
    if (button.classes.contains("selected")) {
      String area = button.id.split("-")[1];
      if (button.id.startsWith("takatsu")) {
        filter.add((fish) => !fish.takatsu.contains(area));
      } else if (button.id.startsWith("masuda")) {
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
