from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
from math import gcd


TARGET_SECONDS = 1.0


def load_audio(path: str | Path, sample_rate: int = 16000) -> np.ndarray:
    samples, source_rate = sf.read(path, dtype="float32", always_2d=False)
    if samples.ndim > 1:
        samples = np.mean(samples, axis=1)

    if source_rate != sample_rate:
        divisor = gcd(source_rate, sample_rate)
        samples = resample_poly(samples, sample_rate // divisor, source_rate // divisor)

    target_length = int(sample_rate * TARGET_SECONDS)
    if len(samples) < target_length:
        samples = np.pad(samples, (0, target_length - len(samples)))
    else:
        peak = np.max(np.abs(samples))
        if peak > 1e-6:
            start = int(np.argmax(np.abs(samples)) - target_length * 0.25)
            start = max(0, min(start, len(samples) - target_length))
        else:
            start = 0
        samples = samples[start:start + target_length]

    peak = np.max(np.abs(samples))
    if peak > 1e-6:
        samples = samples / peak
    return np.asarray(samples, dtype=np.float32)


def log_mel(
    audio: np.ndarray,
    sample_rate: int,
    n_mels: int = 40,
    frame_length: int = 512,
    hop_length: int = 160,
) -> np.ndarray:
    window = np.hanning(frame_length).astype(np.float32)
    pad = frame_length // 2
    padded = np.pad(audio, (pad, pad), mode="reflect")
    frames = np.lib.stride_tricks.sliding_window_view(padded, frame_length)[::hop_length]
    frames = frames[:200]

    spectrum = np.abs(np.fft.rfft(frames * window, n=frame_length, axis=1))
    mel_filter = _mel_filterbank(sample_rate, frame_length, n_mels)
    mel = spectrum @ mel_filter.T
    mel = np.log(np.maximum(mel, 1e-6))

    mean = mel.mean()
    std = mel.std()
    if std > 1e-6:
        mel = (mel - mean) / std
    return mel.astype(np.float32)


def _mel_filterbank(sample_rate: int, fft_length: int, n_mels: int) -> np.ndarray:
    def hz_to_mel(hz):
        return 2595.0 * np.log10(1.0 + hz / 700.0)

    def mel_to_hz(mel):
        return 700.0 * (10.0 ** (mel / 2595.0) - 1.0)

    frequencies = np.linspace(
        hz_to_mel(0),
        hz_to_mel(sample_rate / 2),
        n_mels + 2,
    )
    frequencies = mel_to_hz(frequencies)
    bins = np.floor((fft_length + 1) * frequencies / sample_rate).astype(int)
    bins = np.clip(bins, 0, fft_length // 2)

    filters = np.zeros((n_mels, fft_length // 2 + 1), dtype=np.float32)
    for index in range(n_mels):
        left, center, right = bins[index:index + 3]
        if center > left:
            filters[index, left:center] = (
                np.arange(left, center) - left
            ) / (center - left)
        if right > center:
            filters[index, center:right] = (
                right - np.arange(center, right)
            ) / (right - center)
    return filters
