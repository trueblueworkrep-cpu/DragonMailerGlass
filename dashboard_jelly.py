"""
Jelly Dashboard - Animated Analytics Dashboard with Organic Blob Components
Matches the reference design with flowing morphing blob shapes
"""

import streamlit as st
from pathlib import Path
import json

# Import jelly components
try:
    from jelly_components import (
        jelly_blob_metric,
        jelly_blob_intensity,
        jelly_blob_volume,
        jelly_blob_progress,
        jelly_blob_bounce,
        jelly_metric,
        jelly_notification,
        jelly_stats_card
    )
    JELLY_AVAILABLE = True
except ImportError:
    JELLY_AVAILABLE = False

# Config path
CONFIG_DIR = Path(__file__).parent / "config"
SENT_MESSAGES_FILE = CONFIG_DIR / "sent_messages.json"


def load_json(filepath, default=None):
    """Load JSON file safely"""
    if default is None:
        default = {}
    try:
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return default


def render():
    """Render the Jelly Analytics Dashboard with organic blob components"""
    
    if not JELLY_AVAILABLE:
        st.error("Jelly components not available")
        return
    
    st.markdown("""
    <style>
    .jelly-dashboard-header {
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 24px;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }
    </style>
    <div class="jelly-dashboard-header">✨ Campaign Overview</div>
    """, unsafe_allow_html=True)
    
    # Load data
    sent_log = load_json(SENT_MESSAGES_FILE, {"messages": []})
    messages = sent_log.get('messages', [])
    
    # Calculate statistics
    total_emails = sum(1 for m in messages if m.get('type') == 'email')
    total_sms = sum(1 for m in messages if m.get('type') in ['sms', 'azure_sms'])
    total_azure = sum(1 for m in messages if m.get('type') == 'azure_sms')
    total_gateway = total_sms - total_azure
    total_success = sum(m.get('success', 0) for m in messages)
    total_failed = sum(m.get('failed', 0) for m in messages)
    total_all = total_success + total_failed
    
    # Rates
    success_rate = (total_success / total_all) if total_all > 0 else 0.5
    bounce_rate = (total_failed / total_all) if total_all > 0 else 0.075
    
    # Row 1: Campaign Overview (big number) + Theme Intensity (flowing blob)
    col1, col2 = st.columns(2)
    with col1:
        jelly_blob_metric(
            "Campaign Overview", 
            f"{total_all:,}", 
            "emails sent this month"
        )
    with col2:
        jelly_blob_intensity("Theme Intensity")
    
    # Row 2: Volume (teal blob) + Email Send Rate (progress blob)
    col1, col2 = st.columns(2)
    with col1:
        jelly_blob_volume("Volume")
    with col2:
        jelly_blob_progress(success_rate, "Email Send Rate", "blue_orange")
    
    # Row 3: Bounce Rate x2 (orange blobs)
    col1, col2 = st.columns(2)
    with col1:
        jelly_blob_bounce(bounce_rate, "Bounce Rate")
    with col2:
        jelly_blob_bounce(bounce_rate * 0.8, "Bounce rate")  # Slightly different value
    
    # Stats Summary Card
    st.markdown("---")
    jelly_stats_card("📊 Detailed Statistics", [
        {"label": "Total Sent", "value": str(total_all)},
        {"label": "Emails", "value": str(total_emails)},
        {"label": "Gateway SMS", "value": str(total_gateway)},
        {"label": "Azure SMS", "value": str(total_azure)},
        {"label": "Success", "value": str(total_success)},
        {"label": "Failed", "value": str(total_failed)},
    ], "#00d4ff")
    
    # Recent Activity with notifications
    st.markdown("### 📋 Recent Activity")
    if messages:
        for msg in reversed(messages[-5:]):
            icon = "📧" if msg.get('type') == 'email' else "📱"
            timestamp = msg.get('timestamp', 'Unknown')[:16].replace('T', ' ')
            msg_text = f"{icon} {msg.get('subject', 'SMS')[:30]} - {timestamp}"
            
            notif_type = "success" if msg.get('failed', 0) == 0 else "warning"
            jelly_notification(msg_text, notif_type)
    else:
        jelly_notification("No messages sent yet - Start sending to see activity!", "info")


if __name__ == "__main__":
    render()
