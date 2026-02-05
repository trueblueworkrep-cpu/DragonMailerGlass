"""
Jelly Components - Organic Fluid Blob UI Elements for Dragon Mailer
Beautiful morphing blob shapes with CSS-only animations (no SVG path animations)
"""

import streamlit as st
import random


def jelly_blob_metric(label: str, value: str, sublabel: str = "", blob_type: str = "blue_orange"):
    """
    Display an organic fluid blob metric card.
    """
    uid = f"bm{random.randint(10000, 99999)}"
    
    st.markdown(f"""
    <style>
    .jcard{uid} {{
        background: rgba(15, 20, 35, 0.85);
        border-radius: 24px;
        padding: 24px;
        margin: 12px 0;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    }}
    .jlbl{uid} {{
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        font-weight: 500;
        margin-bottom: 16px;
    }}
    .jval{uid} {{
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        font-size: 48px;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 8px;
    }}
    .jsub{uid} {{
        color: rgba(255, 255, 255, 0.5);
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
    }}
    </style>
    <div class="jcard{uid}">
        <div class="jlbl{uid}">{label}</div>
        <div class="jval{uid}">{value}</div>
        <div class="jsub{uid}">{sublabel}</div>
    </div>
    """, unsafe_allow_html=True)


def jelly_blob_intensity(label: str = "Theme Intensity"):
    """
    Display a flowing blue-to-orange intensity blob using CSS gradients.
    """
    uid = f"bi{random.randint(10000, 99999)}"
    
    st.markdown(f"""
    <style>
    @keyframes morph{uid} {{
        0%, 100% {{ border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }}
        25% {{ border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }}
        50% {{ border-radius: 50% 50% 40% 60% / 40% 50% 60% 50%; }}
        75% {{ border-radius: 40% 60% 50% 50% / 60% 40% 50% 60%; }}
    }}
    @keyframes glow{uid} {{
        0%, 100% {{ box-shadow: 0 0 25px rgba(59, 130, 246, 0.5), 0 0 50px rgba(249, 115, 22, 0.3); }}
        50% {{ box-shadow: 0 0 40px rgba(59, 130, 246, 0.7), 0 0 70px rgba(249, 115, 22, 0.5); }}
    }}
    .icard{uid} {{
        background: rgba(15, 20, 35, 0.85);
        border-radius: 24px;
        padding: 24px;
        margin: 12px 0;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    }}
    .ilbl{uid} {{
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        font-weight: 500;
        margin-bottom: 20px;
    }}
    .iblob{uid} {{
        width: 100%;
        height: 70px;
        background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 35%, #f97316 70%, #ea580c 100%);
        animation: morph{uid} 8s ease-in-out infinite, glow{uid} 3s ease-in-out infinite;
    }}
    </style>
    <div class="icard{uid}">
        <div class="ilbl{uid}">{label}</div>
        <div class="iblob{uid}"></div>
    </div>
    """, unsafe_allow_html=True)


