# Smart Voice Project

Khung project phát triển nhận diện từ khóa và điều khiển thiết bị nhà ở trên EFR32MG26.

Luồng phát triển:

```text
data/raw/*.wav
  -> tiền xử lý về 16 kHz / 1 giây
  -> train mô hình CNN
  -> evaluation trên validation/test
  -> quantization INT8
  -> exports/keyword_spotting.tflite
  -> thay mô hình trong Simplicity Studio
  -> build firmware
  -> nạp bằng Commander hoặc VS Code
```

## Cấu trúc

```text
smart_voice_project/
├── config/classes.yaml
├── data/
│   ├── raw/{on,off,unknown,background}
│   ├── processed/
│   ├── splits/
│   └── README.md
├── src/
│   ├── audio.py
│   ├── dataset.py
│   ├── model.py
│   ├── train.py
│   ├── evaluate.py
│   ├── convert.py
│   └── predict.py
├── scripts/
│   ├── collect_audio.py
│   └── run_pipeline.py
├── models/
│   ├── checkpoints/
│   └── exports/
├── firmware/
│   └── deployment.md
├── tests/
│   └── test_pipeline.py
├── requirements.txt
└── pyproject.toml
```

## Cài đặt

Khuyến nghị Python 3.10 hoặc 3.11.

```powershell
cd smart_voice_project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Thu thập dữ liệu

```powershell
python scripts/collect_audio.py --label on --speaker member01 --output data/raw/on
python scripts/collect_audio.py --label off --speaker member01 --output data/raw/off
python scripts/collect_audio.py --label unknown --speaker member01 --output data/raw/unknown
python scripts/collect_audio.py --label background --speaker member01 --output data/raw/background
```

Mỗi lần thu được một file WAV tên theo thời gian.

## Chạy pipeline

```powershell
python scripts/run_pipeline.py
```

Lệnh trên lần lượt:

1. Quét data WAV.
2. Chuẩn hóa 16 kHz/1 giây.
3. Tách train/validation/test theo người nói.
4. Huấn luyện.
5. Đánh giá.
6. Xuất mô hình INT8 `.tflite`.

## Quy tắc dữ liệu

- `on`, `off`: dữ liệu từ khóa đúng.
- `unknown`: câu gần giống hoặc các từ khóa khác.
- `background`: tiếng phòng yên, tiếng quạt, TV, xe cộ hoặc âm thanh không có lệnh.
- Không để cùng một người nói xuất hiện đồng thời trong train và test.
- Không copy cùng một file gốc vào nhiều speaker group.
- Giữ tên file: `<speaker>_<room>_<distance>_<take>.wav`.
