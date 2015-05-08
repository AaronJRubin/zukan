import 'dart:html';
import '../animal.dart';
import 'dart:async';
import 'package:browser_detect/browser_detect.dart';

main() {
  String animal_name = document.baseUri.split("/").last.replaceFirst(".html", "");
  Animal animal = animal_map[animal_name];
  List<String> imageClasses = animal.backgroundImageClasses();
  if (window.screen.width > 700 && imageClasses.length > 1 && browser.isChrome) {
    List<String> backgroundImages = animal.backgroundImages();
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
