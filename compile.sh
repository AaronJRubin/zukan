cd zukan_workspace

pub build

cd ..

mv site/static/takatsugawa-zukan.appcache site/takatsugawa-zukan.appcache

rm -r site/static/

cp -r zukan_workspace/build/web site/static/

mv site/takatsugawa-zukan.appcache site/static/takatsugawa-zukan.appcache