"""
Enhanced Animation System for Dragon Mailer
Advanced micro-interactions, page transitions, and celebration effects
"""
"""
Enhanced Animation System for Dragon Mailer
Advanced micro-interactions, page transitions, and celebration effects
"""

import streamlit as st
import random
import time


def inject_enhanced_animations():
    """Inject comprehensive animation system CSS and JavaScript"""
    css = """
    <style>
    /* ============================================== */
    /* ENHANCED ANIMATION SYSTEM                      */
    /* ============================================== */

    /* Page Transition Effects */
    .page-enter {
        animation: pageSlideIn 0.5s ease-out;
    }

    .page-exit {
        animation: pageSlideOut 0.3s ease-in;
    }

    @keyframes pageSlideIn {
        0% { transform: translateX(30px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }

    @keyframes pageSlideOut {
        0% { transform: translateX(0); opacity: 1; }
        100% { transform: translateX(-30px); opacity: 0; }
    }

    /* Micro-interactions */
    .micro-bounce {
        animation: microBounce 0.6s ease-out;
    }

    .micro-pulse {
        animation: microPulse 2s ease-in-out infinite;
    }

    .micro-shake {
        animation: microShake 0.5s ease-in-out;
    }

    .micro-glow {
        animation: microGlow 1s ease-in-out;
    }

    @keyframes microBounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-8px); }
        60% { transform: translateY(-4px); }
    }

    @keyframes microPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    @keyframes microShake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
        20%, 40%, 60%, 80% { transform: translateX(2px); }
    }

    @keyframes microGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.3); }
        50% { box-shadow: 0 0 30px rgba(0, 212, 255, 0.6); }
    }

    /* Enhanced Button Interactions */
    .btn-enhanced {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .btn-enhanced::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }

    .btn-enhanced:hover::before {
        width: 300px;
        height: 300px;
    }

    .btn-enhanced:active {
        transform: scale(0.98);
        transition: transform 0.1s;
    }

    /* Loading States */
    .loading-dots {
        display: inline-flex;
        gap: 4px;
        align-items: center;
    }

    .loading-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #00d4ff;
        animation: loadingDot 1.4s ease-in-out infinite both;
    }

    .loading-dot:nth-child(1) { animation-delay: -0.32s; }
    .loading-dot:nth-child(2) { animation-delay: -0.16s; }

    @keyframes loadingDot {
        0%, 80%, 100% {
            transform: scale(0);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }

    /* Success Celebration */
    .celebration-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
    }

    .celebration-particle {
        position: absolute;
        width: 8px;
        height: 8px;
        background: #00d4ff;
        border-radius: 50%;
        animation: celebrate 2s ease-out forwards;
    }

    @keyframes celebrate {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) rotate(720deg);
            opacity: 0;
        }
    }

    /* Form Field Focus Effects */
    .form-field-enhanced {
        position: relative;
        transition: all 0.3s ease;
    }

    .form-field-enhanced:focus-within {
        transform: translateY(-2px);
    }

    .form-field-enhanced:focus-within .form-label {
        color: #00d4ff;
        transform: translateY(-2px);
    }

    .form-field-enhanced .form-input {
        transition: all 0.3s ease;
    }

    .form-field-enhanced .form-input:focus {
        border-color: #00d4ff;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }

    /* Card Hover Effects */
    .card-enhanced {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        transform-style: preserve-3d;
    }

    .card-enhanced:hover {
        transform: translateY(-8px) rotateX(5deg);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }

    /* Staggered Animation Classes */
    .stagger-1 { animation-delay: 0.1s; }
    .stagger-2 { animation-delay: 0.2s; }
    .stagger-3 { animation-delay: 0.3s; }
    .stagger-4 { animation-delay: 0.4s; }
    .stagger-5 { animation-delay: 0.5s; }

    /* Fade In Animations */
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }

    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }

    .fade-in-down {
        animation: fadeInDown 0.6s ease-out;
    }

    .fade-in-left {
        animation: fadeInLeft 0.6s ease-out;
    }

    .fade-in-right {
        animation: fadeInRight 0.6s ease-out;
    }

    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

    @keyframes fadeInUp {
        0% {
            opacity: 0;
            transform: translateY(30px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInDown {
        0% {
            opacity: 0;
            transform: translateY(-30px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInLeft {
        0% {
            opacity: 0;
            transform: translateX(-30px);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes fadeInRight {
        0% {
            opacity: 0;
            transform: translateX(30px);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* Typing Effect */
    .typing-effect {
        overflow: hidden;
        border-right: 2px solid #00d4ff;
        white-space: nowrap;
        animation: typing 3s steps(40, end), blink-caret 0.75s step-end infinite;
    }

    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }

    @keyframes blink-caret {
        from, to { border-color: transparent; }
        50% { border-color: #00d4ff; }
    }

    /* Progress Ring Animation */
    .progress-ring {
        transform: rotate(-90deg);
    }

    .progress-ring-circle {
        transition: stroke-dasharray 0.3s ease;
        stroke-linecap: round;
    }

    /* Skeleton Loading */
    .skeleton {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: skeleton-loading 1.5s infinite;
    }

    @keyframes skeleton-loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    /* Notification Toast Animations */
    .toast-enter {
        animation: toastSlideIn 0.3s ease-out;
    }

    .toast-exit {
        animation: toastSlideOut 0.3s ease-in;
    }

    @keyframes toastSlideIn {
        0% {
            transform: translateX(100%);
            opacity: 0;
        }
        100% {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes toastSlideOut {
        0% {
            transform: translateX(0);
            opacity: 1;
        }
        100% {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    /* Gesture Animations for Mobile */
    @media (max-width: 768px) {
        .swipe-left {
            animation: swipeLeft 0.5s ease-out;
        }

        .swipe-right {
            animation: swipeRight 0.5s ease-out;
        }

        .tap-feedback {
            animation: tapFeedback 0.2s ease-out;
        }
    }

    @keyframes swipeLeft {
        0% { transform: translateX(0); }
        100% { transform: translateX(-100px); }
    }

    @keyframes swipeRight {
        0% { transform: translateX(0); }
        100% { transform: translateX(100px); }
    }

    @keyframes tapFeedback {
        0% { transform: scale(1); }
        50% { transform: scale(0.95); }
        100% { transform: scale(1); }
    }

    /* Advanced Hover Effects */
    .hover-lift {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .hover-lift:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    .hover-glow {
        transition: all 0.3s ease;
    }

    .hover-glow:hover {
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
    }

    .hover-rotate {
        transition: all 0.3s ease;
    }

    .hover-rotate:hover {
        transform: rotate(5deg);
    }

    /* Scroll-triggered Animations */
    .scroll-reveal {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.6s ease;
    }

    .scroll-reveal.revealed {
        opacity: 1;
        transform: translateY(0);
    }

    /* Morphing Shapes */
    .morphing-shape {
        animation: morphingShape 8s ease-in-out infinite;
    }

    @keyframes morphingShape {
        0%, 100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
        25% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }
        50% { border-radius: 50% 50% 40% 60% / 40% 50% 60% 50%; }
        75% { border-radius: 40% 60% 50% 50% / 60% 40% 50% 60%; }
    }

    /* Liquid Button Effect */
    .liquid-button {
        position: relative;
        overflow: hidden;
    }

    .liquid-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }

    .liquid-button:hover::before {
        left: 100%;
    }

    /* Floating Elements */
    .floating {
        animation: floating 6s ease-in-out infinite;
    }

    @keyframes floating {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }

    .floating-delayed {
        animation: floating 6s ease-in-out infinite;
        animation-delay: -2s;
    }

    /* Pulse Ring Effect */
    .pulse-ring {
        position: relative;
    }

    .pulse-ring::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 100%;
        height: 100%;
        border: 2px solid #00d4ff;
        border-radius: 50%;
        transform: translate(-50%, -50%);
        animation: pulseRing 2s infinite;
    }

    @keyframes pulseRing {
        0% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 1;
        }
        100% {
            transform: translate(-50%, -50%) scale(1.5);
            opacity: 0;
        }
    }

    </style>
    """

    js = """
    <script>
    // Enhanced Animation System JavaScript
    window.EnhancedAnimations = {
        // Page transitions
        transitionPage: function(fromElement, toElement, direction = 'forward') {
            if (fromElement) {
                fromElement.classList.add('page-exit');
                setTimeout(() => {
                    fromElement.style.display = 'none';
                    fromElement.classList.remove('page-exit');
                }, 300);
            }

            if (toElement) {
                toElement.style.display = 'block';
                toElement.classList.add('page-enter');
                setTimeout(() => {
                    toElement.classList.remove('page-enter');
                }, 500);
            }
        },

        // Micro-interactions
        addMicroInteraction: function(element, type) {
            element.classList.add(`micro-${type}`);
            setTimeout(() => {
                element.classList.remove(`micro-${type}`);
            }, 600);
        },

        // Celebration effect
        celebrate: function() {
            const container = document.createElement('div');
            container.className = 'celebration-container';

            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'celebration-particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 2 + 's';
                particle.style.background = `hsl(${Math.random() * 360}, 100%, 70%)`;
                container.appendChild(particle);
            }

            document.body.appendChild(container);
            setTimeout(() => {
                document.body.removeChild(container);
            }, 3000);
        },

        // Staggered animations
        staggerAnimate: function(elements, animationClass, delay = 100) {
            elements.forEach((element, index) => {
                setTimeout(() => {
                    element.classList.add(animationClass);
                }, index * delay);
            });
        },

        // Scroll-triggered animations
        initScrollReveal: function() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('revealed');
                    }
                });
            });

            document.querySelectorAll('.scroll-reveal').forEach(el => {
                observer.observe(el);
            });
        },

        // Typing effect
        typeText: function(element, text, speed = 50) {
            let i = 0;
            element.textContent = '';

            function type() {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                } else {
                    element.classList.remove('typing-effect');
                }
            }

            element.classList.add('typing-effect');
            type();
        },

        // Progress ring animation
        animateProgressRing: function(ring, percentage) {
            const circle = ring.querySelector('.progress-ring-circle');
            const radius = circle.r.baseVal.value;
            const circumference = radius * 2 * Math.PI;

            circle.style.strokeDasharray = `${circumference} ${circumference}`;
            circle.style.strokeDashoffset = circumference;

            const offset = circumference - (percentage / 100) * circumference;
            circle.style.strokeDashoffset = offset;
        },

        // Gesture handling for mobile
        initGestures: function() {
            let startX, startY;

            document.addEventListener('touchstart', (e) => {
                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
            });

            document.addEventListener('touchend', (e) => {
                if (!startX || !startY) return;

                const endX = e.changedTouches[0].clientX;
                const endY = e.changedTouches[0].clientY;
                const diffX = startX - endX;
                const diffY = startY - endY;

                if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                    // Horizontal swipe
                    const target = e.target.closest('.card-enhanced, .btn-enhanced');
                    if (target) {
                        if (diffX > 0) {
                            target.classList.add('swipe-left');
                        } else {
                            target.classList.add('swipe-right');
                        }
                        setTimeout(() => {
                            target.classList.remove('swipe-left', 'swipe-right');
                        }, 500);
                    }
                }
            });

            // Tap feedback
            document.addEventListener('touchstart', (e) => {
                const target = e.target.closest('button, .card-enhanced');
                if (target) {
                    target.classList.add('tap-feedback');
                }
            });

            document.addEventListener('touchend', (e) => {
                document.querySelectorAll('.tap-feedback').forEach(el => {
                    el.classList.remove('tap-feedback');
                });
            });
        },

        // Enhanced button interactions
        enhanceButtons: function() {
            document.querySelectorAll('.btn-enhanced').forEach(button => {
                button.addEventListener('mouseenter', () => {
                    this.addMicroInteraction(button, 'glow');
                });

                button.addEventListener('click', () => {
                    this.addMicroInteraction(button, 'bounce');
                });
            });
        },

        // Form field enhancements
        enhanceFormFields: function() {
            document.querySelectorAll('.form-field-enhanced').forEach(field => {
                const input = field.querySelector('.form-input');
                const label = field.querySelector('.form-label');

                if (input && label) {
                    input.addEventListener('focus', () => {
                        label.classList.add('focused');
                    });

                    input.addEventListener('blur', () => {
                        if (!input.value) {
                            label.classList.remove('focused');
                        }
                    });

                    // Check initial state
                    if (input.value) {
                        label.classList.add('focused');
                    }
                }
            });
        },

        // Initialize all enhancements
        init: function() {
            this.initScrollReveal();
            this.initGestures();
            this.enhanceButtons();
            this.enhanceFormFields();

            // Add loading class to body initially
            document.body.classList.add('loading');
            setTimeout(() => {
                document.body.classList.remove('loading');
                document.body.classList.add('loaded');
            }, 100);
        }
    };

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.EnhancedAnimations.init();
        });
    } else {
        window.EnhancedAnimations.init();
    }

    // Helper functions for Streamlit
    window.animateSuccess = function() {
        window.EnhancedAnimations.celebrate();
    };

    window.animateElement = function(elementId, animation) {
        const element = document.getElementById(elementId);
        if (element) {
            window.EnhancedAnimations.addMicroInteraction(element, animation);
        }
    };

    window.staggerElements = function(selector, animationClass) {
        const elements = document.querySelectorAll(selector);
        window.EnhancedAnimations.staggerAnimate(elements, animationClass);
    };

    window.typeWriter = function(elementId, text) {
        const element = document.getElementById(elementId);
        if (element) {
            window.EnhancedAnimations.typeText(element, text);
        }
    };
    </script>
    """

    st.markdown(css, unsafe_allow_html=True)
    st.markdown(js, unsafe_allow_html=True)


