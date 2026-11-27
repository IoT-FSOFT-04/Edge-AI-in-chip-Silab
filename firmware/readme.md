# Silicon Labs firmware

Project firmware cho **EFR32MG26 / BRD2608A**, dùng Simplicity SDK,
MicriumOS, microphone I2S, Audio Feature Generator và TensorFlow Lite Micro.

## Project mẫu hiện tại

- Nhận diện `on` và `off` bằng `keyword_spotting_on_off_v2.tflite`.
- Khi nhận `on`, chạy model `blink.tflite` để điều khiển LED0 bằng PWM.
- Khi nhận `off`, tắt LED0.
- Cấu hình project/component nằm trong
  [aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos.slcp](aiml_soc_voice_control_light_blink_concurrent_efr32_micriumos.slcp).

## Các file chính

- [voice_control_light.cc](voice_control_light.cc): task MicriumOS, audio
  feature generation, inference và hành động LED mẫu.
- [recognize_commands.cc](recognize_commands.cc): xử lý nhãn, detection
  threshold và suppression.
- [config/](config/): cấu hình microphone, PWM, RTOS và model.
- [config/tflite/](config/tflite/): các model TFLite hiện tích hợp.
- [autogen/](autogen/): mã được SLC/Simplicity Studio sinh tự động; không sửa
  trực tiếp.
- [cmake_gcc/](cmake_gcc/): cấu hình build GCC/CMake.
- [tailieu/machine-learning.pdf](tailieu/machine-learning.pdf): tài liệu
  Silicon Labs AI/ML SDK trong workspace.

## Tích hợp model TensorFlow/Keras mới

Model được huấn luyện và đánh giá trên PC theo hướng dẫn tại
[../training_pc/README.md](../training_pc/README.md). Sau khi export `.tflite`:

1. Xác nhận input/output tensor, thứ tự nhãn, kiểu quantization và operators.
2. Xác nhận frontend dùng khi train khớp Audio Feature Generator trong project.
3. Đưa đúng model vào `config/tflite/` và cập nhật model instance nếu cần.
4. Chạy SLC Generate và build lại firmware.
5. Kiểm tra RAM/Flash, độ trễ và độ chính xác trên board.

Không giả định AI/ML Extension dùng để huấn luyện model và không sửa trực tiếp
`autogen/`.
