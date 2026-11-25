from pathlib import Path
import argparse
import json

import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import yaml

from src.dataset import make_features


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/classes.yaml")
    parser.add_argument("--splits", default="data/splits")
    parser.add_argument("--model", default="models/checkpoints/best.keras")
    parser.add_argument("--output", default="models/exports")
    args = parser.parse_args()

    with Path(args.config).open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    with (Path(args.splits) / "test.json").open("r", encoding="utf-8") as handle:
        test_rows = json.load(handle)

    x_test, y_test = make_features(test_rows, config)
    model = tf.keras.models.load_model(args.model)
    probabilities = model.predict(x_test, verbose=0)
    predictions = np.argmax(probabilities, axis=1)

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    report = classification_report(
        y_test,
        predictions,
        target_names=config["classes"],
        zero_division=0,
    )
    matrix = confusion_matrix(y_test, predictions)
    print(report)
    print("Confusion matrix:")
    print(matrix)
    (output / "classification_report.txt").write_text(report, encoding="utf-8")
    np.save(output / "confusion_matrix.npy", matrix)


if __name__ == "__main__":
    main()
