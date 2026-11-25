from pathlib import Path
import argparse
import json

import tensorflow as tf
import yaml

from src.dataset import make_features
from src.model import build_model


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_split(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/classes.yaml")
    parser.add_argument("--splits", default="data/splits")
    parser.add_argument("--output", default="models/checkpoints")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    train_rows = load_split(Path(args.splits) / "train.json")
    validation_rows = load_split(Path(args.splits) / "validation.json")

    x_train, y_train = make_features(train_rows, config)
    x_validation, y_validation = make_features(validation_rows, config)

    tf.keras.utils.set_random_seed(config["training"]["seed"])
    model = build_model(
        input_shape=x_train.shape[1:],
        class_count=len(config["classes"]),
    )
    model.compile(
        optimizer=tf.keras.optimizers.Adam(config["training"]["learning_rate"]),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=8,
            restore_best_weights=True,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            str(output / "best.keras"),
            monitor="val_accuracy",
            save_best_only=True,
        ),
    ]
    history = model.fit(
        x_train,
        y_train,
        validation_data=(x_validation, y_validation),
        epochs=config["training"]["epochs"],
        batch_size=config["training"]["batch_size"],
        callbacks=callbacks,
    )

    model.save(output / "last.keras")
    with (output / "history.json").open("w", encoding="utf-8") as handle:
        json.dump(history.history, handle, indent=2)


if __name__ == "__main__":
    main()
