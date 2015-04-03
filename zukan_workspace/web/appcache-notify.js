var appcache = window.applicationCache;

appcache.addEventListener("downloading", function(event) {
		var notifications = document.querySelector("#appcache-notifications");	
		notifications.innerHTML = 'キャッシュ更新中！しばらくこのページに残ってください。<span id="downloaded">0</span>/244ダウンロード済み。';
		notifications.classList.toggle("displayed");
		var filesDownloaded = 0;
		var downloaded = document.querySelector("#downloaded");
		appcache.addEventListener("progress", function(event) {
			filesDownloaded += 1;
			downloaded.innerHTML = filesDownloaded;
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