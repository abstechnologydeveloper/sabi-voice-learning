# YarnGPT Research And Sabi Voice Open Source Strategy

## Why YarnGPT Matters

YarnGPT proves there is real demand for Nigerian and African-localized voice AI.
Its public materials show a text-to-speech approach focused on Nigerian-accented
English and Nigerian languages. Recent acquisition news also validates the
commercial interest in local-language voice infrastructure.

Sabi Voice should learn from YarnGPT, but should not use YarnGPT or any external
provider as the production dependency. Our goal is to build an open-source
learning voice layer and a Sabi-owned voice engine.

## What YarnGPT Appears To Do

Public YarnGPT materials describe:

- Nigerian-accented text-to-speech.
- Pure language-modeling approach without external adapters.
- Audio tokenization/decoding through WavTokenizer.
- Hugging Face causal language model generation.
- 24kHz output.
- Preset voices.
- Nigerian/local-language support in English, Yoruba, Igbo, and Hausa.

The visible architecture is roughly:

```text
input text
  -> create language + speaker prompt
  -> tokenize prompt
  -> causal language model generates audio codes
  -> audio tokenizer decodes codes into waveform
  -> save/play 24kHz audio
```

## What We Should Copy Conceptually

We should copy these ideas:

- Treat speech as a model-serving backend, not a client feature.
- Use speaker IDs and language IDs.
- Keep audio generation behind a Python API.
- Generate short segments instead of one huge file.
- Make the provider replaceable.
- Optimize for Nigerian/local-language speech quality.

## What We Should Not Copy Blindly

We should not:

- Depend permanently on YarnGPT hosting or package behavior.
- Use any dataset we do not have legal rights to use.
- Clone voices without written consent.
- Open-source private model weights trained on restricted voice data.
- Make Sabi Voice only a TTS project.

Sabi Voice must be a learning system first, with TTS as one component.

## Sabi Voice Differentiation

YarnGPT's core value is Nigerian/local-language speech generation.

Sabi Voice's core value should be:

```text
Material-grounded teaching
  + local-language explanation
  + step-by-step academic reasoning
  + audio lesson segments
  + transcripts, formulas, key points, examples
  + Flutter/web Studio integration
```

For AbS, the strongest product is not "read this text aloud." It is:

```text
Turn this material into a tutor-led lesson.
```

## Architecture For AbS

```text
Flutter/Web Studio
  -> ABS-backend StudioJob voice-learning
  -> lesson script generation
  -> Sabi Voice Python service
  -> provider: stub | sabi-custom
  -> audio storage
  -> audioUrl returned to Studio
```

The Python service remains provider-neutral:

```text
POST /v1/tts
{
  "text": "...",
  "language": "yo",
  "voiceId": "sabi_female_yo_01",
  "format": "mp3",
  "speed": 1.0
}
```

## Provider Roadmap

### Provider 1: Stub

Purpose:

- Make backend, Flutter, and web integration work immediately.
- Generate valid audio files for testing.

Status:

- Implemented as the first provider.

### Provider 2: Sabi Custom Voice

Purpose:

- Own the Sabi learning voice.
- Use consented recordings.
- Tune for teaching tone, STEM, exam explanations, and local language.

Rules:

- Written speaker consent.
- Clean dataset.
- Separate license for model weights if needed.

## Open Source Strategy

To win on open source, Sabi Voice should be useful even without AbS.

Open-source components:

- FastAPI voice service.
- Provider interface.
- Stub provider.
- Local storage adapter.
- Example Node integration.
- Example lesson segment payload.
- Docs for adding providers.
- Evaluation scripts for latency and audio quality checks.
- Dataset preparation tools for consented voice data.

Do not open-source by default:

- Production API keys.
- Private AbS backend code.
- User material.
- Paid model weights unless license permits.
- Voice datasets without speaker consent and clear release license.

Recommended license:

- Apache-2.0 for code.
- Separate model/data licenses.

## Community Positioning

Sabi Voice should be positioned as:

```text
Open-source voice learning infrastructure for African education.
```

Not just:

```text
Another TTS wrapper.
```

The README should lead with:

- Local-language education.
- Learning from materials.
- Provider-neutral voice generation.
- Easy integration for apps.
- Safe consent-based voice training.

## Milestones

### Milestone 1

- Stub provider running.
- AbS backend can call `/v1/tts`.
- Flutter/web can play generated audio URL.

### Milestone 2

- Add Sabi custom provider placeholder.
- Add dataset tooling.
- Add speaker consent docs.

### Milestone 3

- Train/fine-tune first Sabi-owned voice model.
- Add model runtime behind `sabi-custom`.
- Benchmark latency, pronunciation, and teaching clarity.

### Milestone 4

- Add production storage adapter.
- Add Dockerfile.
- Add CI.
- Publish initial open-source repo.

### Milestone 5

- Launch AbS Studio voice-learning MVP.
- Collect feedback.
- Improve model/provider quality.
