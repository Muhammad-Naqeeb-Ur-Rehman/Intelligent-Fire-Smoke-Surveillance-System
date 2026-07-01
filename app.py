import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import os
import cv2
import time
import subprocess
import base64
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import threading
import queue
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import requests
import numpy as np
import json

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="FireGuard AI — Pro Surveillance",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# DARK THEME + PROFESSIONAL UI
# =====================================================

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d1117;
    color: #e6edf3;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #30363d;
}
[data-testid="stHeader"] { background: transparent; }

.brand-bar {
    display: flex; align-items: center; gap: 14px;
    padding: 18px 0 8px 0;
    border-bottom: 1px solid #30363d;
    margin-bottom: 24px;
}
.brand-title {
    font-size: 1.75rem; font-weight: 700;
    letter-spacing: -0.5px; color: #f0f6fc; line-height: 1;
}
.brand-subtitle {
    font-size: 0.78rem; color: #8b949e;
    letter-spacing: 0.06em; text-transform: uppercase; margin-top: 3px;
}
.brand-dot {
    width: 38px; height: 38px; border-radius: 10px;
    background: linear-gradient(135deg, #ff4d4d 0%, #ff8c00 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    box-shadow: 0 0 16px rgba(255,77,77,0.45); flex-shrink: 0;
}

.stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
    gap: 12px; margin: 18px 0;
}
.stat-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 12px; padding: 16px 18px;
    display: flex; flex-direction: column; gap: 6px;
    transition: border-color 0.2s;
}
.stat-card:hover { border-color: #ff4d4d55; }
.stat-label { font-size: 0.72rem; color: #8b949e; text-transform: uppercase; letter-spacing: 0.07em; }
.stat-value { font-size: 1.35rem; font-weight: 700; color: #f0f6fc; line-height: 1; }
.stat-value.fire  { color: #ff6b35; }
.stat-value.smoke { color: #a8b2d8; }
.stat-value.green { color: #3fb950; }

@keyframes flash {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.25; }
}
.alert-critical {
    background: linear-gradient(135deg, #3d0e0e 0%, #2a0a0a 100%);
    border: 1.5px solid #ff4d4d; border-radius: 14px;
    padding: 22px 26px; margin: 20px 0;
    box-shadow: 0 0 24px rgba(255,77,77,0.35);
    animation: flash 1.2s ease-in-out infinite;
}
.alert-warning {
    background: linear-gradient(135deg, #2d1a00 0%, #1e1200 100%);
    border: 1.5px solid #e3a008; border-radius: 14px;
    padding: 22px 26px; margin: 20px 0;
    box-shadow: 0 0 24px rgba(227,160,8,0.18);
}
.alert-safe {
    background: linear-gradient(135deg, #0d2a18 0%, #071a0f 100%);
    border: 1.5px solid #3fb950; border-radius: 14px;
    padding: 22px 26px; margin: 20px 0;
}
.alert-title { font-size: 1.15rem; font-weight: 700; margin-bottom: 10px; }
.alert-action-item { font-size: 0.88rem; padding: 4px 0; color: #c9d1d9; }

.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
    gap: 14px; margin: 16px 0;
}
.gallery-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 12px; overflow: hidden;
    transition: transform 0.18s, border-color 0.18s;
}
.gallery-card:hover { transform: translateY(-3px); border-color: #ff4d4d88; }
.gallery-meta { padding: 8px 10px; font-size: 0.72rem; color: #8b949e; line-height: 1.6; }
.gallery-meta strong { color: #f0f6fc; font-size: 0.8rem; }

.log-box {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 14px 16px;
    font-family: 'Courier New', monospace;
    font-size: 0.82rem;
    max-height: 280px;
    overflow-y: auto;
    line-height: 1.9;
}
.log-fire  { color: #ff6b35; }
.log-smoke { color: #a8b2d8; }
.log-safe  { color: #3fb950; }
.log-time  { color: #484f58; margin-right: 10px; }

.section-heading {
    font-size: 1rem; font-weight: 600; color: #c9d1d9;
    letter-spacing: 0.03em; margin: 28px 0 12px 0;
    padding-bottom: 8px; border-bottom: 1px solid #21262d;
    display: flex; align-items: center; gap: 8px;
}

.stButton > button {
    background: linear-gradient(135deg, #ff4d4d, #ff8c00);
    color: white; border: none; border-radius: 8px;
    font-weight: 600; padding: 0.55rem 1.4rem;
    font-size: 0.88rem; letter-spacing: 0.03em;
    transition: opacity 0.18s, transform 0.18s;
    box-shadow: 0 0 14px rgba(255,77,77,0.3);
}
.stButton > button:hover { opacity: 0.88; transform: translateY(-1px); }

div[data-testid="stFileUploader"] {
    background: #161b22; border: 1.5px dashed #30363d;
    border-radius: 12px; padding: 10px;
}
div[data-testid="stFileUploader"]:hover { border-color: #ff4d4d66; }

div[data-testid="stMetric"] {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 10px; padding: 12px 16px;
}
div[data-testid="stMetricLabel"] p { color: #8b949e !important; font-size: 0.78rem !important; }
div[data-testid="stMetricValue"]   { color: #f0f6fc !important; }

hr { border-color: #21262d !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
</style>

<!-- Alarm sound (base64 beep via Web Audio API) -->
<script>
function playAlarm() {
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        function beep(freq, start, dur) {
            const o = ctx.createOscillator();
            const g = ctx.createGain();
            o.connect(g); g.connect(ctx.destination);
            o.frequency.value = freq;
            o.type = 'square';
            g.gain.setValueAtTime(0.3, ctx.currentTime + start);
            g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + start + dur);
            o.start(ctx.currentTime + start);
            o.stop(ctx.currentTime + start + dur + 0.05);
        }
        for (let i = 0; i < 4; i++) { beep(880, i * 0.35, 0.25); beep(660, i * 0.35 + 0.15, 0.15); }
    } catch(e) {}
}
window.playAlarm = playAlarm;
</script>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "history":        [],
    "snapshots":      [],
    "detection_log":  [],
    "image_result":   None,
    "video_result":   None,
    "webcam_running": False,
    "fire_count":     0,
    "smoke_count":    0,
    "recording":      False,
    "rec_path":       "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# =====================================================
# BRAND BAR
# =====================================================

st.markdown("""
<div class="brand-bar">
    <div class="brand-dot">🔥</div>
    <div>
        <div class="brand-title">FireGuard AI <span style="font-size:0.9rem;color:#ff4d4d;font-weight:500;">PRO</span></div>
        <div class="brand-subtitle">Intelligent Fire &amp; Smoke Surveillance System</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("### ⚙️ Detection Settings")
    confidence = st.slider("Confidence Threshold", 0.10, 1.00, 0.10, 0.05)

    st.markdown("---")
    mode = st.radio("Detection Mode", [
        "🖼️  Image Detection",
        "🎥  Video Detection",
        "📹  Live Webcam",
        "🌐  IP / RTSP Camera",
    ])

    st.markdown("---")
    st.markdown("### 🔔 Notifications")

    notif_expander = st.expander("Configure Alerts", expanded=False)
    with notif_expander:
        enable_email   = st.checkbox("📧 Email (Outlook)")
        enable_discord = st.checkbox("💬 Discord Webhook")

        if enable_email:
            outlook_user = st.text_input("Outlook Email",    placeholder="you@outlook.com")
            outlook_pass = st.text_input("App Password",     type="password")
            notify_to    = st.text_input("Notify To (email)", placeholder="recipient@email.com")
        else:
            outlook_user = outlook_pass = notify_to = ""

        if enable_discord:
            discord_webhook = st.text_input("Discord Webhook URL", type="password")
        else:
            discord_webhook = ""

    st.markdown("---")
    st.markdown("### 💾 Auto Recording")
    rec_expander = st.expander("Recording Settings", expanded=False)
    with rec_expander:
        rec_save_path = st.text_input(
            "Save recordings to",
            value="recordings/",
            help="Folder path where event recordings are saved"
        )
        rec_pre_secs  = st.slider("Pre-event buffer (sec)", 0, 10, 3)
        rec_post_secs = st.slider("Post-event buffer (sec)", 0, 30, 5)

    st.markdown("---")
    st.markdown(
        "<div style='background:#1a2a1a;border:1px solid #3fb95055;"
        "border-radius:8px;padding:10px 14px;font-size:0.82rem;color:#3fb950;'>"
        "✅ YOLO Model Loaded</div>", unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear All Data"):
        for k, v in defaults.items():
            st.session_state[k] = v if not isinstance(v, list) else []
        st.rerun()

# =====================================================
# NOTIFICATION HELPERS
# =====================================================

def send_email_alert(label: str, conf: float, img_bgr, outlook_user: str,
                     outlook_pass: str, notify_to: str):
    try:
        msg = MIMEMultipart()
        msg["Subject"] = f"🔥 FireGuard AI — {label.upper()} DETECTED"
        msg["From"]    = outlook_user
        msg["To"]      = notify_to

        body = MIMEText(f"""
🚨 FireGuard AI Alert

Detection Type : {label.upper()}
Confidence     : {conf*100:.1f}%
Time           : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Recommended Actions:
✔ Evacuate the area immediately
✔ Notify Fire Department
✔ Shut down nearby equipment

-- FireGuard AI Pro Surveillance System
        """)
        msg.attach(body)

        # Attach snapshot
        _, buf = cv2.imencode(".jpg", img_bgr)
        img_attach = MIMEImage(buf.tobytes(), name="snapshot.jpg")
        msg.attach(img_attach)

        with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
            server.starttls()
            server.login(outlook_user, outlook_pass)
            server.sendmail(outlook_user, notify_to, msg.as_string())
        return True
    except Exception as e:
        return str(e)


def send_discord_alert(label: str, conf: float, img_bgr, webhook_url: str):
    try:
        _, buf = cv2.imencode(".jpg", img_bgr)
        payload = {
            "embeds": [{
                "title": f"🚨 {label.upper()} DETECTED — FireGuard AI",
                "color": 16711680 if label.lower() == "fire" else 16753920,
                "fields": [
                    {"name": "Detection",  "value": label.upper(),               "inline": True},
                    {"name": "Confidence", "value": f"{conf*100:.1f}%",          "inline": True},
                    {"name": "Time",       "value": datetime.now().strftime("%H:%M:%S"), "inline": True},
                    {"name": "Action",     "value": "Evacuate & call Fire Dept", "inline": False},
                ],
                "footer": {"text": "FireGuard AI Pro Surveillance"},
            }]
        }
        files = {"file": ("snapshot.jpg", buf.tobytes(), "image/jpeg")}
        data  = {"payload_json": json.dumps(payload)}
        requests.post(webhook_url, data=data, files=files, timeout=8)
        return True
    except Exception as e:
        return str(e)


def send_notifications(label: str, conf: float, img_bgr):
    if enable_email and outlook_user and outlook_pass and notify_to:
        threading.Thread(
            target=send_email_alert,
            args=(label, conf, img_bgr, outlook_user, outlook_pass, notify_to),
            daemon=True
        ).start()

    if enable_discord and discord_webhook:
        threading.Thread(
            target=send_discord_alert,
            args=(label, conf, img_bgr, discord_webhook),
            daemon=True
        ).start()

# =====================================================
# RECORDING HELPER
# =====================================================

def get_video_writer(save_path: str, fps: float, width: int, height: int):
    Path(save_path).mkdir(parents=True, exist_ok=True)
    filename = datetime.now().strftime("event_%Y%m%d_%H%M%S.mp4")
    full_path = str(Path(save_path) / filename)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    return cv2.VideoWriter(full_path, fourcc, fps, (width, height)), full_path

# =====================================================
# SHARED HELPERS
# =====================================================

def image_to_b64(img_bgr) -> str:
    _, buf = cv2.imencode(".jpg", img_bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buf).decode()


def save_snapshot(annotated_bgr, label: str, conf: float, date_str: str = None, time_str: str = None):
    now = datetime.now()
    st.session_state.snapshots.append({
        "date":    date_str or now.strftime("%Y-%m-%d"),
        "time":    time_str or now.strftime("%I:%M:%S %p"),
        "label":   label,
        "conf":    conf,
        "img_b64": image_to_b64(annotated_bgr),
    })


def add_log(label: str, conf: float):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.detection_log.append({
        "time":  ts,
        "label": label,
        "conf":  conf,
    })
    if len(st.session_state.detection_log) > 200:
        st.session_state.detection_log = st.session_state.detection_log[-200:]


def build_alert(fire: bool, smoke: bool, highest_conf: float,
                count: int = None, ts: str = None, play_sound: bool = False):
    sound_js = '<script>if(window.playAlarm) window.playAlarm();</script>' if play_sound else ''
    if fire:
        actions = [
            "🚒 Notify Fire Department immediately",
            "🚪 Evacuate the area",
            "🔌 Shut down nearby electrical equipment",
            "🧯 Deploy fire suppression if trained to do so",
        ]
        counter_html = f'<div style="font-size:0.8rem;color:#ff8c8c;margin-top:6px;">Detections this session: <strong>{count}</strong></div>' if count else ''
        ts_html      = f'<div style="font-size:0.8rem;color:#8b949e;">Last detected: {ts}</div>' if ts else ''
        st.markdown(f"""
        {sound_js}
        <div class="alert-critical">
            <div class="alert-title">🚨 CRITICAL ALERT — FIRE DETECTED</div>
            <div style="font-size:0.95rem;color:#ff8c8c;font-weight:600;">
                Confidence: {highest_conf*100:.1f}%
            </div>
            {counter_html}{ts_html}
            <div style="font-size:0.8rem;color:#8b949e;margin:10px 0 6px;">RECOMMENDED ACTIONS</div>
            {"".join(f'<div class="alert-action-item">✔ {a}</div>' for a in actions)}
        </div>""", unsafe_allow_html=True)

    elif smoke:
        actions = [
            "🔍 Investigate source of smoke",
            "🚪 Prepare evacuation route",
            "📢 Alert occupants to stand by",
            "🔔 Activate smoke alarm system",
        ]
        st.markdown(f"""
        <div class="alert-warning">
            <div class="alert-title">⚠️ WARNING — SMOKE DETECTED</div>
            <div style="font-size:0.95rem;color:#e3c08c;font-weight:600;">
                Confidence: {highest_conf*100:.1f}%
            </div>
            <div style="font-size:0.8rem;color:#8b949e;margin:10px 0 6px;">RECOMMENDED ACTIONS</div>
            {"".join(f'<div class="alert-action-item">✔ {a}</div>' for a in actions)}
        </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="alert-safe">
            <div class="alert-title">✅ All Clear — No Threats Detected</div>
            <div style="font-size:0.88rem;color:#7ee787;">Area appears safe. Continue monitoring.</div>
        </div>""", unsafe_allow_html=True)


def render_stat_cards(fire, smoke, total, highest_conf, avg_conf, processing_time):
    color = "fire" if fire else ("smoke" if smoke else "green")
    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-label">🔥 Fire</div>
            <div class="stat-value fire">{"Detected" if fire else "Clear"}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">💨 Smoke</div>
            <div class="stat-value smoke">{"Detected" if smoke else "Clear"}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">📦 Total Objects</div>
            <div class="stat-value">{total}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">🎯 Highest Conf</div>
            <div class="stat-value {color}">{highest_conf*100:.1f}%</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">📊 Avg Confidence</div>
            <div class="stat-value">{avg_conf:.1f}%</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">⏱ Processing</div>
            <div class="stat-value">{processing_time:.2f}s</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_conf_distribution(conf_values: list):
    if not conf_values:
        return
    fig = px.histogram(
        x=conf_values, nbins=10,
        labels={"x": "Confidence (%)", "y": "Count"},
        title="📉 Confidence Distribution",
        color_discrete_sequence=["#ff4d4d"],
    )
    fig.update_layout(
        paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
        font=dict(color="#8b949e"),
        xaxis=dict(gridcolor="#21262d"),
        yaxis=dict(gridcolor="#21262d"),
        margin=dict(l=10, r=10, t=40, b=10), height=250,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_gallery():
    snaps = st.session_state.snapshots
    if not snaps:
        st.markdown(
            "<div style='color:#484f58;font-size:0.88rem;padding:16px 0;'>"
            "No fire/smoke snapshots yet.</div>", unsafe_allow_html=True
        )
        return
    cards_html = "<div class='gallery-grid'>"
    for s in reversed(snaps[-24:]):
        badge_color = "#ff4d4d" if s["label"].lower() == "fire" else "#a8b2d8"
        cards_html += f"""
        <div class="gallery-card">
            <img src="data:image/jpeg;base64,{s['img_b64']}"
                 style="width:100%;height:120px;object-fit:cover;" />
            <div class="gallery-meta">
                <strong style="color:{badge_color};">{s['label'].upper()}</strong>
                &nbsp;·&nbsp; {s['conf']*100:.0f}%<br>
                📅 {s['date']}<br>
                🕐 {s['time']}
            </div>
        </div>"""
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)


def render_detection_log():
    logs = st.session_state.detection_log
    if not logs:
        st.markdown(
            "<div style='color:#484f58;font-size:0.88rem;padding:16px 0;'>"
            "No events logged yet.</div>", unsafe_allow_html=True
        )
        return
    rows = ""
    for entry in reversed(logs[-50:]):
        css = "log-fire" if entry["label"].lower() == "fire" else \
              ("log-smoke" if entry["label"].lower() == "smoke" else "log-safe")
        icon = "🔥" if entry["label"].lower() == "fire" else \
               ("💨" if entry["label"].lower() == "smoke" else "✅")
        rows += (
            f'<span class="log-time">{entry["time"]}</span>'
            f'<span class="{css}">{icon} {entry["label"].upper():<10}</span>'
            f'<span style="color:#6e7681;"> {entry["conf"]*100:5.1f}%</span><br>'
        )
    st.markdown(f'<div class="log-box">{rows}</div>', unsafe_allow_html=True)


def render_history_table():
    if not st.session_state.history:
        st.markdown(
            "<div style='color:#484f58;font-size:0.88rem;padding:16px 0;'>"
            "No detections logged yet.</div>", unsafe_allow_html=True
        )
        return
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True, hide_index=True,
        column_config={
            "Time":       st.column_config.TextColumn("⏰ Time"),
            "File":       st.column_config.TextColumn("📁 Source"),
            "Fire":       st.column_config.TextColumn("🔥 Fire"),
            "Smoke":      st.column_config.TextColumn("💨 Smoke"),
            "Objects":    st.column_config.NumberColumn("📦 Objects"),
            "Confidence": st.column_config.TextColumn("🎯 Confidence"),
            "Duration":   st.column_config.TextColumn("⏱ Duration"),
        }
    )


def render_live_charts():
    history = st.session_state.history
    if len(history) < 2:
        st.markdown(
            "<div style='color:#484f58;font-size:0.88rem;padding:16px 0;'>"
            "Run at least 2 detections to see live charts.</div>", unsafe_allow_html=True
        )
        return
    df = pd.DataFrame(history)
    df["conf_val"] = df["Confidence"].str.replace("%", "").astype(float)
    df["seq"]      = range(1, len(df) + 1)
    df["fire_n"]   = (df["Fire"]  == "✅").astype(int)
    df["smoke_n"]  = (df["Smoke"] == "✅").astype(int)

    col1, col2 = st.columns(2)
    with col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=df["seq"], y=df["conf_val"],
            mode="lines+markers",
            line=dict(color="#ff4d4d", width=2),
            marker=dict(size=7, color="#ff8c00"),
            fill="tozeroy", fillcolor="rgba(255,77,77,0.08)"
        ))
        fig1.update_layout(
            title="Confidence Over Detections",
            paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
            font=dict(color="#8b949e"),
            xaxis=dict(gridcolor="#21262d", title="Detection #"),
            yaxis=dict(gridcolor="#21262d", title="Confidence (%)"),
            margin=dict(l=10, r=10, t=40, b=10), height=280,
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fire_t  = int(df["fire_n"].sum())
        smoke_t = int(df["smoke_n"].sum())
        safe_t  = int((df["fire_n"] + df["smoke_n"] == 0).sum())
        fig2 = go.Figure(go.Bar(
            x=["🔥 Fire", "💨 Smoke", "✅ Safe"],
            y=[fire_t, smoke_t, safe_t],
            marker_color=["#ff4d4d", "#a8b2d8", "#3fb950"],
            text=[fire_t, smoke_t, safe_t], textposition="outside",
        ))
        fig2.update_layout(
            title="Detection Breakdown",
            paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
            font=dict(color="#8b949e"),
            xaxis=dict(gridcolor="#21262d"),
            yaxis=dict(gridcolor="#21262d"),
            margin=dict(l=10, r=10, t=40, b=10), height=280,
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)


# =====================================================
# LIVE STREAM DETECTION (Webcam & RTSP shared logic)
# =====================================================

def run_live_detection(source, source_label: str):
    """Shared logic for webcam (source=0) and RTSP (source=rtsp_url string)."""
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        st.error(f"❌ Cannot open source: {source}")
        return

    fps   = cap.get(cv2.CAP_PROP_FPS) or 25
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  or 640
    height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480

    # UI placeholders
    frame_placeholder = st.empty()
    alert_placeholder = st.empty()
    log_placeholder   = st.empty()

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    metric_fire  = col_m1.empty()
    metric_smoke = col_m2.empty()
    metric_conf  = col_m3.empty()
    metric_fps   = col_m4.empty()

    stop_btn = st.button("⏹️  Stop", key="stop_live")

    # Recording state
    rec_writer   = None
    rec_path_cur = ""
    post_counter = 0
    was_threat   = False
    notif_sent   = False

    frame_count   = 0
    t_start       = time.time()
    last_fire     = False
    last_smoke    = False
    last_conf     = 0.0

    Path(rec_save_path).mkdir(parents=True, exist_ok=True)

    while not stop_btn:
        ret, frame = cap.read()
        if not ret:
            st.warning("⚠️ Stream ended or disconnected.")
            break

        results         = model(frame, conf=confidence, verbose=False)
        annotated_frame = results[0].plot()

        fire = smoke = False
        highest_conf = 0.0

        for box in results[0].boxes:
            cls      = int(box.cls[0])
            name     = model.names[cls].lower()
            conf_val = float(box.conf[0])
            highest_conf = max(highest_conf, conf_val)
            if name == "fire":
                fire = True
            elif name == "smoke":
                smoke = True

        threat = fire or smoke
        now_ts = datetime.now()

        # ── Auto-recording ──
        if threat:
            if rec_writer is None:
                rec_writer, rec_path_cur = get_video_writer(
                    rec_save_path, fps, width, height
                )
                st.toast(f"🔴 Recording started → {rec_path_cur}", icon="🎥")
            post_counter = int(rec_post_secs * fps)
            was_threat   = True

        if rec_writer is not None:
            rec_writer.write(annotated_frame)
            if not threat:
                if post_counter > 0:
                    post_counter -= 1
                else:
                    rec_writer.release()
                    rec_writer   = None
                    rec_path_cur = ""
                    was_threat   = False
                    notif_sent   = False
                    st.toast("✅ Recording saved.", icon="💾")

        # ── Snapshot + log + notifications ──
        if threat:
            label = "Fire" if fire else "Smoke"
            if frame_count % 30 == 0:   # snapshot every ~1 sec
                save_snapshot(annotated_frame, label, highest_conf,
                              now_ts.strftime("%Y-%m-%d"),
                              now_ts.strftime("%I:%M:%S %p"))
                add_log(label, highest_conf)
                if fire:
                    st.session_state.fire_count  += 1
                else:
                    st.session_state.smoke_count += 1

            if not notif_sent:
                send_notifications(label, highest_conf, annotated_frame)
                notif_sent = True

        last_fire  = fire
        last_smoke = smoke
        last_conf  = highest_conf

        # ── Display ──
        rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(rgb, channels="RGB", use_container_width=True)

        elapsed = time.time() - t_start
        live_fps = frame_count / elapsed if elapsed > 0 else 0

        metric_fire.metric("🔥 Fire",  "🔴 YES" if fire  else "🟢 No")
        metric_smoke.metric("💨 Smoke", "🟠 YES" if smoke else "🟢 No")
        metric_conf.metric("🎯 Conf",  f"{highest_conf*100:.1f}%")
        metric_fps.metric("⚡ FPS",    f"{live_fps:.1f}")

        # Alert
        if fire:
            alert_placeholder.error(
                f"🚨 **FIRE DETECTED** — {highest_conf*100:.1f}% confidence — "
                f"{now_ts.strftime('%H:%M:%S')}"
            )
        elif smoke:
            alert_placeholder.warning(
                f"⚠️ **SMOKE DETECTED** — {highest_conf*100:.1f}% confidence — "
                f"{now_ts.strftime('%H:%M:%S')}"
            )
        else:
            alert_placeholder.success("✅ All Clear")

        frame_count += 1

    cap.release()
    if rec_writer:
        rec_writer.release()

    # Save session history entry
    st.session_state.history.append({
        "Time":       datetime.now().strftime("%H:%M:%S"),
        "File":       source_label,
        "Fire":       "✅" if last_fire  else "❌",
        "Smoke":      "✅" if last_smoke else "❌",
        "Objects":    st.session_state.fire_count + st.session_state.smoke_count,
        "Confidence": f"{last_conf*100:.1f}%",
        "Duration":   f"{time.time()-t_start:.0f}s",
    })

    st.success("⏹️ Stream stopped.")


# =====================================================
# IMAGE MODE
# =====================================================

if mode == "🖼️  Image Detection":

    uploaded_image = st.file_uploader(
        "Upload an image", type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            image.save(tmp.name)
            image_path = tmp.name

        col_orig, col_result = st.columns(2, gap="medium")
        with col_orig:
            st.markdown("<div class='section-heading'>🖼️ Original Image</div>", unsafe_allow_html=True)
            st.image(image, use_container_width=True)

        if st.session_state.image_result is not None:
            r = st.session_state.image_result
            with col_result:
                st.markdown("<div class='section-heading'>🔍 Detection Result</div>", unsafe_allow_html=True)
                st.image(r["annotated"][:, :, ::-1], use_container_width=True)

        if st.button("🚀  Run Detection"):
            start_time = time.time()
            with st.spinner("Analysing…"):
                results = model.predict(source=image_path, conf=confidence)
            processing_time = time.time() - start_time

            annotated    = results[0].plot()
            fire = smoke = False
            total        = 0
            highest_conf = 0.0
            conf_values  = []

            for box in results[0].boxes:
                total    += 1
                cls       = int(box.cls[0])
                name      = model.names[cls].lower()
                conf_val  = float(box.conf[0])
                conf_values.append(conf_val * 100)
                highest_conf = max(highest_conf, conf_val)
                if name == "fire":  fire  = True
                elif name == "smoke": smoke = True

            avg_conf = sum(conf_values) / len(conf_values) if conf_values else 0.0
            now_ts   = datetime.now()

            st.session_state.image_result = {
                "fire": fire, "smoke": smoke, "total": total,
                "highest_conf": highest_conf, "avg_conf": avg_conf,
                "processing_time": processing_time, "conf_values": conf_values,
                "annotated": annotated, "filename": uploaded_image.name,
                "ts": now_ts.strftime("%H:%M:%S"),
            }

            if fire or smoke:
                label = "Fire" if fire else "Smoke"
                save_snapshot(annotated, label, highest_conf,
                              now_ts.strftime("%Y-%m-%d"),
                              now_ts.strftime("%I:%M:%S %p"))
                add_log(label, highest_conf)
                send_notifications(label, highest_conf, annotated)
                if fire:   st.session_state.fire_count  += 1
                else:      st.session_state.smoke_count += 1

            st.session_state.history.append({
                "Time": now_ts.strftime("%H:%M:%S"),
                "File": uploaded_image.name,
                "Fire":  "✅" if fire  else "❌",
                "Smoke": "✅" if smoke else "❌",
                "Objects": total,
                "Confidence": f"{highest_conf*100:.1f}%",
                "Duration": f"{processing_time:.2f}s",
            })
            st.rerun()

    if st.session_state.image_result is not None:
        r = st.session_state.image_result
        st.markdown("<div class='section-heading'>🚨 Smart Alert Panel</div>", unsafe_allow_html=True)
        build_alert(r["fire"], r["smoke"], r["highest_conf"],
                    count=st.session_state.fire_count,
                    ts=r["ts"],
                    play_sound=r["fire"])
        st.markdown("<div class='section-heading'>📈 Detection Analytics</div>", unsafe_allow_html=True)
        render_stat_cards(r["fire"], r["smoke"], r["total"],
                          r["highest_conf"], r["avg_conf"], r["processing_time"])
        render_conf_distribution(r["conf_values"])

# =====================================================
# VIDEO MODE
# =====================================================

elif mode == "🎥  Video Detection":

    uploaded_video = st.file_uploader(
        "Upload a video", type=["mp4", "avi", "mov"],
        label_visibility="collapsed"
    )

    if uploaded_video is not None:
        st.markdown("<div class='section-heading'>🎥 Original Video</div>", unsafe_allow_html=True)
        st.video(uploaded_video)

        if st.button("🚀  Run Video Detection"):
            input_dir  = Path("temp")
            output_dir = Path("streamlit_output")
            input_dir.mkdir(exist_ok=True)
            output_dir.mkdir(exist_ok=True)

            input_path  = input_dir  / uploaded_video.name
            output_path = output_dir / "detected_video.mp4"

            with open(input_path, "wb") as f:
                f.write(uploaded_video.read())

            cap = cv2.VideoCapture(str(input_path))
            if not cap.isOpened():
                st.error("Unable to open video.")
                st.stop()

            fps          = cap.get(cv2.CAP_PROP_FPS) or 25
            width        = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height       = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

            progress     = st.progress(0)
            frame_no     = 0
            start_time   = time.time()
            fire_frames  = 0; smoke_frames = 0
            all_confs    = []; snap_taken = False
            highest_conf = 0.0
            notif_sent   = False

            while True:
                ret, frame = cap.read()
                if not ret: break

                res             = model(frame, conf=confidence, verbose=False)
                annotated_frame = res[0].plot()
                writer.write(annotated_frame)

                fire = smoke = False
                for box in res[0].boxes:
                    cls      = int(box.cls[0])
                    name     = model.names[cls].lower()
                    conf_val = float(box.conf[0])
                    all_confs.append(conf_val * 100)
                    highest_conf = max(highest_conf, conf_val)
                    if name == "fire":
                        fire = True; fire_frames += 1
                    elif name == "smoke":
                        smoke = True; smoke_frames += 1

                if (fire or smoke) and not snap_taken:
                    label = "Fire" if fire else "Smoke"
                    save_snapshot(annotated_frame, label, highest_conf)
                    add_log(label, highest_conf)
                    snap_taken = True
                    if not notif_sent:
                        send_notifications(label, highest_conf, annotated_frame)
                        notif_sent = True

                frame_no += 1
                if total_frames > 0:
                    progress.progress(min(frame_no / total_frames, 1.0))

            cap.release(); writer.release()
            processing_time = time.time() - start_time
            progress.empty()

            browser_video = output_dir / "detected_video_browser.mp4"
            result = subprocess.run([
                "ffmpeg", "-y", "-i", str(output_path),
                "-vcodec", "libx264", "-profile:v", "baseline",
                "-level", "3.0", "-pix_fmt", "yuv420p",
                "-crf", "23", "-preset", "fast",
                "-acodec", "aac", "-movflags", "+faststart",
                str(browser_video)
            ], capture_output=True, text=True)

            video_b64 = None
            if result.returncode == 0 and browser_video.exists() and browser_video.stat().st_size > 0:
                with open(browser_video, "rb") as vf:
                    video_b64 = base64.b64encode(vf.read()).decode()

            fire_detected  = fire_frames  > 0
            smoke_detected = smoke_frames > 0
            avg_conf       = sum(all_confs) / len(all_confs) if all_confs else 0.0
            now_ts         = datetime.now()

            st.session_state.video_result = {
                "fire": fire_detected, "smoke": smoke_detected,
                "fire_frames": fire_frames, "smoke_frames": smoke_frames,
                "frame_no": frame_no, "highest_conf": highest_conf,
                "avg_conf": avg_conf, "processing_time": processing_time,
                "all_confs": all_confs, "video_b64": video_b64,
                "ffmpeg_ok": result.returncode == 0, "ffmpeg_err": result.stderr,
                "filename": uploaded_video.name,
            }

            if fire_detected:  st.session_state.fire_count  += 1
            if smoke_detected: st.session_state.smoke_count += 1

            st.session_state.history.append({
                "Time": now_ts.strftime("%H:%M:%S"),
                "File": uploaded_video.name,
                "Fire":  "✅" if fire_detected  else "❌",
                "Smoke": "✅" if smoke_detected else "❌",
                "Objects": fire_frames + smoke_frames,
                "Confidence": f"{highest_conf*100:.1f}%",
                "Duration": f"{processing_time:.2f}s",
            })
            st.rerun()

    if st.session_state.video_result is not None:
        r = st.session_state.video_result
        st.markdown("<div class='section-heading'>🎬 Detection Result</div>", unsafe_allow_html=True)
        if not r["ffmpeg_ok"]:
            st.error("❌ FFmpeg conversion failed.")
            st.code(r["ffmpeg_err"])
        elif r["video_b64"]:
            st.markdown(
                f'<video width="100%" controls autoplay>'
                f'<source src="data:video/mp4;base64,{r["video_b64"]}" type="video/mp4">'
                f'</video>', unsafe_allow_html=True
            )

        st.markdown("<div class='section-heading'>🚨 Smart Alert Panel</div>", unsafe_allow_html=True)
        build_alert(r["fire"], r["smoke"], r["highest_conf"],
                    play_sound=r["fire"])
        st.markdown("<div class='section-heading'>📈 Video Analytics</div>", unsafe_allow_html=True)
        render_stat_cards(r["fire"], r["smoke"],
                          r["fire_frames"] + r["smoke_frames"],
                          r["highest_conf"], r["avg_conf"], r["processing_time"])
        render_conf_distribution(r["all_confs"])

# =====================================================
# LIVE WEBCAM MODE
# =====================================================

elif mode == "📹  Live Webcam":
    st.markdown("<div class='section-heading'>📹 Live Webcam Detection</div>", unsafe_allow_html=True)
    st.info("💡 Click **Start** to activate your laptop webcam. Bounding boxes, confidence scores, and alerts appear in real time.")

    col_info1, col_info2 = st.columns(2)
    with col_info1:
        cam_index = st.number_input("Camera index (0 = default webcam)", min_value=0, max_value=10, value=0, step=1)
    with col_info2:
        st.markdown("<br>", unsafe_allow_html=True)
        start_webcam = st.button("▶️  Start Webcam")

    if start_webcam:
        run_live_detection(int(cam_index), f"Webcam [{cam_index}]")

# =====================================================
# IP / RTSP CAMERA MODE
# =====================================================

elif mode == "🌐  IP / RTSP Camera":
    st.markdown("<div class='section-heading'>🌐 IP / RTSP Camera Detection</div>", unsafe_allow_html=True)
    st.info("💡 Supports Hikvision, Dahua, Uniview, Axis, and any ONVIF/RTSP-compatible camera.")

    rtsp_url = st.text_input(
        "RTSP / IP Stream URL",
        placeholder="rtsp://username:password@192.168.1.100:554/Streaming/Channels/101",
        help="Examples:\n• Hikvision: rtsp://admin:pass@192.168.1.64:554/Streaming/Channels/101\n• Dahua: rtsp://admin:pass@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0\n• Generic RTSP: rtsp://192.168.1.x:554/stream"
    )

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("**Common RTSP formats:**")
        st.code("Hikvision : rtsp://user:pass@IP:554/Streaming/Channels/101")
        st.code("Dahua     : rtsp://user:pass@IP:554/cam/realmonitor?channel=1&subtype=0")
        st.code("Axis      : rtsp://user:pass@IP/axis-media/media.amp")

    with col_r2:
        test_btn  = st.button("🔌 Test Connection")
        start_btn = st.button("▶️  Start Stream")

    if test_btn and rtsp_url:
        with st.spinner("Testing connection…"):
            cap_test = cv2.VideoCapture(rtsp_url)
            if cap_test.isOpened():
                ret, _ = cap_test.read()
                cap_test.release()
                if ret:
                    st.success("✅ Connection successful! Stream is live.")
                else:
                    st.error("❌ Connected but could not read frames. Check URL.")
            else:
                st.error("❌ Cannot connect. Check URL, credentials, and network.")

    if start_btn and rtsp_url:
        run_live_detection(rtsp_url, f"RTSP: {rtsp_url[:40]}…")
    elif start_btn and not rtsp_url:
        st.warning("⚠️ Please enter a valid RTSP URL first.")

# =====================================================
# DETECTION LOG
# =====================================================

st.markdown("<div class='section-heading'>📋 Live Detection Log</div>", unsafe_allow_html=True)
render_detection_log()

# =====================================================
# DETECTION HISTORY
# =====================================================

st.markdown("<div class='section-heading'>📜 Detection History</div>", unsafe_allow_html=True)
render_history_table()

# =====================================================
# SNAPSHOT GALLERY
# =====================================================

st.markdown("<div class='section-heading'>📸 Recent Alerts — Snapshot Gallery</div>", unsafe_allow_html=True)
render_gallery()

# =====================================================
# LIVE CHARTS
# =====================================================

st.markdown("<div class='section-heading'>📊 Live Charts</div>", unsafe_allow_html=True)
render_live_charts()
