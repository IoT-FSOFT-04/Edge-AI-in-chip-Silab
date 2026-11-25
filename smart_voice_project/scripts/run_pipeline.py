from pathlib import Path
import subprocess
import sys
import yaml


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, check=True)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))

    with (root / "config/classes.yaml").open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    from src.dataset import scan_dataset, split_by_speaker, save_splits

    rows = scan_dataset(root / "data/raw", config["classes"])
    if not rows:
        raise SystemExit("No WAV files found under data/raw/<class>")
    splits = split_by_speaker(rows, seed=config["training"]["seed"])
    save_splits(splits, root / "data/splits")

    counts = {name: len(items) for name, items in splits.items()}
    print("Dataset split:", counts)

    run([sys.executable, "src/train.py"])
    run([sys.executable, "src/evaluate.py"])
    run([sys.executable, "src/convert.py"])


if __name__ == "__main__":
    main()