def enhanced_button(text: str, key: str = None, color: str = "#00d4ff", icon: str = "", animation: str = "bounce"):
    """Create an enhanced animated button"""
    uid = f"eb{random.randint(10000, 99999)}"

    st.markdown(f"""
    <style>
    .enhanced-btn-{uid} {{
        background: linear-gradient(135deg, {color}90, {color}cc);
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        color: white;
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 4px 20px {color}40;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        class: btn-enhanced liquid-button;
    }}

    .enhanced-btn-{uid}:hover {{
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 30px {color}60;
    }}

    .enhanced-btn-{uid}:active {{
        transform: translateY(0) scale(0.98);
        transition: all 0.1s;
    }}

    .enhanced-btn-{uid}::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }}

    .enhanced-btn-{uid}:hover::before {{
        left: 100%;
    }}
    </style>
    <button class="enhanced-btn-{uid} btn-enhanced liquid-button" id="btn-{uid}" onclick="animateElement('btn-{uid}', '{animation}')">
        {f'<span>{icon}</span>' if icon else ''} {text}
    </button>
    """, unsafe_allow_html=True)


def enhanced_loading(text: str = "Loading...", style: str = "dots"):
    """Create enhanced loading animation"""
    uid = f"el{random.randint(10000, 99999)}"

    if style == "dots":
        loading_html = f"""
        <div class="loading-dots">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
        <span style="margin-left: 8px; color: rgba(255, 255, 255, 0.7);">{text}</span>
        """
    elif style == "pulse":
        loading_html = f"""
        <div class="pulse-ring" style="display: inline-block; width: 20px; height: 20px; border: 2px solid #00d4ff; border-radius: 50%;"></div>
        <span style="margin-left: 12px; color: rgba(255, 255, 255, 0.7);">{text}</span>
        """
    elif style == "morphing":
        loading_html = f"""
        <div class="morphing-shape" style="width: 40px; height: 20px; background: linear-gradient(90deg, #00d4ff, #4ecdc4); display: inline-block; margin-right: 12px;"></div>
        <span style="color: rgba(255, 255, 255, 0.7);">{text}</span>
        """
    else:
        loading_html = f"""
        <div class="skeleton" style="width: 100px; height: 20px; border-radius: 4px; display: inline-block; margin-right: 12px;"></div>
        <span style="color: rgba(255, 255, 255, 0.7);">{text}</span>
        """

    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; padding: 20px;" id="loading-{uid}">
        {loading_html}
    </div>
    """, unsafe_allow_html=True)


def enhanced_notification(message: str, type: str = "info", duration: int = 3000, celebration: bool = False):
    """Create enhanced notification with animations"""
    uid = f"en{random.randint(10000, 99999)}"

    type_colors = {
        "info": "#3b82f6",
        "success": "#22c55e",
        "warning": "#f59e0b",
        "error": "#ef4444"
    }

    type_icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }

    color = type_colors.get(type, "#3b82f6")
    icon = type_icons.get(type, "ℹ️")

    st.markdown(f"""
    <div class="toast-enter" style="
        background: rgba(15, 20, 35, 0.95);
        border-radius: 12px;
        padding: 16px 20px;
        margin: 10px 0;
        backdrop-filter: blur(15px);
        border: 1px solid {color}40;
        border-left: 4px solid {color};
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 4px 20px {color}20;
        animation: toastSlideIn 0.3s ease-out;
        max-width: 500px;
    " id="notification-{uid}">
        <span style="font-size: 20px;">{icon}</span>
        <span style="color: rgba(255, 255, 255, 0.9); flex: 1;">{message}</span>
    </div>

    <script>
        // Auto-remove notification
        setTimeout(() => {{
            const notification = document.getElementById('notification-{uid}');
            if (notification) {{
                notification.style.animation = 'toastSlideOut 0.3s ease-in';
                setTimeout(() => {{
                    if (notification.parentNode) {{
                        notification.parentNode.removeChild(notification);
                    }}
                }}, 300);
            }}
        }}, {duration});

        // Celebration effect for success
        {f"setTimeout(() => {{ animateSuccess(); }}, 200);" if celebration and type == "success" else ""}
    </script>
    """, unsafe_allow_html=True)


def enhanced_progress_ring(value: float, size: int = 100, color: str = "#00d4ff", label: str = ""):
    """Create animated progress ring"""
    uid = f"pr{random.randint(10000, 99999)}"
    percentage = int(value * 100)
    radius = (size - 10) // 2
    circumference = 2 * 3.14159 * radius

    st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: center; gap: 10px;" id="progress-{uid}">
        <svg width="{size}" height="{size}" class="progress-ring">
            <circle
                cx="{size//2}"
                cy="{size//2}"
                r="{radius}"
                stroke="rgba(255, 255, 255, 0.1)"
                stroke-width="8"
                fill="transparent"
            />
            <circle
                cx="{size//2}"
                cy="{size//2}"
                r="{radius}"
                stroke="{color}"
                stroke-width="8"
                fill="transparent"
                class="progress-ring-circle"
                style="stroke-dasharray: {circumference}; stroke-dashoffset: {circumference};"
            />
        </svg>
        <div style="text-align: center;">
            <div style="font-size: 24px; font-weight: bold; color: {color};">{percentage}%</div>
            {f'<div style="color: rgba(255, 255, 255, 0.7); font-size: 14px;">{label}</div>' if label else ''}
        </div>
    </div>

    <script>
        // Animate progress ring
        setTimeout(() => {{
            const circle = document.querySelector('#progress-{uid} .progress-ring-circle');
            const offset = {circumference} - ({percentage} / 100) * {circumference};
            circle.style.strokeDashoffset = offset;
        }}, 100);
    </script>
    """, unsafe_allow_html=True)


