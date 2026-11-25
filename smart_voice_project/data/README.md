# Data Layout

Đặt file WAV vào thư mục theo nhãn:

```text
data/raw/on/*.wav
data/raw/off/*.wav
data/raw/unknown/*.wav
data/raw/background/*.wav
```

Tên file khuyến nghị:

```text
<speaker>_<room>_<distance_m>_<take>.wav
```

Ví dụ:

```text
member01_livingroom_2m_001.wav
member02_bedroom_1m_012.wav
```

Không commit dữ liệu cá nhân hoặc dữ liệu có chấp nhận rủi ro riêng tư nếu chưa được phép.