def jelly_blob_volume(label: str = "Volume", show_icon: bool = True):
    """
    Display a teal organic blob volume indicator.
    """
    uid = f"bv{random.randint(10000, 99999)}"
    
    icon_html = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.6"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>' if show_icon else ""
    
    st.markdown(f"""
    <style>
    @keyframes vmorph{uid} {{
        0%, 100% {{ border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%; transform: scale(1); }}
        25% {{ border-radius: 60% 40% 60% 40% / 50% 60% 40% 50%; transform: scale(1.02); }}
        50% {{ border-radius: 40% 60% 40% 60% / 40% 50% 60% 50%; transform: scale(0.98); }}
        75% {{ border-radius: 55% 45% 55% 45% / 55% 45% 55% 45%; transform: scale(1.01); }}
    }}
    @keyframes vglow{uid} {{
        0%, 100% {{ box-shadow: 0 0 30px rgba(6, 182, 212, 0.4); }}
        50% {{ box-shadow: 0 0 50px rgba(6, 182, 212, 0.6); }}
    }}
    .vcard{uid} {{
        background: rgba(15, 20, 35, 0.85);
        border-radius: 24px;
        padding: 24px;
        margin: 12px 0;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    }}
    .vlbl{uid} {{
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        font-weight: 500;
        margin-bottom: 20px;
    }}
    .vwrap{uid} {{
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: 10px;
    }}
    .vblob{uid} {{
        width: 140px;
        height: 70px;
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 50%, #0e7490 100%);
        animation: vmorph{uid} 6s ease-in-out infinite, vglow{uid} 3s ease-in-out infinite;
    }}
    </style>
    <div class="vcard{uid}">
        <div class="vlbl{uid}">{label}</div>
        <div class="vwrap{uid}">
            <div class="vblob{uid}"></div>
            {icon_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def jelly_blob_progress(value: float, label: str = "Email Send Rate", color_scheme: str = "blue_orange"):
    """
    Display a flowing progress blob with percentage.
    """
    uid = f"bp{random.randint(10000, 99999)}"
    percentage = int(value * 100)
    
    if color_scheme == "orange":
        gradient = "linear-gradient(90deg, #f97316 0%, #ea580c 50%, #c2410c 100%)"
        shadow = "rgba(249, 115, 22, 0.5)"
    elif color_scheme == "teal":
        gradient = "linear-gradient(90deg, #06b6d4 0%, #0891b2 50%, #0e7490 100%)"
        shadow = "rgba(6, 182, 212, 0.5)"
    else:
        gradient = "linear-gradient(90deg, #3b82f6 0%, #60a5fa 30%, #f97316 70%, #ea580c 100%)"
        shadow = "rgba(59, 130, 246, 0.4)"
    
    st.markdown(f"""
    <style>
    @keyframes pmorph{uid} {{
        0%, 100% {{ border-radius: 60% 40% 50% 50% / 50% 50% 50% 50%; }}
        25% {{ border-radius: 50% 50% 60% 40% / 40% 60% 40% 60%; }}
        50% {{ border-radius: 40% 60% 40% 60% / 60% 40% 60% 40%; }}
        75% {{ border-radius: 50% 50% 50% 50% / 50% 50% 50% 50%; }}
    }}
    @keyframes pglow{uid} {{
        0%, 100% {{ box-shadow: 0 0 20px {shadow}; }}
        50% {{ box-shadow: 0 0 35px {shadow}; }}
    }}
    .pcard{uid} {{
        background: rgba(15, 20, 35, 0.85);
        border-radius: 24px;
        padding: 24px;
        margin: 12px 0;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    }}
    .plbl{uid} {{
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        font-weight: 500;
        margin-bottom: 16px;
    }}
    .pwrap{uid} {{
        display: flex;
        align-items: center;
        gap: 20px;
    }}
    .pblob{uid} {{
        flex: 1;
        height: 50px;
        background: {gradient};
        animation: pmorph{uid} 6s ease-in-out infinite, pglow{uid} 3s ease-in-out infinite;
    }}
    .pval{uid} {{
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Segoe UI', sans-serif;
        font-size: 28px;
        font-weight: 600;
        min-width: 70px;
        text-align: right;
    }}
    .pbar{uid} {{
        height: 6px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
        margin-top: 12px;
        overflow: hidden;
    }}
    .pfill{uid} {{
        height: 100%;
        width: {percentage}%;
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
        border-radius: 3px;
    }}
    </style>
    <div class="pcard{uid}">
        <div class="plbl{uid}">{label}</div>
        <div class="pwrap{uid}">
            <div class="pblob{uid}"></div>
            <div class="pval{uid}">{percentage}%</div>
        </div>
        <div class="pbar{uid}"><div class="pfill{uid}"></div></div>
    </div>
    """, unsafe_allow_html=True)


def jelly_blob_bounce(value: float, label: str = "Bounce Rate"):
    """
    Display an orange bounce rate blob indicator.
    """
    uid = f"bb{random.randint(10000, 99999)}"
    percentage = round(value * 100, 1)
    
    st.markdown(f"""
    <style>
    @keyframes bmorph{uid} {{
        0%, 100% {{ border-radius: 60% 40% 50% 50% / 50% 50% 50% 50%; transform: scale(1); }}
        25% {{ border-radius: 50% 50% 60% 40% / 40% 60% 40% 60%; transform: scale(1.03); }}
        50% {{ border-radius: 40% 60% 40% 60% / 60% 40% 60% 40%; transform: scale(0.97); }}
        75% {{ border-radius: 55% 45% 55% 45% / 50% 50% 50% 50%; transform: scale(1.01); }}
    }}
    @keyframes bglow{uid} {{
        0%, 100% {{ box-shadow: 0 0 15px rgba(249, 115, 22, 0.5); }}
        50% {{ box-shadow: 0 0 30px rgba(249, 115, 22, 0.7); }}
    }}
    .bcard{uid} {{
        background: rgba(15, 20, 35, 0.85);
        border-radius: 24px;
        padding: 24px;
        margin: 12px 0;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    }}
    .blbl{uid} {{
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        font-weight: 500;
        margin-bottom: 16px;
    }}
    .bwrap{uid} {{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .bblob{uid} {{
        width: 180px;
        height: 60px;
        background: linear-gradient(90deg, #f97316 0%, #ea580c 50%, #c2410c 100%);
        animation: bmorph{uid} 5s ease-in-out infinite, bglow{uid} 3s ease-in-out infinite;
    }}
    .bval{uid} {{
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Segoe UI', sans-serif;
        font-size: 28px;
        font-weight: 600;
    }}
    </style>
    <div class="bcard{uid}">
        <div class="blbl{uid}">{label}</div>
        <div class="bwrap{uid}">
            <div class="bblob{uid}"></div>
            <div class="bval{uid}">{percentage}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def jelly_metric(label: str, value: str, delta: str = None, color: str = "#00d4ff"):
    """Simple glowing metric card."""
    uid = f"jm{random.randint(10000, 99999)}"
    
    delta_html = ""
    if delta:
        is_positive = not delta.startswith('-')
        delta_color = "#4ade80" if is_positive else "#f87171"
        delta_icon = "↑" if is_positive else "↓"
        delta_html = f'<div style="color:{delta_color};font-size:14px;margin-top:8px;">{delta_icon} {delta}</div>'
    
    st.markdown(f"""
    <style>
    @keyframes mglow{uid} {{
        0%, 100% {{ box-shadow: 0 0 20px {color}30; }}
        50% {{ box-shadow: 0 0 35px {color}50; }}
    }}
    .mcard{uid} {{
        background: rgba(15, 20, 35, 0.85);
        border-radius: 20px;
        padding: 24px;
        margin: 10px 0;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        animation: mglow{uid} 3s ease-in-out infinite;
    }}
    .mlbl{uid} {{
        color: rgba(255, 255, 255, 0.6);
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }}
    .mval{uid} {{
        color: {color};
        font-family: 'Segoe UI', sans-serif;
        font-size: 36px;
        font-weight: 700;
    }}
    </style>
    <div class="mcard{uid}">
        <div class="mlbl{uid}">{label}</div>
        <div class="mval{uid}">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def jelly_notification(message: str, type: str = "info", color: str = None):
    """Display a notification with glow effect."""
    uid = f"jn{random.randint(10000, 99999)}"
    
    type_colors = {"info": "#3b82f6", "success": "#22c55e", "warning": "#f59e0b", "error": "#ef4444"}
    type_icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
    
    c = color or type_colors.get(type, "#3b82f6")
    icon = type_icons.get(type, "ℹ️")
    
    st.markdown(f"""
    <style>
    @keyframes nslide{uid} {{
        0% {{ transform: translateX(-20px); opacity: 0; }}
        100% {{ transform: translateX(0); opacity: 1; }}
    }}
    .nbox{uid} {{
        background: rgba(15, 20, 35, 0.9);
        border-radius: 12px;
        padding: 14px 18px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid {c}40;
        border-left: 4px solid {c};
        display: flex;
        align-items: center;
        gap: 12px;
        animation: nslide{uid} 0.4s ease-out;
        box-shadow: 0 4px 20px {c}20;
    }}
    .ntxt{uid} {{
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
    }}
    </style>
    <div class="nbox{uid}">
        <span style="font-size:18px;">{icon}</span>
        <span class="ntxt{uid}">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def jelly_loading(text: str = "Loading...", color: str = "#00d4ff"):
    """Display animated loading indicator."""
    uid = f"jl{random.randint(10000, 99999)}"
    
    st.markdown(f"""
    <style>
    @keyframes lbounce{uid} {{
        0%, 100% {{ transform: translateY(0) scale(1); border-radius: 50%; }}
        50% {{ transform: translateY(-15px) scale(0.9); border-radius: 40% 60% 60% 40%; }}
    }}
    .lbox{uid} {{
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 30px;
        background: rgba(15, 20, 35, 0.85);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin: 20px 0;
    }}
    .ldots{uid} {{
        display: flex;
        gap: 12px;
        margin-bottom: 15px;
    }}
    .ldot{uid} {{
        width: 16px;
        height: 16px;
        background: linear-gradient(135deg, {color}, {color}aa);
        animation: lbounce{uid} 1s ease-in-out infinite;
        box-shadow: 0 0 15px {color}60;
        border-radius: 50%;
    }}
    .ldot{uid}:nth-child(1) {{ animation-delay: 0s; }}
    .ldot{uid}:nth-child(2) {{ animation-delay: 0.15s; }}
    .ldot{uid}:nth-child(3) {{ animation-delay: 0.3s; }}
    .ltxt{uid} {{
        color: rgba(255, 255, 255, 0.7);
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
    }}
    </style>
    <div class="lbox{uid}">
        <div class="ldots{uid}">
            <div class="ldot{uid}"></div>
            <div class="ldot{uid}"></div>
            <div class="ldot{uid}"></div>
        </div>
        <div class="ltxt{uid}">{text}</div>
    </div>
    """, unsafe_allow_html=True)


def jelly_progress(value: float, label: str = "Progress", color: str = "#00d4ff"):
    """Simple jelly progress bar using blob style."""
    jelly_blob_progress(value, label, "blue_orange")


def jelly_gauge(value: float, max_value: float = 100, label: str = "Gauge", color: str = "#00d4ff", suffix: str = "%"):
    """Gauge using blob style."""
    percentage = (value / max_value) if max_value > 0 else 0
    jelly_blob_bounce(percentage, label)


def jelly_stats_card(title: str, stats: list, color: str = "#00d4ff"):
    """Stats card with multiple values."""
    uid = f"js{random.randint(10000, 99999)}"
    
    stats_items = ""
    for stat in stats:
        val = stat.get('value', '0')
        lbl = stat.get('label', '')
        stats_items += f'<div class="sitem{uid}"><div class="sval{uid}">{val}</div><div class="slbl{uid}">{lbl}</div></div>'
    
    st.markdown(f"""
    <style>
    .scard{uid} {{
        background: rgba(15, 20, 35, 0.85);
        border-radius: 24px;
        padding: 28px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        margin: 15px 0;
    }}
    .stitle{uid} {{
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }}
    .sgrid{uid} {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
        gap: 20px;
    }}
    .sitem{uid} {{
        text-align: center;
    }}
    .sval{uid} {{
        color: {color};
        font-size: 28px;
        font-weight: 700;
    }}
    .slbl{uid} {{
        color: rgba(255, 255, 255, 0.5);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }}
    </style>
    <div class="scard{uid}">
        <div class="stitle{uid}">{title}</div>
        <div class="sgrid{uid}">{stats_items}</div>
    </div>
    """, unsafe_allow_html=True)


def jelly_slider_display(value: float, min_val: float = 0, max_val: float = 100, 
                          label: str = "Value", color: str = "#00d4ff", suffix: str = ""):
    """Display a value as a blob progress."""
    percentage = (value - min_val) / (max_val - min_val) if (max_val - min_val) > 0 else 0
    jelly_blob_progress(percentage, f"{label}: {value}{suffix}", "blue_orange")


def jelly_button(text: str, key: str = None, color: str = "#00d4ff", icon: str = ""):
    """Display a styled button (visual only)."""
    uid = f"jb{random.randint(10000, 99999)}"
    
    st.markdown(f"""
    <style>
    .jbtn{uid} {{
        background: linear-gradient(135deg, {color}90, {color}cc);
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        color: white;
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 0 20px {color}40;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }}
    </style>
    <button class="jbtn{uid}">{icon} {text}</button>
    """, unsafe_allow_html=True)


__all__ = [
    'jelly_blob_metric', 'jelly_blob_intensity', 'jelly_blob_volume',
    'jelly_blob_progress', 'jelly_blob_bounce', 'jelly_metric',
    'jelly_notification', 'jelly_loading', 'jelly_progress',
    'jelly_gauge', 'jelly_stats_card', 'jelly_slider_display', 'jelly_button'
]
