#!/bin/bash


if [ ! -d "../server/src/" ]; then
  echo "../server/src do not exists."
  exit 1
fi

npm install
npm run build

rm ../server/src/static/ -rf
rm ../server/src/templates/ -rf
mkdir ../server/src/templates
mv ./dist/index.html ../server/src/templates/index.html
mv ./dist/ ../server/src/static/
