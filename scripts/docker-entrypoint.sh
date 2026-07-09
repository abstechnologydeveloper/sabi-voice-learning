#!/usr/bin/env bash
set -euo pipefail

if [[ "${SABI_VOICE_DOWNLOAD_MODELS:-true}" == "true" ]]; then
  /app/scripts/download-kokoro-models.sh
fi

exec "$@"
