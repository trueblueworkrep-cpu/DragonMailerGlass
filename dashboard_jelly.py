"""
Jelly Dashboard - Animated Analytics Dashboard with Theme Support.
Supports Glass, Dark, and Light interface modes.
"""

import json
from pathlib import Path

import streamlit as st

try:
    from jelly_components import (
        jelly_blob_bounce,
        jelly_blob_intensity,
        jelly_blob_metric,
        jelly_blob_progress,
        jelly_blob_volume,
        jelly_metric,
        jelly_notification,
        jelly_stats_card,
    )
    JELLY_AVAILABLE = True
except ImportError:
    JELLY_AVAILABLE = False

CONFIG_DIR = Path(__file__).parent / "config"
SENT_MESSAGES_FILE = CONFIG_DIR / "sent_messages.json"
SETTINGS_FILE = CONFIG_DIR / "settings.json"
THEME_OPTIONS = ["Glass", "Dark", "Light"]


def load_json(filepath, default=None):
    """Load JSON file safely."""
    if default is None:
        default = {}
    try:
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default


def save_json(filepath, data):
    """Save JSON file safely."""
    filepath.parent.mkdir(exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_current_theme():
    """Get current UI theme from settings with healing for stale values."""
    settings = load_json(SETTINGS_FILE, {})
    theme = settings.get("theme", "Glass")
    if theme not in THEME_OPTIONS:
        theme = "Glass"
        settings["theme"] = theme
        settings["available_themes"] = THEME_OPTIONS
        save_json(SETTINGS_FILE, settings)
    return theme


def get_theme_components():
    """Get component functions for the active dashboard."""
    if not JELLY_AVAILABLE:
        st.error("Jelly components not available")
        return None
    return {
        "blob_metric": jelly_blob_metric,
        "blob_intensity": jelly_blob_intensity,
        "blob_volume": jelly_blob_volume,
        "blob_progress": jelly_blob_progress,
        "blob_bounce": jelly_blob_bounce,
        "metric": jelly_metric,
        "notification": jelly_notification,
        "stats_card": jelly_stats_card,
    }


def get_theme_visuals(theme):
    """Theme-tuned colors for dashboard visuals."""
    if theme == "Dark":
        return {
            "header_color": "#22c55e",
            "header_glow": "text-shadow: 0 0 20px rgba(34, 197, 94, 0.25);",
            "progress_scheme": "teal",
            "accent": "#22c55e",
        }
    if theme == "Light":
        return {
            "header_color": "#0ea5e9",
            "header_glow": "",
            "progress_scheme": "orange",
            "accent": "#0ea5e9",
        }
    return {
        "header_color": "#00d4ff",
        "header_glow": "text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);",
        "progress_scheme": "blue_orange",
        "accent": "#00d4ff",
    }


def render_theme_selector():
    """Render theme selector in sidebar."""
    st.sidebar.markdown("### 🎨 Theme Settings")
    current_theme = get_current_theme()

    selected_theme = st.sidebar.selectbox(
        "Choose Theme:",
        THEME_OPTIONS,
        index=THEME_OPTIONS.index(current_theme),
        key="theme_selector",
    )

    if selected_theme != current_theme:
        settings = load_json(SETTINGS_FILE, {})
        settings["theme"] = selected_theme
        settings["available_themes"] = THEME_OPTIONS
        save_json(SETTINGS_FILE, settings)
        st.rerun()

    return selected_theme


def render():
    """Render the analytics dashboard."""
    current_theme = render_theme_selector()
    visuals = get_theme_visuals(current_theme)
    components = get_theme_components()

    if not components:
        return

    st.markdown(
        f"""
    <style>
    .dashboard-header {{
        color: {visuals["header_color"]};
        font-family: 'Segoe UI', sans-serif;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 24px;
        {visuals["header_glow"]}
    }}
    </style>
    <div class="dashboard-header">✨ Campaign Overview</div>
    """,
        unsafe_allow_html=True,
    )

    st.sidebar.info(f"🎨 Active Theme: **{current_theme}**")

    sent_log = load_json(SENT_MESSAGES_FILE, {"messages": []})
    messages = sent_log.get("messages", [])

    total_emails = sum(1 for m in messages if m.get("type") == "email")
    total_sms = sum(1 for m in messages if m.get("type") in ["sms", "azure_sms"])
    total_azure = sum(1 for m in messages if m.get("type") == "azure_sms")
    total_gateway = total_sms - total_azure
    total_success = sum(m.get("success", 0) for m in messages)
    total_failed = sum(m.get("failed", 0) for m in messages)
    total_all = total_success + total_failed

    success_rate = (total_success / total_all) if total_all > 0 else 0.5
    bounce_rate = (total_failed / total_all) if total_all > 0 else 0.075

    col1, col2 = st.columns(2)
    with col1:
        components["blob_metric"]("Campaign Overview", f"{total_all:,}", "emails sent this month")
    with col2:
        components["blob_intensity"]("Theme Intensity")

    col1, col2 = st.columns(2)
    with col1:
        components["blob_volume"]("Volume")
    with col2:
        components["blob_progress"](success_rate, "Email Send Rate", visuals["progress_scheme"])

    col1, col2 = st.columns(2)
    with col1:
        components["blob_bounce"](bounce_rate, "Bounce Rate")
    with col2:
        components["blob_bounce"](bounce_rate * 0.8, "Bounce rate")

    st.markdown("---")
    components["stats_card"](
        "📊 Detailed Statistics",
        [
            {"label": "Total Sent", "value": str(total_all)},
            {"label": "Emails", "value": str(total_emails)},
            {"label": "Gateway SMS", "value": str(total_gateway)},
            {"label": "Azure SMS", "value": str(total_azure)},
            {"label": "Success", "value": str(total_success)},
            {"label": "Failed", "value": str(total_failed)},
        ],
        visuals["accent"],
    )

    st.markdown("### 📋 Recent Activity")
    if messages:
        for msg in reversed(messages[-5:]):
            icon = "📧" if msg.get("type") == "email" else "📱"
            timestamp = msg.get("timestamp", "Unknown")[:16].replace("T", " ")
            msg_text = f"{icon} {msg.get('subject', 'SMS')[:30]} - {timestamp}"

            notif_type = "success" if msg.get("failed", 0) == 0 else "warning"
            components["notification"](msg_text, notif_type)
    else:
        components["notification"]("No messages sent yet - Start sending to see activity!", "info")


if __name__ == "__main__":
    render()
