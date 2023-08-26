#!/bin/sh

ROOT_DIR=/usr/share/nginx/html

echo "Replacing env constants in JS"
for file in $ROOT_DIR/assets/*.js 
do
  echo "Processing $file ...";

  sed -i 's|VUE_APP_SERVER_URL|'${VUE_APP_SERVER_URL}'|g' $file

done
echo "Starting Nginx"
nginx -g 'daemon off;'