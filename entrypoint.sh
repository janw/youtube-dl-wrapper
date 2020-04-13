#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

export PYTHONPATH=/src
cd /downloads

exec python3 -um youtube_dl_wrapper -c /config/config.yaml
