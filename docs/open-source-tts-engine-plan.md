# Open Source TTS Engine Plan

## Direction

Sabi Voice should not depend on hosted provider APIs. We can use open-source
voice engines locally inside the Python service, then later replace or
fine-tune them with Sabi-owned models.

This is not an experiment path for production. Production uses one approved
runtime at a time, with explicit model files, pinned dependencies, and a license
record.

The public API remains stable:

```text
POST /v1/tts
```

The engine behind it can change:

```text
stub -> kokoro-onnx -> sabi-custom
```

Research adapters should live outside this production service until quality,
cost, and licensing pass review.

## Engine Shortlist

### 1. Kokoro ONNX

Use case:

- Production English/Nigerian-English baseline.
- Explicit local model files.
- Smaller deployment surface than PyTorch.

Pros:

- Open-weight TTS model.
- Small 82M parameter model.
- Fast and cost-efficient.

Risks:

- Local Nigerian language support may be limited.
- Need quality testing for Nigerian-accented English and Pidgin.

### 2. Piper

Use case:

- Future separate adapter if a CPU fallback is needed.

Pros:

- Fast local neural TTS.
- MIT-licensed project.
- Easy to deploy.

Risks:

- Voice model licenses vary by training source.
- Not designed for expressive teaching or voice cloning.
- Local Nigerian language voices may not exist.

### 3. F5-TTS

Use case:

- Future training/research path for Sabi-owned voices.

Pros:

- MIT-licensed code.
- Zero-shot style workflow.
- Good community interest.
- Supports expressive speech and code-switching in published materials.

Risks:

- GPU requirement.
- Need model/license review for exact checkpoints.
- Needs careful safety controls for voice cloning.

### 4. StyleTTS2

Use case:

- Future training/research path for high-quality Sabi voices.

Pros:

- MIT-licensed code.
- Strong research quality.
- Good candidate for custom voice experiments.

Risks:

- More engineering effort than a plug-and-play runtime.
- Needs clean training data and GPU.

### 5. Meta MMS TTS

Use case:

- Research only unless licensing allows production.
- Useful for low-resource language experiments.

Pros:

- Very broad language coverage.
- Public docs describe TTS support across 1,100+ languages.

Risks:

- MMS checkpoints are commonly listed as CC BY-NC 4.0.
- Non-commercial license is not suitable for premium AbS production without
  separate permission.

### Avoid For Production Without License Review

- XTTS-v2 pretrained weights: model license has commercial-use concerns.
- Any voice checkpoint trained on unclear/restricted data.
- Any voice clone without speaker consent.

## Recommended Build Order

### Phase 1: Keep Stub Provider

Already implemented.

Purpose:

- Backend integration.
- Flutter/web playback.
- Studio job result format.

### Phase 2: Add Kokoro ONNX Adapter

Purpose:

- Production local open-source speech generation.
- Start with English/Pidgin-like teaching scripts.

Adapter:

```text
app/providers/kokoro_onnx.py
```

Config:

```text
provider defaults to kokoro-onnx
```

### Phase 3: Sabi Custom

Purpose:

- Train/fine-tune our own voices.
- Support English, Pidgin, Yoruba, Hausa, and Igbo.

## Open Source Rules

To win with the community:

- Keep the service provider-neutral.
- Do not bundle restricted model weights.
- Add `MODEL_LICENSES.md`.
- Add model manifest support:

```json
{
  "provider": "kokoro",
  "model": "Kokoro-82M",
  "modelLicense": "Apache-2.0",
  "voices": [
    {
      "id": "af_heart",
      "language": "en",
      "license": "Apache-2.0"
    }
  ]
}
```

- Ship example integrations.
- Ship consent templates for custom voice training.
- Ship dataset preparation tools.
- Keep AbS product logic outside the open-source voice service.

## AbS Product Rule

The open-source voice engine only speaks the lesson. The AbS backend still owns:

- Premium access.
- Studio material extraction.
- Lesson planning.
- STEM step verification.
- Student progress.
- Flutter/web playback experience.
