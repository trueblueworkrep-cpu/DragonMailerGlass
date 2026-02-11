"""
Skeuomorphic Components - 3D Realistic UI Elements for Dragon Mailer
Rich depth, beveled edges, and realistic material appearance
"""

import streamlit as st
import random


def skeu_blob_metric(label: str, value: str, sublabel: str = "", blob_type: str = "metallic"):
    """
    Display a skeuomorphic 3D metric card with embossed effect.
    """
    uid = f"sm{random.randint(10000, 99999)}"
    
    st.markdown(f"""
    <style>
    .skcard{uid} {{
        background: linear-gradient(145deg, #f5f5f5, #e8e8e8);
        border-radius: 16px;
        padding: 28px;
        margin: 12px 0;
        box-shadow: 
            8px 8px 16px #d0d0d0,
            -8px -8px 16px #ffffff,
            inset 1px 1px 0 rgba(255, 255, 255, 0.8),
            inset -1px -1px 0 rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }}
    .sklbl{uid} {{
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
        opacity: 0.7;
    }}
    .skval{uid} {{
        color: #1a1a1a;
        font-family: 'Segoe UI', sans-serif;
        font-size: 48px;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 8px;
    }}
    .sksub{uid} {{
        color: #666666;
        font-family: 'Segoe UI', sans-serif;
        font-size: 12px;
    }}
    </style>
    <div class="skcard{uid}">
        <div class="sklbl{uid}">{label}</div>
        <div class="skval{uid}">{value}</div>
        <div class="sksub{uid}">{sublabel}</div>
    </div>
    """, unsafe_allow_html=True)


