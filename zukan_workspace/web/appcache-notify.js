var appcache = window.applicationCache;
appcache.addEventListener("downloading", function () {
    "use strict";
    var notifications = document.querySelector("#appcache-notifications");
    notifications.innerHTML = 'キャッシュ更新中！しばらくこのページに残ってください。<span id="progress"></span>';
    notifications.classList.toggle("displayed");
    var progress = document.querySelector("#progress");
    var downloaded, total;
    appcache.addEventListener("progress", function (event) {
        if (event.total !== undefined) {
            if (downloaded === undefined) {
                progress.innerHTML = '<span id="downloaded">0</span>/<span id="total">349</span>ダウンロード済み。';
                downloaded = document.querySelector("#downloaded");
                total = document.querySelector("#total");
                console.log(downloaded);
                console.log(total);
            }
            downloaded.innerHTML = event.loaded;
            total.innerHTML = event.total;
        }
    });
    var finish = function () {
        notifications.classList.toggle("finished");
    };
    var updated = function () {
        notifications.innerHTML = "キャッシュされました！変わったサイトを見るためにこのページをリフレッシュしてください。";
        finish();
    };
    var cached = function () {
        notifications.innerHTML = "キャッシュされました！オフラインでもアクセス出来るようになりました。";
        finish();
    };
    appcache.addEventListener("updateready", updated);
    appcache.addEventListener("cached", cached);
});
