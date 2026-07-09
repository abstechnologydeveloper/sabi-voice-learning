# Model Licenses

This repository must not commit model weights unless their license allows
redistribution. Production deployments should mount model files at runtime and
set explicit paths in `.env`.

## Approved Production Candidates

### Kokoro ONNX

- Provider: `kokoro-onnx`
- Purpose: production local English/Nigerian-English speech generation.
- Required files:
  - `models/kokoro/kokoro-v1.0.onnx`
  - `models/kokoro/voices-v1.0.bin`
- Runtime config:
  - provider defaults to `kokoro-onnx`
- Rule: verify model and voice file license before production use.

## Not Approved For AbS Plus Production Without Separate Review

- Non-commercial checkpoints.
- Voice-cloning checkpoints trained on unclear speaker consent.
- Any checkpoint whose dataset or redistribution terms are unclear.

## Sabi-Owned Voice Requirement

For Yoruba, Hausa, Igbo, Pidgin, and branded Sabi teacher voices, the production
target is a Sabi-owned or Sabi-licensed model trained from consented recordings.
Open-source engines may be used as runtimes, but the final voices must have
clean commercial rights.
