#!/bin/bash

set -euxo pipefail

function download_GET(){
  local file="$1"
  local url="$2"

  if [ -e "$file" ]; then
    echo "File $file exists"
  else
    curl -X GET \
      "$url" \
      -H "Authorization: Bearer $TODOIST_API_TOKEN" > "$file"
  fi
}