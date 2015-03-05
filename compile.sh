cd zukan_workspace

pub build

cd ..

rm -r site/static/

cp -r zukan_workspace/build/web site/static/