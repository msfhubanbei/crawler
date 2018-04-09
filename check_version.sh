#!/usr/bin/env bash
set -ex
base_url=$1

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

ultraVersion=`python ${SHELL_FOLDER}/../../canary_test/get_ultra_ui_version_ex.py ${base_url}`
echo $ultraVersion
