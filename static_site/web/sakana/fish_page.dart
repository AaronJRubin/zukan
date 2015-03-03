import 'dart:html';
import '../fish.dart';
import 'dart:async';

BodyElement body = document.querySelector("body");
List<String> images = getBackgroundImages();
int currentImage = 0;

main() {
  if (window.screen.width > 700) {
    window.onResize.listen((e) {
      if (window.innerWidth < 700) {
        body.style.backgroundImage = "none";
      } else {
        body.style.backgroundImage = "url(" + images[currentImage] + ")";
      }
    });
    Timer timer = new Timer.periodic(new Duration(seconds: 5), (t) {
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
  Fish fish = fish_map[fish_name];
  return fish.backgroundImages();
}

