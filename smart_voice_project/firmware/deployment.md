# Deployment lên Silicon Labs

## 1. Sao lưu project

Giữ project gốc. Khi triển khai mô hình mới, thay `.tflite` trong thư mục firmware
`config/tflite/`, không sửa `autogen/`.

## 2. Đặt mô hình mới

Sao chép:

```text
smart_voice_project/models/exports/keyword_spotting.tflite
```

thành:

```text
config/tflite/keyword_spotting_on_off_v2.tflite
```

Sau đó mở project trong Simplicity Studio và chạy **SLC Generate**.

## 3. Cập nhật nhãn

Nhãn mô hình phải khớp thứ tự đầu ra và cấu hình `classes` trong:

```text
config/classes.yaml
```

Hiện mã firmware trong `recognize_commands.cc` chỉ mặc định 4 nhãn theo thứ tự:

```text
0 on
1 off
2 unknown
3 background
```

Nếu train thêm lệnh điều khiển thiết bị, cập nhật:

- `kCategoryLabels`
- `kMaxCategoryCount`
- `num_classes`
- metadata parameter `classes`
- bộ ánh xạ lệnh sang thiết bị

## 4. Thay bộ điều khiển

Tách animation LED hiện tại khỏi nhận diện:

```text
recognize_commands.cc
  -> nhận diện

device_control.cc
  -> ánh xạ nhãn sang relay/GPIO/BLE/Wi-Fi
```

Không để chuỗi action thiết bị nằm trực tiếp trong `recognize_commands.cc`.

## 5. Build

Trong VS Code sử dụng:

```text
Simplicity Studio: Build
```

Hoặc build CMake hiện có:

```powershell
cmake --build cmake_gcc/build
```

## 6. Nạp firmware

Mở **Silicon Labs VS Code Debugger** hoặc dùng **Commander** để nạp firmware đã build.

Kiểm tra tối thiểu:

- Microphone bắt đầu lấy mẫu ở EM1.
- Không có lệnh giả liên tục.
- Cả `on` và `off` hoạt động.
- Từ khóa khác bị nhãn `unknown/background`.
- Relay hoặc LED thực hiện đúng trạng thái.
- Dòng log ngưỡng và suppression hợp lý.
