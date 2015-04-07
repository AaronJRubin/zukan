import 'dart:html';
import '../fish.dart';
import 'dart:async';



main() {
  String fish_name = document.baseUri.split("/").last.replaceFirst(".html", "");
  Fish fish = fish_map[fish_name];
  List<String> imageClasses = fish.backgroundImageClasses();
  if (window.screen.width > 700 && imageClasses.length > 1) {
    List<String> backgroundImages = fish.backgroundImages();
    for (String backgroundImage in backgroundImages) {
      new ImageElement(src: backgroundImage); // preload background images
    }
    BodyElement body = document.querySelector("body");
    int currentImageClass = 0;
    Timer timer = new Timer.periodic(new Duration(seconds: 10), (t) {
      body.classes.remove(imageClasses[currentImageClass]);
      currentImageClass = (currentImageClass + 1) % imageClasses.length;
      body.classes.add(imageClasses[currentImageClass]);
    });
  }
}
