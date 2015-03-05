import 'dart:html';
import '../fish.dart';
import 'dart:async';

BodyElement body = document.querySelector("body");
List<String> images = getBackgroundImages();
int currentImage = 1;

main() {
  if (window.screen.width > 700 && images.length > 1) {
    window.onResize.listen((e) {
      if (window.innerWidth < 700) {
        body.style.backgroundImage = "none";
      } else {
        body.style.backgroundImage = "url(" + images[currentImage] + ")";
      }
    });
    Timer timer = new Timer.periodic(new Duration(seconds: 15), (t) {
      if (window.innerWidth >= 700) {
      body.style.backgroundImage = "url(" + images[currentImage] + ")";
      }
      currentImage += 1;
      if (currentImage >= images.length) {
        currentImage = 0;
      }
    });
  }
}


List<String> getBackgroundImages() {
  String fish_name = document.baseUri.split("/").last.replaceFirst(".html", "");
  print("Name: " + fish_name);
  Fish fish = fish_map[fish_name];
  print("Kana: " + fish.kana);
  return fish.backgroundImages();
}