def enhanced_card(content: str, hover_effect: str = "lift", animation_delay: int = 0):
    """Create enhanced animated card"""
    uid = f"ec{random.randint(10000, 99999)}"

    effect_class = ""
    if hover_effect == "lift":
        effect_class = "hover-lift"
    elif hover_effect == "glow":
        effect_class = "hover-glow"
    elif hover_effect == "rotate":
        effect_class = "hover-rotate"

    st.markdown(f"""
    <div class="card-enhanced {effect_class} scroll-reveal stagger-{min(animation_delay // 100 + 1, 5)}"
         style="background: rgba(15, 20, 35, 0.85); border-radius: 16px; padding: 20px; margin: 10px 0;
                backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.08);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); transition: all 0.3s ease;
                animation-delay: {animation_delay}ms;" id="card-{uid}">
        {content}
    </div>
    """, unsafe_allow_html=True)


def enhanced_form_field(label: str, input_type: str = "text", placeholder: str = "", key: str = None):
    """Create enhanced animated form field"""
    uid = f"ef{random.randint(10000, 99999)}"

    st.markdown(f"""
    <div class="form-field-enhanced" style="margin: 20px 0; position: relative;">
        <label class="form-label" style="
            position: absolute;
            top: 16px;
            left: 16px;
            color: rgba(255, 255, 255, 0.6);
            transition: all 0.3s ease;
            pointer-events: none;
            font-size: 14px;
        ">{label}</label>
        <input type="{input_type}" class="form-input" placeholder="{placeholder}"
               style="
                   width: 100%;
                   padding: 16px;
                   background: rgba(20, 25, 45, 0.8);
                   border: 1px solid rgba(255, 255, 255, 0.2);
                   border-radius: 8px;
                   color: white;
                   font-size: 14px;
                   transition: all 0.3s ease;
                   box-sizing: border-box;
               "
               id="input-{uid}">
    </div>

    <script>
        // Enhanced form field behavior
        const input{uid} = document.getElementById('input-{uid}');
        const label{uid} = input{uid}.previousElementSibling;

        function updateLabel{uid}() {{
            if (input{uid}.value || input{uid} === document.activeElement) {{
                label{uid}.style.top = '8px';
                label{uid}.style.fontSize = '12px';
                label{uid}.style.color = '#00d4ff';
            }} else {{
                label{uid}.style.top = '16px';
                label{uid}.style.fontSize = '14px';
                label{uid}.style.color = 'rgba(255, 255, 255, 0.6)';
            }}
        }}

        input{uid}.addEventListener('focus', updateLabel{uid});
        input{uid}.addEventListener('blur', updateLabel{uid});
        input{uid}.addEventListener('input', updateLabel{uid});

        // Initial state
        updateLabel{uid}();
    </script>
    """, unsafe_allow_html=True)


