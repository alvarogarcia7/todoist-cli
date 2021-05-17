#!/bin/bash

set -euxo pipefail

source ./keys.sh

source ./functions.sh

download_GET "all_tasks.json" "https://api.todoist.com/rest/v1/tasks"