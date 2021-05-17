#!/bin/bash

set -euxo pipefail

source ./keys.sh

source ./functions.sh


download_GET "all_projects.json" "https://api.todoist.com/rest/v1/projects"

