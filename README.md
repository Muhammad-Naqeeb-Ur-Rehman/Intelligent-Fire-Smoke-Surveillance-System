<div align="center">

# 🔥 Intelligent Fire & Smoke Surveillance System

### AI-powered real-time fire and smoke detection with live alerting, recording, and notifications

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![YOLO](https://img.shields.io/badge/YOLOv8-Ultralytics-purple)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

<br>

<img src="assets/screenshots/banner.png" alt="FireGuard AI Banner" width="100%">

</div>

---

## 📖 Overview

**FireGuard AI** is a full-stack, AI-powered surveillance system that detects **fire and smoke in real time** from images, video files, laptop webcams, and IP/RTSP CCTV cameras. Built on a **custom-trained YOLOv8 model**, it goes beyond simple detection — providing a complete monitoring pipeline with live alerts, auto-recording, snapshot logging, analytics dashboards, and instant notifications via Email and Discord.

Designed to feel like a **real commercial safety monitoring product**, not just a detection demo.

---

## ✨ Key Features

<table>
<tr>
<td width="50%" valign="top">

### 🎯 Detection Modes
- 🖼️ **Image Detection** — upload and analyze single images
- 🎥 **Video Detection** — process pre-recorded video files
- 📹 **Live Webcam** — real-time detection from your laptop camera
- 🌐 **IP / RTSP Camera** — connect to Hikvision, Dahua, Uniview, Axis, or any ONVIF camera

### 📈 Analytics & Insights
- Real-time stat dashboard (fire/smoke status, confidence, processing time)
- Confidence distribution histograms
- Live trend charts across detection sessions
- Full detection history table

</td>
<td width="50%" valign="top">

### 🚨 Safety & Alerting
- Flashing critical alert banners with recommended actions
- In-browser alarm sound on fire detection
- Scrolling live detection log (console-style)
- Detection counters and timestamps

### 🔔 Automation
- Auto-snapshot capture on every threat detection
- Auto-recording of fire/smoke events with pre/post buffers
- Email notifications via Outlook SMTP (with snapshot attached)
- Discord webhook alerts with rich embeds

</td>
</tr>
</table>

---

## 🖥️ Screenshots

<div align="center">

| Dashboard | Live Detection |
|:---:|:---:|
| <img src="assets/screenshots/dashboard.png" width="400"> | <img src="assets/screenshots/live-detection.png" width="400"> |

| Alert Panel | Snapshot Gallery |
|:---:|:---:|
| <img src="assets/screenshots/alert-panel.png" width="400"> | <img src="assets/screenshots/gallery.png" width="400"> |

</div>

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | Streamlit (custom dark-themed CSS) |
| **AI Model** | YOLOv8 (Ultralytics) — custom-trained on fire/smoke dataset |
| **Computer Vision** | OpenCV |
| **Video Processing** | FFmpeg |
| **Visualization** | Plotly |
| **Notifications** | SMTP (Outlook), Discord Webhooks |
| **Data Handling** | Pandas, NumPy |

---

## 📂 Project Structure

```
Intelligent-Fire-Smoke-Surveillance-System/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
├── .gitignore
│
├── .streamlit/
│   └── config.toml             # Streamlit theme configuration
│
├── models/
│   └── best.pt                 # Trained YOLOv8 weights (not tracked in git — see below)
│
├── assets/
│   └── screenshots/            # README images / demo GIFs
│
└── recordings/                 # Auto-saved event recordings (runtime generated)
```

> ⚠️ **Note on model weights:** `models/best.pt` is excluded from version control due to file size. See [Setup](#-setup--installation) below for how to add your trained model.

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Muhammad-Naqeeb-Ur-Rehman/Intelligent-Fire-Smoke-Surveillance-System.git
cd Intelligent-Fire-Smoke-Surveillance-System
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg (required for video processing)

**Windows:**
1. Download from [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/) → `ffmpeg-release-essentials.zip`
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your System PATH
4. Verify: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### 5. Add your trained model

Place your trained YOLOv8 weights file at:
```
models/best.pt
```

### 6. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🔔 Notification Setup (Optional)

### Email (Outlook SMTP)
1. Open the app sidebar → **🔔 Notifications** → enable **Email (Outlook)**
2. Generate an [App Password](https://support.microsoft.com/en-us/account-billing/manage-app-passwords-for-two-step-verification-d6dc8c6d-4bf7-4851-ad95-6d07799387e9) for your Outlook account
3. Enter your email, app password, and recipient email in the sidebar

### Discord Webhook
1. In your Discord server: **Server Settings → Integrations → Webhooks → New Webhook**
2. Copy the webhook URL
3. Paste it into the sidebar under **💬 Discord Webhook**

---

## 🌐 IP / RTSP Camera Examples

| Brand | RTSP URL Format |
|---|---|
| **Hikvision** | `rtsp://user:pass@IP:554/Streaming/Channels/101` |
| **Dahua** | `rtsp://user:pass@IP:554/cam/realmonitor?channel=1&subtype=0` |
| **Axis** | `rtsp://user:pass@IP/axis-media/media.amp` |
| **Generic ONVIF** | `rtsp://user:pass@IP:554/stream1` |

---

## 🗺️ Roadmap

- [ ] Multi-camera grid view
- [ ] Cloud storage integration for recordings (S3 / Drive)
- [ ] Mobile push notifications
- [ ] Role-based access / multi-user login
- [ ] Heatmap of detection zones over time

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/Muhammad-Naqeeb-Ur-Rehman/Intelligent-Fire-Smoke-Surveillance-System/issues).

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

---

## 👤 Author

**Muhammad Naqeeb Ur Rehman**

[![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)](https://github.com/Muhammad-Naqeeb-Ur-Rehman)

---

<div align="center">

⭐ **If you find this project useful, consider giving it a star!** ⭐

</div>