def staggered_animation_container(elements: list, animation: str = "fade-in-up", delay: int = 100):
    """Apply staggered animations to a list of elements"""
    container_id = f"sa{random.randint(10000, 99999)}"

    st.markdown(f"""
    <div id="stagger-{container_id}">
        <script>
            setTimeout(() => {{
                staggerElements('#stagger-{container_id} > *', '{animation}');
            }}, 100);
        </script>
    </div>
    """, unsafe_allow_html=True)

    return container_id


def typing_effect(text: str, speed: int = 50):
    """Create typing effect for text"""
    uid = f"te{random.randint(10000, 99999)}"

    st.markdown(f"""
    <div id="typing-{uid}" style="font-family: 'Segoe UI', sans-serif; font-size: 18px; color: #00d4ff; min-height: 24px;">
        <script>
            setTimeout(() => {{
                typeWriter('typing-{uid}', '{text}');
            }}, 500);
        </script>
    </div>
    """, unsafe_allow_html=True)


def floating_elements(count: int = 5, colors: list = None):
    """Create floating background elements"""
    if colors is None:
        colors = ["#00d4ff", "#4ecdc4", "#45b7d1", "#96ceb4", "#ffeaa7"]

    elements_html = ""
    for i in range(count):
        color = colors[i % len(colors)]
        delay = random.randint(0, 6000)
        size = random.randint(20, 60)
        left = random.randint(0, 90)
        duration = random.randint(8000, 12000)

        elements_html += f"""
        <div style="
            position: fixed;
            width: {size}px;
            height: {size}px;
            background: {color};
            border-radius: 50%;
            opacity: 0.1;
            left: {left}%;
            top: 100vh;
            animation: floating {duration}ms ease-in-out infinite;
            animation-delay: {delay}ms;
            pointer-events: none;
            z-index: 0;
        "></div>
        """

    st.markdown(f"""
    <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1;">
        {elements_html}
    </div>
    """, unsafe_allow_html=True)


# Utility functions for easy integration
def animate_page_transition(from_page: str, to_page: str):
    """Animate transition between pages"""
    st.markdown(f"""
    <script>
        // Page transition animation
        const fromElement = document.querySelector('[data-page="{from_page}"]');
        const toElement = document.querySelector('[data-page="{to_page}"]');
        if (fromElement && toElement) {{
            window.EnhancedAnimations.transitionPage(fromElement, toElement);
        }}
    </script>
    """, unsafe_allow_html=True)
