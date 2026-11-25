import argparse
from datetime import datetime
from pathlib import Path
import queue

import sounddevice as sd
import soundfile as sf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--speaker", required=True)
    parser.add_argument("--output", default=None)
    parser.add_argument("--room", default="room")
    parser.add_argument("--distance", default="1m")
    parser.add_argument("--duration", type=float, default=1.0)
    parser.add_argument("--sample-rate", type=int, default=16000)
    args = parser.parse_args()

    output = Path(args.output or f"data/raw/{args.label}")
    output.mkdir(parents=True, exist_ok=True)
    frames = queue.Queue()

    def callback(indata, _frames, _time, status):
        if status:
            print(status)
        frames.put(indata.copy())

    print(f"Recording {args.label}. Press Ctrl+C to stop.")
    take = 1
    while True:
        input(f"Take {take}: press Enter then record {args.duration:.1f}s...")
        print("Recording...")
        recorded = []
        with sd.InputStream(
            samplerate=args.sample_rate,
            channels=1,
            dtype="float32",
            callback=callback,
        ):
            while sum(len(chunk) for chunk in recorded) < args.sample_rate * args.duration:
                recorded.append(frames.get())

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = (
            f"{args.speaker}_{args.room}_{args.distance}_{timestamp}_{take:03d}.wav"
        )
        path = output / filename
        samples = list(recorded)
        sf.write(path, __import__("numpy").concatenate(samples), args.sample_rate)
        print(f"Saved: {path}")
        take += 1


if __name__ == "__main__":
    main()
