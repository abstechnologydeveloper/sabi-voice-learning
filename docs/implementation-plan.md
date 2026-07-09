# Sabi Voice Learning Backend Plan

## Objective

Build an open-source Python voice backend that AbS can use for Sabi Voice
Learning. The service should generate voice audio from teaching text and return
playable audio URLs.

## Boundary

This Python service does voice generation only.

It does not:

- Authenticate AbS users.
- Check AbS Plus entitlements.
- Read Studio materials.
- Generate lesson scripts.
- Manage Flutter/web UI.

Those responsibilities stay in the main AbS backend and clients.

## Integration Contract

AbS backend calls:

```http
POST {SABI_VOICE_API_URL}/v1/tts
Authorization: Bearer {SABI_VOICE_API_KEY}
```

Request:

```json
{
  "text": "Teaching transcript for one segment.",
  "language": "yo",
  "voiceId": "sabi_female_yo_01",
  "format": "mp3",
  "speed": 1.0,
  "metadata": {
    "studentId": "...",
    "studioJobId": "...",
    "segmentId": "segment-1"
  }
}
```

Response:

```json
{
  "audioUrl": "https://voice.example.com/audio/segment.mp3",
  "durationSeconds": 92,
  "format": "mp3",
  "voiceId": "sabi_female_yo_01",
  "provider": "sabi-custom",
  "status": "ready"
}
```

## Provider Roadmap

### Phase 1: Stub Provider

Returns valid short WAV files for end-to-end integration.

### Phase 2: Prototype Provider

Add the first local open-source model runtime. No hosted provider API should be
required for the production product.

### Phase 3: Sabi Custom Provider

Use consented Sabi voice recordings and trained/fine-tuned models.

## Storage Roadmap

### Phase 1

Local file storage for development.

### Phase 2

AbS backend upload adapter for production. The Python service posts generated
audio to the AbS backend public file upload endpoint, then returns the public
R2/S3 URL from that response.

### Open Source Storage

Storage is automatic:

- If `SABI_VOICE_BACKEND_BASE_URL` is set, audio is uploaded to
  `{baseUrl}/api/v1/public-files-upload` and the returned public URL is used.
- If it is not set, local development storage serves `/audio/{fileName}` from
  disk.

Open-source users can expose the same multipart upload route on their own
backend.

The client response stays stable:

```json
{
  "audioUrl": "https://public-storage.example.com/uploads/file.wav"
}
```

## Production Requirements

- API key auth.
- Rate limiting at reverse proxy/API gateway.
- GPU worker isolation.
- Per-request max text length.
- Structured logs.
- Segment-level failure handling.
- Voice/model version in response metadata.
