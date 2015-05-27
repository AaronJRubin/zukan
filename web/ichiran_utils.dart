library ichiran_utils;

import 'dart:html';

typedef bool FilterFunction<T>(T thing);

class Filter<T> {
  List<FilterFunction> filterFunctions = [];

  Filter();
  bool filter(T thing) {
    return filterFunctions.map((function) => function(thing)).fold(
        true, (bool1, bool2) => bool1 && bool2);
  }

  void add(FilterFunction func) {
    filterFunctions.add(func);
  }
}

void setUpSearchAreaToggle() {
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
}