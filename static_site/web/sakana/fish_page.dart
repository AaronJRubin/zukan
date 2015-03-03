import 'dart:html';

main() {
  print("Hello from dart!");
  String fish_name = document.baseUri.split("/").last.replaceFirst(".html", "");
  print("My name is " + fish_name);
}