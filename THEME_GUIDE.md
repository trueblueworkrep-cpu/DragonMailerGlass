# Theme System Guide - Dragon Mailer

## Overview
Dragon Mailer supports multiple UI themes that can be switched dynamically through the sidebar. The current options are Glass, Dark, and Light.

## Available Themes

### 1. Glass Theme (Modern Glassmorphism)
- Description: Modern, futuristic design with translucent elements
- Characteristics:
  - Glowing animated blobs with smooth morphing
  - Blue and orange gradient accents
  - Glassy, frosted glass effect
  - Soft glow animations
  - High-tech appearance
- Best for: Modern, contemporary interfaces; tech-forward applications

### 2. Dark Theme (Low-Glare Focus)
- Description: Deep, low-glare panels with crisp contrast
- Characteristics:
  - Dark surfaces with cool highlights
  - Reduced glare for long sessions
  - Strong accent contrast for key actions
  - Calm, focused presentation
- Best for: Night use, long sessions, and focus-heavy workflows

### 3. Light Theme (Bright and Clean)
- Description: Bright surfaces with clean typography and gentle accents
- Characteristics:
  - Light panels with subtle cyan accents
  - Crisp readability in bright environments
  - Minimal glow for a clean look
  - Clear visual hierarchy
- Best for: Daytime use, presentations, and shared workspaces

## Switching Themes
1. Open the Dashboard
2. Look at the left sidebar (Theme Settings section)
3. Select your preferred theme from the dropdown
4. The dashboard will update instantly

Your theme preference is saved in `config/settings.json`.

## Theme Components
All themes use the same component API with different visual styling:

| Component | Description |
|-----------|-------------|
| `blob_metric` | Large metric card display |
| `blob_intensity` | Animated intensity indicator |
| `blob_volume` | Volume/level control display |
| `blob_progress` | Progress bar with percentage |
| `blob_bounce` | Bounce rate indicator |
| `metric` | Simple metric with optional delta |
| `notification` | Info/success/warning/error messages |
| `stats_card` | Multi-statistic summary card |

## Configuration
Edit `config/settings.json` to set the default theme:

```json
{
  "theme": "Glass",
  "available_themes": ["Glass", "Dark", "Light"],
  "login_enabled": true,
  "password_hash": "",
  "multi_user_enabled": true,
  "session_timeout": 3600
}
```

Change `"theme": "Glass"` to `"theme": "Dark"` or `"theme": "Light"` to set a different default.

## Design Details

### Glass Theme Colors
- Primary Blue: `#3b82f6`
- Accent Orange: `#f97316`
- Teal Accent: `#06b6d4`
- Background: Dark with transparency and blur

### Dark Theme Colors
- Primary Accent: `#22c55e`
- Panel Background: `#0f172a` to `#1e293b`
- Text: `#e2e8f0`
- Borders: `rgba(148, 163, 184, 0.25)`

### Light Theme Colors
- Primary Accent: `#0ea5e9`
- Panel Background: `#ffffff` to `#f0f9ff`
- Text: `#0f172a`
- Borders: `rgba(14, 165, 233, 0.3)`

## Adding New Themes
To add a new theme:
1. Add the theme name to `UI_THEME_OPTIONS` in `app.py`.
2. Add the theme name to `THEME_OPTIONS` in `dashboard_jelly.py`.
3. Add theme tokens in `get_ui_theme_visuals()` (`app.py`) and `get_theme_visuals()` (`dashboard_jelly.py`).
4. Add any CSS overrides in `inject_ui_theme_overrides()` (`app.py`).
5. Update `config/settings.json` `available_themes`.

## Tips for Best Experience

### Glass Theme
- Best on modern devices
- Higher GPU usage due to blur and glow
- Looks best in darker environments

### Dark Theme
- Reduced glare for long sessions
- Strong contrast for focus
- Ideal for dim lighting

### Light Theme
- Great in bright rooms
- Crisp readability for demos
- Minimal glow for clarity

## Troubleshooting
**Theme not switching?**
- Restart the Streamlit app
- Verify `config/settings.json` is writable
- Refresh the page

**Components look broken?**
- Ensure browser supports CSS3
- Clear browser cache
- Try a different browser

**Performance issues?**
- Glass uses more GPU due to blur/animations
- Try Dark or Light for lower overhead
