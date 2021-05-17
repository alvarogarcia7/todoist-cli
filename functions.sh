#!/bin/bash

set -euxo pipefail

function download_GET(){
  local file="$1"
  local url="$2"

  curl -X GET \
    "$url" \
    -H "Authorization: Bearer $TODOIST_API_TOKEN" > "$file"
}