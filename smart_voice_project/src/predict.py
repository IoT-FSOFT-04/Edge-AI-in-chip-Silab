from pathlib import Path
import argparse

import numpy as np
import tensorflow as tf
import yaml

from src.audio import load_audio, log_mel


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("wav")
    parser.add_argument("--config", default="config/classes.yaml")
    parser.add_argument("--model", default="models/exports/keyword_spotting.tflite")
    args = parser.parse_args()

    with Path(args.config).open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    audio_config = config["audio"]
    feature_config = config["features"]

    audio = load_audio(args.wav, audio_config["sample_rate"])
    mel = log_mel(
        audio,
        audio_config["sample_rate"],
        n_mels=feature_config["n_mels"],
        frame_length=feature_config["frame_length"],
        hop_length=feature_config["hop_length"],
    )
    sample = mel[..., np.newaxis][np.newaxis, ...].astype(np.float32)

    interpreter = tf.lite.Interpreter(model_path=args.model)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]

    sample_input = sample
    if input_details["dtype"] == np.int8:
        scale, zero_point = input_details["quantization"]
        sample_input = np.clip(
            np.round(sample / scale + zero_point),
            -128,
            127,
        ).astype(np.int8)

    interpreter.set_tensor(input_details["index"], sample_input)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details["index"])[0]
    if output_details["dtype"] == np.int8:
        scale, zero_point = output_details["quantization"]
        output = (output.astype(np.float32) - zero_point) * scale

    result = sorted(
        zip(config["classes"], output),
        key=lambda item: item[1],
        reverse=True,
    )
    for label, score in result:
        print(f"{label}: {score:.4f}")


if __name__ == "__main__":
    main()
