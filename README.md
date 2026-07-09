# Sabi Voice Service

Sabi Voice Service is the open-source Python backend for Sabi Voice Learning.
It receives teaching text, generates audio with a local voice engine, uploads
the audio through a backend file endpoint, and returns a playable URL.

This service is intentionally separate from the main AbS Node backend.

## Features

- FastAPI HTTP service.
- API-key protected TTS endpoint.
- Local `kokoro-onnx` voice provider by default.
- Optional `stub` provider for integration tests.
- Backend upload storage for R2/S3-backed public URLs.
- Local file storage fallback when no backend URL is configured.

## Project Layout

```text
app/
  api/          HTTP routes
  core/         configuration and API-key security
  providers/    voice engines
  storage/      local and backend upload storage
  main.py       FastAPI app factory
```

## API

Health:

```http
GET /health
```

Generate one speech segment:

```http
POST /v1/tts
Authorization: Bearer dev-secret-key
Content-Type: application/json
```

```json
{
  "text": "Today we will learn photosynthesis step by step.",
  "language": "en",
  "voiceId": "af_heart",
  "format": "wav",
  "speed": 1.0,
  "metadata": {
    "studioJobId": "job-id",
    "segmentId": "segment-1"
  }
}
```

Response:

```json
{
  "audioUrl": "https://public-storage.example.com/uploads/file.wav",
  "durationSeconds": 1.2,
  "format": "wav",
  "voiceId": "af_heart",
  "provider": "kokoro-onnx",
  "status": "ready"
}
```

## Configuration

Minimum config:

```text
SABI_VOICE_API_KEYS=dev-secret-key
SABI_VOICE_BACKEND_BASE_URL=https://backend.abstechconnect.com
```

When `SABI_VOICE_BACKEND_BASE_URL` is set, the service uploads generated audio
to:

```text
{SABI_VOICE_BACKEND_BASE_URL}/api/v1/public-files-upload
```

If no backend URL is configured, local development storage serves generated
files from `/audio/{fileName}`.

## Local Development

```bash
cd /Users/apple/Desktop/sabi-voice-service
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8095 --reload
```

Test:

```bash
curl -X POST http://localhost:8095/v1/tts \
  -H 'Authorization: Bearer dev-secret-key' \
  -H 'Content-Type: application/json' \
  -d '{"text":"Teach this material clearly.","language":"en","voiceId":"af_heart"}'
```

Place these files in `models/kokoro`:

```text
models/kokoro/kokoro-v1.0.onnx
models/kokoro/voices-v1.0.bin
```

Download them:

```bash
./scripts/download-kokoro-models.sh
```

Run:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8095
```

Kokoro ONNX voice IDs can be passed directly, for example `af_heart` or
`am_adam`. Unknown voice IDs fall back to `af_heart`.

## Docker Deployment

Build:

```bash
docker build -t sabi-voice-service .
```

Run with automatic model download:

```bash
docker run --rm -p 8095:8095 \
  -e SABI_VOICE_API_KEYS=your-secret-key \
  -e SABI_VOICE_BACKEND_BASE_URL=https://backend.abstechconnect.com \
  -v "$(pwd)/models:/app/models" \
  sabi-voice-service
```

The container downloads missing Kokoro model files into `/app/models/kokoro`.
Mounting `$(pwd)/models` keeps those files between container restarts.

To disable startup download and require pre-mounted model files:

```bash
docker run --rm -p 8095:8095 \
  -e SABI_VOICE_DOWNLOAD_MODELS=false \
  -e SABI_VOICE_API_KEYS=your-secret-key \
  -e SABI_VOICE_BACKEND_BASE_URL=https://backend.abstechconnect.com \
  -v "$(pwd)/models:/app/models" \
  sabi-voice-service
```

## Development Checks

```bash
pip install -r requirements.txt
pytest
ruff check .
```

## Product Boundary

Clients must not generate speech locally. Flutter and web only play `audioUrl`.
The main AbS backend owns user auth, premium gates, Studio jobs, material
extraction, lesson planning, and Sabi AI integration.
