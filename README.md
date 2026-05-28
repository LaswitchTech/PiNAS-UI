---
name: PiNAS touchscreen UI
description: Custom PyQt6 touchscreen dashboard for Raspberry Pi 5 NAS appliance
---

# PiNAS UI

Custom embedded touchscreen interface for the PiNAS Raspberry Pi 5 NAS appliance.

## Features

- **Tactical HUD Interface** — Halo UNSC-inspired dark theme with customizable color presets
- **System Monitoring** — Real-time CPU, memory, storage, temperature, and network metrics
- **Swipe Navigation** — Smooth horizontal transitions between screens
- **Theme System** — 6 preset color themes with dynamic UI adaptation
- **Touch-Optimized** — Large touch targets and finger-friendly layout for 480x800 vertical touchscreen

## Screens

1. **System Overview** — CPU, memory, ZFS/RAID, network, uptime, temperature
2. **Storage / SMART** — Drive health, SMART data, capacity indicators
3. **Settings** — WiFi, hostname, system controls, theme customization

## Requirements

- Python 3.10+
- PyQt6 6.6+
- psutil 5.9+
- Raspberry Pi 5 (target platform)
- Linux (Raspberry Pi OS or Debian-based)

## Installation

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

## Configuration

Edit `config/app.json` to adjust:

- Screen dimensions
- Polling intervals
- Default theme preset
- Feature toggles

## Architecture

```
app/
├── screens/       # Swipeable screen pages
├── widgets/       # Custom HUD widgets
├── services/      # Background system polling
├── themes/        # Theme system and presets
├── config/        # Internal configuration
├── assets/        # SVG logos, icons
├── app.py         # MainWindow and screen container
└── main.py        # Application entry point
config/
└── app.json       # Application settings
```

## License

GPL-3.0-only
