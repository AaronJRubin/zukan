var isChrome = navigator.userAgent.toLowerCase().indexOf('chrome') > -1;
var body = document.body;
var locations = body.getAttribute("data-locations").split(" ");
if (screen.width > 700 && locations.length > 1 && isChrome) { 
    var location_images = locations.map(function(location) {
        return "/images/seisokuchi/" + location + ".jpg";
    });
    location_images.forEach(function(location_image) {
        var img = new Image();
        img.src = location_image;
    });
    var currentLocation = 0;
    setInterval(function() {
        body.classList.remove(locations[currentLocation]);
        currentLocation = (currentLocation + 1) % locations.length;
        body.classList.add(locations[currentLocation]);
    }, 10000);
}
