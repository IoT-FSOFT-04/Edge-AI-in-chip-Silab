import numpy as np

from src.audio import load_audio, log_mel


def test_log_mel_shape() -> None:
    audio = np.random.RandomState(42).normal(0, 0.1, 16000).astype(np.float32)
    mel = log_mel(audio, 16000, n_mels=40, frame_length=512, hop_length=160)
    assert mel.shape[1] == 40
    assert mel.shape[0] > 50
    assert np.isfinite(mel).all()
