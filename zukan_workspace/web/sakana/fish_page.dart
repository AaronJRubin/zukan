import 'dart:html';
import '../fish.dart';
import 'dart:async';

BodyElement body = document.querySelector("body");
List<String> imageClasses = getBackgroundImages();
int currentImageClass = 0;

main() {
  if (window.screen.width > 700 && imageClasses.length > 1) {
    Timer timer = new Timer.periodic(new Duration(seconds: 10), (t) {
      body.classes.remove(imageClasses[currentImageClass]);
      currentImageClass = (currentImageClass + 1) % imageClasses.length;
      body.classes.add(imageClasses[currentImageClass]);
    });
  }
}

List<String> getBackgroundImages() {
  String fish_name = document.baseUri.split("/").last.replaceFirst(".html", "");
  Fish fish = fish_map[fish_name];
  return fish.backgroundImageClasses();
}

