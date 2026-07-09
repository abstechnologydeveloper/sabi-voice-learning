#!/usr/bin/env bash
set -euo pipefail

MODEL_DIR="${SABI_VOICE_MODEL_DIR:-models/kokoro}"
BASE_URL="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"

mkdir -p "$MODEL_DIR"

download_file() {
  local name="$1"
  local url="$BASE_URL/$name"
  local output="$MODEL_DIR/$name"

  if [[ -s "$output" ]]; then
    echo "Already exists: $output"
    return
  fi

  echo "Downloading $name..."
  curl -L --fail --progress-bar "$url" -o "$output"
}

download_file "kokoro-v1.0.onnx"
download_file "voices-v1.0.bin"

echo
echo "Kokoro model files are ready in $MODEL_DIR"
