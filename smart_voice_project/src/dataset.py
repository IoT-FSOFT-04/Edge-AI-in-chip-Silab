from pathlib import Path
import json
import random

import numpy as np

from src.audio import load_audio, log_mel


def scan_dataset(raw_dir: Path, classes: list[str]) -> list[dict]:
    rows = []
    for class_index, label in enumerate(classes):
        label_dir = raw_dir / label
        for path in sorted(list(label_dir.glob("*.wav")) + list(label_dir.glob("*.WAV"))):
            filename_speaker = path.stem.split("_")[0]
            rows.append({
                "path": str(path),
                "label": label,
                "class_index": class_index,
                "speaker": filename_speaker,
            })
    return rows


def split_by_speaker(
    rows: list[dict],
    seed: int = 42,
    validation_ratio: float = 0.15,
    test_ratio: float = 0.15,
) -> dict[str, list[dict]]:
    speakers = sorted({row["speaker"] for row in rows})
    random.Random(seed).shuffle(speakers)
    test_count = max(1, int(len(speakers) * test_ratio))
    validation_count = max(1, int(len(speakers) * validation_ratio))

    test_speakers = set(speakers[:test_count])
    validation_speakers = set(speakers[test_count:test_count + validation_count])

    splits = {"train": [], "validation": [], "test": []}
    for row in rows:
        if row["speaker"] in test_speakers:
            splits["test"].append(row)
        elif row["speaker"] in validation_speakers:
            splits["validation"].append(row)
        else:
            splits["train"].append(row)
    return splits


def make_features(rows: list[dict], config: dict) -> tuple[np.ndarray, np.ndarray]:
    audio_config = config["audio"]
    feature_config = config["features"]
    features = []
    labels = []
    for row in rows:
        audio = load_audio(row["path"], audio_config["sample_rate"])
        mel = log_mel(
            audio,
            audio_config["sample_rate"],
            n_mels=feature_config["n_mels"],
            frame_length=feature_config["frame_length"],
            hop_length=feature_config["hop_length"],
        )
        features.append(mel[..., np.newaxis])
        labels.append(row["class_index"])
    return np.asarray(features, dtype=np.float32), np.asarray(labels, dtype=np.int32)


def save_splits(splits: dict[str, list[dict]], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in splits.items():
        with (output / f"{name}.json").open("w", encoding="utf-8") as handle:
            json.dump(rows, handle, indent=2)
