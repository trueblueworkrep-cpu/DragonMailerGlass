# Quick Start - Theme System

## Get Started in 30 Seconds

### 1. Open Your Dashboard
```bash
streamlit run dashboard_jelly.py
```

### 2. Look at the Left Sidebar
You will see a Theme Settings section.

### 3. Pick a Theme
- Glass - Modern, futuristic, glowing animations
- Dark - Low-glare, focused contrast
- Light - Bright, clean, high readability

### 4. Watch It Change Instantly
The entire dashboard transforms to match your theme choice.

## Theme Characteristics at a Glance

### Glass Theme
- Glowing effects
- Smooth animations
- Futuristic look
- Blue and orange gradients

### Dark Theme
- Deep, low-glare panels
- High contrast accents
- Focused and calm presentation

### Light Theme
- Bright surfaces
- Clean typography
- Subtle cyan highlights

## What Components Get Themed?
All these auto-adapt to your selected theme:
- Metric Cards
- Progress Bars
- Notifications (info, success, warning, error)
- Stats Cards
- Volume Controls
- Intensity Indicators

## Examples

### Metric Card
```python
components["blob_metric"](
    "Campaign Overview",
    "1,234",
    "emails sent this month"
)
```

### Progress Bar
```python
components["blob_progress"](0.65, "Send Rate", "blue_orange")
```

### Notification
```python
components["notification"](
    "Campaign sent successfully!",
    "success"
)
```

## Theme Selection Saved?
Yes. Your choice persists across sessions.

Your preference is stored in `config/settings.json`:
```json
{
  "theme": "Glass",
  "available_themes": ["Glass", "Dark", "Light"]
}
```

### Change default theme
Edit `config/settings.json` and change:
```json
"theme": "Glass"  ->  "theme": "Dark"
```

## Performance Tips

### Glass Theme
- Best on modern devices
- Higher GPU usage due to blur and glow
- Looks best in darker environments

### Dark Theme
- Reduced glare for long sessions
- Lower overhead than Glass
- Great for low-light conditions

### Light Theme
- Best in bright rooms
- Minimal glow for clarity
- Clean for presentations

## For Developers

### Add your own components to the theme system
1. Create the function in `jelly_components.py`:
```python
def jelly_custom_widget(value):
    st.markdown("...", unsafe_allow_html=True)
```

2. Add it to the component dictionary in `dashboard_jelly.py`:
```python
def get_theme_components():
    return {
        # ... existing components ...
        "custom_widget": jelly_custom_widget,
    }
```

3. Use it in `render()`:
```python
components["custom_widget"](value)
```

## Troubleshooting

### Theme not switching?
1. Check the sidebar for Theme Settings
2. Make sure `config/settings.json` exists and is writable
3. Refresh the page
4. Restart the Streamlit app

### Components look off?
1. Clear browser cache
2. Try a different browser
3. Check CSS3 support

### Theme not saving?
1. Verify `config/settings.json` permissions
2. Try setting the theme manually in JSON

## Want More?
- Read `THEME_GUIDE.md` for complete documentation
- Check `THEME_COMPARISON.md` for visual comparison
- See `THEME_SYSTEM_IMPLEMENTATION.md` for technical details
