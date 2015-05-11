var appcache = window.applicationCache;

appcache.addEventListener("downloading", function(event) {
    var notifications = document.querySelector("#appcache-notifications");	
    notifications.innerHTML = 'キャッシュ更新中！しばらくこのページに残ってください。<span id="downloaded">0</span>/<span id="total">350</span>ダウンロード済み。';
    notifications.classList.toggle("displayed");
    var currentTotal = 244;
    var downloaded = document.querySelector("#downloaded");
    var total = document.querySelector("#total");
    appcache.addEventListener("progress", function(event) {
        if (currentTotal != event.total) {
            currentTotal = event.total;
            total.innerHTML = currentTotal;
        }
        downloaded.innerHTML = event.loaded;
    });
    updated = function(event) {
        notifications.innerHTML = "キャッシュされました！変わったサイトを見るためにこのページをリフレッシュしてください。";
        notifications.classList.toggle("finished");
    }
    cached = function(event) {
        notifications.innerHTML = "キャッシュされました！オフラインでもアクセス出来るようになりました。";
        notifications.classList.toggle("finished");
    }
    appcache.addEventListener("updateready", updated);
    appcache.addEventListener("cached", cached);
});
