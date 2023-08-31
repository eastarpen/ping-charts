#!/bin/bash


if [ ! -d "../server/src/" ]; then
  echo "../server/src do not exists."
  exit 1
fi

npm run build
rm ../server/src/static/ -r
rm ../server/src/templates/ -r
mkdir ../server/src/templates
mv ./dist/index.html ../server/src/templates/index.html
mv ./dist/ ../server/src/static/
