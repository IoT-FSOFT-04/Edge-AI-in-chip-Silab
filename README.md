# Edge AI Voice Recognition and Device Control

Repository này tách phần firmware Silicon Labs và phần phát triển model trên PC:

```text
.
├── firmware/     # Project Simplicity Studio cho EFR32MG26 / BRD2608A
└── training_pc/  # Thu dữ liệu, train/evaluate TensorFlow/Keras, export TFLite
```

## Quy trình phát triển dự kiến

```text
BRD2608A microphone
  -> gửi PCM về PC
  -> lưu WAV và gán nhãn trong training_pc/data/
  -> train/evaluate TensorFlow/Keras trên PC
  -> convert và lượng tử hóa INT8 TFLite
  -> đưa model vào firmware/config/tflite/
  -> SLC Generate, build và kiểm thử trên EFR32MG26
```

TensorFlow/Keras trên PC là framework huấn luyện. Silicon Labs AI/ML SDK trong
firmware cung cấp các thành phần cần để tạo đặc trưng âm thanh và chạy inference
bằng TensorFlow Lite Micro; không dùng AI/ML SDK để huấn luyện model.

Các bước truyền audio từ board, tạo WAV, huấn luyện và convert model hiện mới là
quy trình mục tiêu; các công cụ tương ứng trong `training_pc/` chưa được triển
khai.

## Bắt đầu

- Xem [firmware/readme.md](firmware/readme.md) để hiểu project Silicon Labs hiện
  tại và các model mẫu.
- Xem [training_pc/README.md](training_pc/README.md) để biết cấu trúc dữ liệu và
  quy trình phát triển model trên PC.

## Trạng thái

Đây là khung dự án. Firmware hiện có model mẫu nhận diện `on`/`off` và điều khiển
LED0. Chưa có chức năng gửi audio PCM từ board về PC, dataset WAV của nhóm, hoặc
model TensorFlow/Keras do nhóm huấn luyện.

Khi train model mới, cần đồng bộ frontend, tensor shape, thứ tự nhãn và lượng tử
hóa giữa PC và Audio Feature Generator trên firmware trước khi nạp thử.