def skeu_blob_intensity(label: str = "Theme Intensity"):
    """
    Display a skeuomorphic intensity slider with 3D depth.
    """
    uid = f"si{random.randint(10000, 99999)}"
    
    st.markdown(f"""
    <style>
    .sicard{uid} {{
        background: linear-gradient(145deg, #f5f5f5, #e8e8e8);
        border-radius: 16px;
        padding: 28px;
        margin: 12px 0;
        box-shadow: 
            8px 8px 16px #d0d0d0,
            -8px -8px 16px #ffffff,
            inset 1px 1px 0 rgba(255, 255, 255, 0.8),
            inset -1px -1px 0 rgba(0, 0, 0, 0.05);
    }}
    .silbl{uid} {{
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 20px;
        opacity: 0.7;
    }}
    .sitrack{uid} {{
        background: linear-gradient(to bottom, #e0e0e0, #f0f0f0);
        border-radius: 12px;
        height: 24px;
        position: relative;
        box-shadow: 
            inset 3px 3px 6px #cccccc,
            inset -3px -3px 6px #ffffff;
        overflow: hidden;
    }}
    .sifill{uid} {{
        height: 100%;
        width: 65%;
        background: linear-gradient(90deg, #ff6b35, #ff8c42, #ffa500);
        box-shadow: inset 1px 1px 2px rgba(255, 255, 255, 0.4);
        border-radius: 12px;
    }}
    </style>
    <div class="sicard{uid}">
        <div class="silbl{uid}">{label}</div>
        <div class="sitrack{uid}">
            <div class="sifill{uid}"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def skeu_blob_volume(label: str = "Volume", show_icon: bool = True):
    """
    Display a skeuomorphic volume knob.
    """
    uid = f"sv{random.randint(10000, 99999)}"
    
    icon_html = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>' if show_icon else ""
    
    st.markdown(f"""
    <style>
    .svcard{uid} {{
        background: linear-gradient(145deg, #f5f5f5, #e8e8e8);
        border-radius: 16px;
        padding: 28px;
        margin: 12px 0;
        box-shadow: 
            8px 8px 16px #d0d0d0,
            -8px -8px 16px #ffffff,
            inset 1px 1px 0 rgba(255, 255, 255, 0.8),
            inset -1px -1px 0 rgba(0, 0, 0, 0.05);
    }}
    .svlbl{uid} {{
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 20px;
        opacity: 0.7;
    }}
    .svwrap{uid} {{
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: 16px;
    }}
    .svknob{uid} {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #f8f8f8, #e0e0e0, #c0c0c0);
        box-shadow: 
            0 10px 20px rgba(0, 0, 0, 0.15),
            inset -2px -2px 5px rgba(0, 0, 0, 0.1),
            inset 2px 2px 5px rgba(255, 255, 255, 0.7),
            0 0 0 3px #e8e8e8,
            0 0 0 6px #c0c0c0;
        position: relative;
    }}
    .svknob{uid}::after {{
        content: '';
        position: absolute;
        width: 6px;
        height: 30px;
        background: linear-gradient(to bottom, #444, #222);
        border-radius: 3px;
        top: 12px;
        left: 50%;
        transform: translateX(-50%);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }}
    </style>
    <div class="svcard{uid}">
        <div class="svlbl{uid}">{label}</div>
        <div class="svwrap{uid}">
            <div class="svknob{uid}"></div>
            {icon_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def skeu_blob_progress(value: float, label: str = "Email Send Rate", color_scheme: str = "blue"):
    """
    Display a skeuomorphic progress bar with realistic depth.
    """
    uid = f"sp{random.randint(10000, 99999)}"
    percentage = int(value * 100)
    
    if color_scheme == "orange":
        fill_color = "linear-gradient(to right, #ff6b35, #ff8c42)"
    elif color_scheme == "teal":
        fill_color = "linear-gradient(to right, #0891b2, #06b6d4)"
    else:
        fill_color = "linear-gradient(to right, #3b82f6, #60a5fa)"
    
    st.markdown(f"""
    <style>
    .spcard{uid} {{
        background: linear-gradient(145deg, #f5f5f5, #e8e8e8);
        border-radius: 16px;
        padding: 28px;
        margin: 12px 0;
        box-shadow: 
            8px 8px 16px #d0d0d0,
            -8px -8px 16px #ffffff,
            inset 1px 1px 0 rgba(255, 255, 255, 0.8),
            inset -1px -1px 0 rgba(0, 0, 0, 0.05);
    }}
    .splbl{uid} {{
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 16px;
        opacity: 0.7;
    }}
    .spwrap{uid} {{
        display: flex;
        align-items: center;
        gap: 20px;
    }}
    .sptrack{uid} {{
        flex: 1;
        height: 32px;
        background: linear-gradient(to bottom, #e0e0e0, #f0f0f0);
        border-radius: 16px;
        box-shadow: 
            inset 4px 4px 8px #cccccc,
            inset -4px -4px 8px #ffffff;
        overflow: hidden;
        position: relative;
    }}
    .spfill{uid} {{
        height: 100%;
        width: {percentage}%;
        background: {fill_color};
        border-radius: 16px;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.3);
        transition: width 0.3s ease;
    }}
    .spval{uid} {{
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        font-size: 24px;
        font-weight: 700;
        min-width: 65px;
        text-align: right;
    }}
    </style>
    <div class="spcard{uid}">
        <div class="splbl{uid}">{label}</div>
        <div class="spwrap{uid}">
            <div class="sptrack{uid}"><div class="spfill{uid}"></div></div>
            <div class="spval{uid}">{percentage}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def skeu_blob_bounce(value: float, label: str = "Bounce Rate"):
    """
    Display a skeuomorphic bounce rate indicator.
    """
    uid = f"sb{random.randint(10000, 99999)}"
    percentage = round(value * 100, 1)
    
    st.markdown(f"""
    <style>
    .sbcard{uid} {{
        background: linear-gradient(145deg, #f5f5f5, #e8e8e8);
        border-radius: 16px;
        padding: 28px;
        margin: 12px 0;
        box-shadow: 
            8px 8px 16px #d0d0d0,
            -8px -8px 16px #ffffff,
            inset 1px 1px 0 rgba(255, 255, 255, 0.8),
            inset -1px -1px 0 rgba(0, 0, 0, 0.05);
    }}
    .sblbl{uid} {{
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 16px;
        opacity: 0.7;
    }}
    .sbwrap{uid} {{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .sbgauge{uid} {{
        flex: 1;
        height: 40px;
        background: linear-gradient(to bottom, #e0e0e0, #f0f0f0);
        border-radius: 20px;
        box-shadow: 
            inset 3px 3px 6px #cccccc,
            inset -3px -3px 6px #ffffff;
        overflow: hidden;
        position: relative;
        margin-right: 20px;
    }}
    .sbfill{uid} {{
        height: 100%;
        width: {percentage}%;
        background: linear-gradient(to right, #ff6b35, #ff8c42);
        border-radius: 20px;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }}
    .sbval{uid} {{
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        font-size: 22px;
        font-weight: 700;
        min-width: 60px;
    }}
    </style>
    <div class="sbcard{uid}">
        <div class="sblbl{uid}">{label}</div>
        <div class="sbwrap{uid}">
            <div class="sbgauge{uid}"><div class="sbfill{uid}"></div></div>
            <div class="sbval{uid}">{percentage}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def skeu_metric(label: str, value: str, delta: str = None, color: str = "#3b82f6"):
    """Skeuomorphic glowing metric card with beveled edges."""
    uid = f"sm{random.randint(10000, 99999)}"
    
    delta_html = ""
    if delta:
        is_positive = not delta.startswith('-')
        delta_color = "#22c55e" if is_positive else "#ef4444"
        delta_icon = "↑" if is_positive else "↓"
        delta_html = f'<div style="color:{delta_color};font-size:14px;margin-top:8px;">{delta_icon} {delta}</div>'
    
    st.markdown(f"""
    <style>
    .scard{uid} {{
        background: linear-gradient(145deg, #f5f5f5, #e8e8e8);
        border-radius: 16px;
        padding: 24px;
        margin: 10px 0;
        box-shadow: 
            6px 6px 12px #d0d0d0,
            -6px -6px 12px #ffffff,
            inset 1px 1px 0 rgba(255, 255, 255, 0.8),
            inset -1px -1px 0 rgba(0, 0, 0, 0.05);
    }}
    .slbl{uid} {{
        color: #666666;
        font-family: 'Segoe UI', sans-serif;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }}
    .sval{uid} {{
        color: {color};
        font-family: 'Segoe UI', sans-serif;
        font-size: 32px;
        font-weight: 700;
    }}
    </style>
    <div class="scard{uid}">
        <div class="slbl{uid}">{label}</div>
        <div class="sval{uid}">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def skeu_notification(message: str, type: str = "info", color: str = None):
    """Display a skeuomorphic notification with embossed effect."""
    uid = f"sn{random.randint(10000, 99999)}"
    
    type_colors = {"info": "#3b82f6", "success": "#22c55e", "warning": "#f59e0b", "error": "#ef4444"}
    type_icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
    
    c = color or type_colors.get(type, "#3b82f6")
    icon = type_icons.get(type, "ℹ️")
    
    st.markdown(f"""
    <style>
    .snbox{uid} {{
        background: linear-gradient(145deg, #f5f5f5, #e8e8e8);
        border-radius: 12px;
        padding: 14px 18px;
        margin: 10px 0;
        border: 2px solid {c};
        border-left: 5px solid {c};
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 
            4px 4px 8px #d0d0d0,
            -4px -4px 8px #ffffff,
            inset 1px 1px 0 rgba(255, 255, 255, 0.8),
            inset -1px -1px 0 rgba(0, 0, 0, 0.02);
    }}
    .sntxt{uid} {{
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
    }}
    </style>
    <div class="snbox{uid}">
        <span style="font-size:18px;">{icon}</span>
        <span class="sntxt{uid}">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def skeu_button(text: str, key: str = None, color: str = "#3b82f6", icon: str = ""):
    """Display a skeuomorphic 3D button."""
    uid = f"sb{random.randint(10000, 99999)}"
    
    st.markdown(f"""
    <style>
    .sbtn{uid} {{
        background: linear-gradient(145deg, #ffffff, #e8e8e8);
        border: 2px solid {color};
        border-radius: 12px;
        padding: 12px 24px;
        color: {color};
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 
            0 6px 12px rgba(0, 0, 0, 0.1),
            inset 1px 1px 0 rgba(255, 255, 255, 0.8),
            inset -1px -1px 0 rgba(0, 0, 0, 0.05);
        display: inline-flex;
        align-items: center;
        gap: 8px;
        transition: all 0.2s ease;
    }}
    .sbtn{uid}:active {{
        box-shadow: 
            0 2px 4px rgba(0, 0, 0, 0.1),
            inset 2px 2px 4px rgba(0, 0, 0, 0.1),
            inset -1px -1px 2px rgba(255, 255, 255, 0.5);
        transform: translateY(2px);
    }}
    .sbtn{uid}:hover {{
        background: linear-gradient(145deg, #f0f0f0, #e0e0e0);
    }}
    </style>
    <button class="sbtn{uid}">{icon} {text}</button>
    """, unsafe_allow_html=True)


def skeu_stats_card(title: str, stats: list, color: str = "#3b82f6"):
    """Skeuomorphic stats card with multiple values."""
    uid = f"ss{random.randint(10000, 99999)}"
    
    stats_items = ""
    for stat in stats:
        val = stat.get('value', '0')
        lbl = stat.get('label', '')
        stats_items += f'<div class="sitem{uid}"><div class="sval{uid}">{val}</div><div class="slbl{uid}">{lbl}</div></div>'
    
    st.markdown(f"""
    <style>
    .scard{uid} {{
        background: linear-gradient(145deg, #f5f5f5, #e8e8e8);
        border-radius: 16px;
        padding: 28px;
        box-shadow: 
            8px 8px 16px #d0d0d0,
            -8px -8px 16px #ffffff,
            inset 1px 1px 0 rgba(255, 255, 255, 0.8),
            inset -1px -1px 0 rgba(0, 0, 0, 0.05);
        margin: 15px 0;
    }}
    .stitle{uid} {{
        color: #1a1a1a;
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid #d0d0d0;
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
        color: #666666;
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


def skeu_loading(text: str = "Loading...", color: str = "#3b82f6"):
    """Display skeuomorphic loading indicator."""
    uid = f"sl{random.randint(10000, 99999)}"
    
    st.markdown(f"""
    <style>
    @keyframes spin{uid} {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    .lbox{uid} {{
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 30px;
        background: linear-gradient(145deg, #f5f5f5, #e8e8e8);
        border-radius: 16px;
        box-shadow: 
            8px 8px 16px #d0d0d0,
            -8px -8px 16px #ffffff;
        margin: 20px 0;
    }}
    .lspinner{uid} {{
        width: 50px;
        height: 50px;
        border: 4px solid #e0e0e0;
        border-top: 4px solid {color};
        border-radius: 50%;
        animation: spin{uid} 1s linear infinite;
        margin-bottom: 15px;
    }}
    .ltxt{uid} {{
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
    }}
    </style>
    <div class="lbox{uid}">
        <div class="lspinner{uid}"></div>
        <div class="ltxt{uid}">{text}</div>
    </div>
    """, unsafe_allow_html=True)


__all__ = [
    'skeu_blob_metric', 'skeu_blob_intensity', 'skeu_blob_volume',
    'skeu_blob_progress', 'skeu_blob_bounce', 'skeu_metric',
    'skeu_notification', 'skeu_button', 'skeu_stats_card', 'skeu_loading'
]
