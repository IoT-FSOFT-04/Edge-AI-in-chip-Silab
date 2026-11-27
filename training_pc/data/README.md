# Dataset folders

- `raw/<label>/`: WAV clips captured from the BRD2608A microphone, grouped by
  the class labels in `../config/classes.yaml`.
- `processed/`: generated/preprocessed files; normally reproducible from raw
  recordings and not committed to Git.

Use mono 16 kHz PCM 16-bit WAV as the initial capture format. The final audio
format and preprocessing must be confirmed against the firmware Audio Feature
Generator before training a model intended for deployment.
