# Edge-AI-in-chip-Silab

Project nhóm phát triển nhận diện âm thanh và điều khiển thiết bị bằng AI trên chip Silicon Labs EFR32MG26.

## Nội dung project

- Firmware Simplicity Studio/MicriumOS chạy TensorFlow Lite Micro.
- Nhận dạng liên tục bằng microphone I2S.
- Framework Python thu thập dữ liệu, huấn luyện, đánh giá và chuyển đổi mô hình sang INT8 TFLite.
- Tài liệu triển khai mô hình mới lên board Silicon Labs.

## Firmware hiện tại

Tên project:

```text
aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos
```

Firmware sử dụng:

- Microphone I2S để thu âm thanh.
- Mô hình `keyword_spotting_on_off_v2.tflite` để nhận dạng `on` và `off`.
- Mô hình `blink.tflite` để điều khiển animation LED bằng PWM.
- MicriumOS task để chạy inference định kỳ.
- Concurrency load để giữ cả hai mô hình trong RAM.

Các mô hình hiện tại nằm trong `config/tflite/`.

## PC training framework

Khung phát triển Python nằm trong [smart_voice_project/](smart_voice_project/README.md).

Luồng phát triển:

```text
Thu âm .wav
  -> tiền xử lý 16 kHz / Log-Mel
  -> chia train/validation/test theo người nói
  -> huấn luyện CNN
  -> đánh giá
  -> quantization INT8
  -> export .tflite
  -> thay mô hình vào firmware
  -> build và nạp lên EFR32
```

## Cấu trúc chính

```text
.
├── app.c                           # entry point ứng dụng
├── voice_control_light.cc          # task nhận diện và điều khiển LED
├── recognize_commands.cc           # xử lý kết quả inference
├── config/tflite/                  # mô hình TFLite hiện tại
├── smart_voice_project/
│   ├── data/
│   ├── src/
│   ├── scripts/
│   ├── models/
│   ├── firmware/
│   └── tests/
├── cmake_gcc/                      # build CMake hiện tại
└── *.slcp                          # cấu hình Simplicity SDK
```

## Quy tắc dữ liệu

- Không commit file dữ liệu cá nhân hoặc WAV chưa được nhóm phép.
- Nhãn `on`: mẫu phát âm từ khóa bật.
- Nhãn `off`: mẫu phát âm từ khóa tắt.
- Nhãn `unknown`: câu hoặc từ khóa không thuộc hai lệnh.
- Nhãn `background`: tiếng ồn phòng, quạt, TV và môi trường.
- Tách test theo người nói để đánh giá khả năng tổng quát.

## Hướng dẫn nhanh

Thu thập dữ liệu và huấn luyện trên PC:

```powershell
cd smart_voice_project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python scripts/collect_audio.py --label on --speaker member01
python scripts/collect_audio.py --label off --speaker member01
python scripts/collect_audio.py --label unknown --speaker member01
python scripts/collect_audio.py --label background --speaker member01

python scripts/run_pipeline.py
```

Mô hình sau khi export nằm tại:

```text
smart_voice_project/models/exports/keyword_spotting.tflite
```

Xem hướng dẫn triển khai firmware tại [firmware/deployment.md](smart_voice_project/firmware/deployment.md).
