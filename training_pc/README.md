# PC model training workspace

Thư mục này dành cho quy trình phát triển Keyword Spotting trên PC bằng
TensorFlow/Keras. Project firmware Silicon Labs nằm ngang cấp trong `firmware/`.

## Cấu trúc

```text
training_pc/
├── config/classes.yaml       # Danh sách nhãn và cấu hình audio/model
├── data/
│   ├── raw/                  # WAV nhận từ board, sắp xếp theo nhãn
│   └── processed/            # Audio/feature đã qua xử lý
├── models/
│   ├── checkpoints/          # Checkpoint TensorFlow/Keras
│   └── tflite/               # Model .tflite sau khi convert/quantize
├── src/                      # Mã tiền xử lý, dataset, train, evaluate, convert
├── tools/                    # Công cụ nhận audio qua serial và tạo WAV
└── tests/                    # Kiểm thử pipeline
```

Đây mới là khung thư mục; các script nhận audio, train và convert sẽ được triển
khai sau. Không có bước huấn luyện nào chạy trong Silicon Labs AI/ML SDK.

## Môi trường PC

Khuyến nghị Python 3.10 hoặc 3.11. Tạo virtual environment trong thư mục này:

```powershell
cd training_pc
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Dữ liệu

Board BRD2608A sẽ thu PCM; công cụ PC sẽ nhận gói dữ liệu qua serial và lưu WAV
vào `data/raw/<label>/`. Mỗi file nên được ghi lại metadata người nói, phòng,
khoảng cách và lượt thu, ví dụ:

```text
data/raw/on/spk01_room1_1m_take001.wav
```

Chốt danh sách lệnh trước khi thu dataset và cập nhật `config/classes.yaml`.
Tách train/validation/test theo người nói để tránh cùng một người xuất hiện
trong cả train và test.

## Đường đi model tới firmware

```text
data/raw WAV
  -> tiền xử lý giống Audio Feature Generator trên MCU
  -> train/evaluate TensorFlow/Keras
  -> convert và lượng tử hóa INT8 TFLite
  -> kiểm tra shape, quantization và operator
  -> chép model đạt yêu cầu vào ../firmware/config/tflite/
  -> SLC Generate, build và kiểm thử trên board
```

Đặc trưng khi train phải tương thích với Audio Feature Generator của firmware.
Không thay model trong firmware trước khi xác nhận preprocessing, tensor shape,
thứ tự nhãn và quantization khớp nhau.

## Chia sẻ với nhóm

Không commit WAV có giọng nói cá nhân, checkpoint lớn hoặc model thử nghiệm nếu
chưa thống nhất với nhóm. Quy tắc loại trừ dữ liệu và artifact nằm trong
`.gitignore`.
