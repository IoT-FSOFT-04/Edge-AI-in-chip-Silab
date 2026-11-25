from pathlib import Path
import argparse
import json

import numpy as np
import tensorflow as tf
import yaml

from src.dataset import make_features


def load_split(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def representative_samples(
    rows: list[dict],
    config: dict,
    count: int = 100,
):
    features, _ = make_features(rows[:count], config)

    def generator():
        for feature in features:
            yield [feature[np.newaxis, ...]]

    return generator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/classes.yaml")
    parser.add_argument("--splits", default="data/splits")
    parser.add_argument("--model", default="models/checkpoints/best.keras")
    parser.add_argument("--output", default="models/exports/keyword_spotting.tflite")
    args = parser.parse_args()

    with Path(args.config).open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    model = tf.keras.models.load_model(args.model)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    train_rows = load_split(Path(args.splits) / "train.json")
    converter.representative_dataset = representative_samples(train_rows, config)
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8
    tflite = converter.convert()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(tflite)
    print(f"Exported: {output} ({len(tflite)} bytes)")


if __name__ == "__main__":
    main()
