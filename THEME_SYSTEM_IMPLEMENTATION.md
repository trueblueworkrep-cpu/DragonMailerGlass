# Theme System Implementation - Summary

## Overview
Dragon Mailer uses a unified component system with theme-specific visual tokens and CSS overrides. The current themes are Glass, Dark, and Light.

## Files Involved

### 1. `app.py`
Key areas:
- `UI_THEME_OPTIONS`: Interface theme list
- `get_saved_ui_theme()` and `save_ui_theme()`: Theme persistence
- `get_ui_theme_visuals()`: Theme tokens for shared widgets
- `inject_ui_theme_overrides()`: Theme-specific CSS overrides
- `login_page()`: Login background and theme colors

### 2. `dashboard_jelly.py`
Key areas:
- `THEME_OPTIONS`: Dashboard theme list
- `get_theme_visuals()`: Theme tokens for dashboard visuals
- `render_theme_selector()`: Sidebar selector and persistence

### 3. `config/settings.json`
Stores user preference:
```json
{
  "theme": "Glass",
  "available_themes": ["Glass", "Dark", "Light"]
}
```

## Key Features

### Dynamic Theme Switching
Theme selection is stored in `config/settings.json` and applied at runtime without restarting.

### Unified Component API
All themes use the same component functions:
```python
components["blob_metric"](label, value, sublabel)
components["notification"](message, level)
components["blob_progress"](value, label, color_scheme)
```

## Adding a New Theme
1. Add the theme name to `UI_THEME_OPTIONS` in `app.py`.
2. Add the theme name to `THEME_OPTIONS` in `dashboard_jelly.py`.
3. Define the theme tokens:
   - `get_ui_theme_visuals()` in `app.py`
   - `get_theme_visuals()` in `dashboard_jelly.py`
4. Add CSS overrides in `inject_ui_theme_overrides()` in `app.py`.
5. Update `config/settings.json` `available_themes`.

## Notes
- Glass is the only theme with heavy blur/glow effects.
- Dark and Light are low-overhead and reduce GPU load.
