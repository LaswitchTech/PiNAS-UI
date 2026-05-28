# CLAUDE.md

# PiNAS Project Guidelines

## Overview

PiNAS is a custom Raspberry Pi 5 NAS appliance built around:

- Raspberry Pi 5
- RADXA Penta SATA HAT
- OpenMediaVault
- Custom 3D printed enclosure
- 4.3" vertical touchscreen (480x800)
- Python-based custom touchscreen UI

The goal of this project is to create a compact, futuristic NAS appliance with a polished hardware and software experience inspired by Halo UNSC interfaces and tactical military HUD systems.

---

# Core Philosophy

## 1. Minimal Dependencies

Favor:
- Python standard library
- Lightweight native Linux tools
- Small focused libraries

Avoid:
- Electron
- Heavy frameworks
- Unnecessary abstraction layers

The system must remain:
- Fast
- Lightweight
- Easy to maintain
- Reliable offline

---

# UI Philosophy

## Theme Direction

The UI should resemble:
- Halo Assault Rifle HUD
- UNSC tactical interfaces
- Military sci-fi terminals
- Embedded system diagnostics

### Visual Characteristics

- Dark backgrounds
- Monochrome green HUD elements
- Thin grid lines
- Angular panels
- Soft glow effects
- Minimalist typography
- Technical/military styling
- High readability
- Smooth animations

### Design Constraints

The screen is:
- 480x800
- Vertical orientation
- Touchscreen
- Embedded environment

UI must:
- Be finger friendly
- Avoid clutter
- Remain readable from a distance
- Use large touch targets
- Be performant on Raspberry Pi hardware

---

# Application Architecture

## Screen System

The UI is composed of horizontally swipeable pages similar to iOS home screens.

### Screen 1 — System Overview

Displays:
- CPU usage
- Memory usage
- ZFS/RAID pool usage
- IPv4 address
- Hostname
- System uptime
- Temperature

### Screen 2 — Storage / SMART

Displays:
- Individual drive health
- SMART status
- Temperature
- Capacity
- Usage
- Activity indicators

### Screen 3 — Settings

Displays:
- WiFi configuration
- Hostname configuration
- Network settings
- Reboot/shutdown controls
- Update controls

---

# Technical Requirements

## Preferred Stack

### UI

Preferred:
- PyQt6
- QtQuick/QML (optional)
- Custom-painted widgets

Acceptable:
- Tkinter (only if lightweight)

Avoid:
- Web-based UIs for local display
- Chromium kiosk solutions

### System Integration

Use:
- psutil
- smartctl
- zpool
- mdadm
- hostnamectl
- nmcli
- systemctl

Avoid:
- Parsing unstable shell output when APIs exist

---

# Coding Standards

## General Rules

- Keep files modular
- Keep functions small
- Prefer clarity over cleverness
- Avoid unnecessary inheritance
- Avoid overengineering
- Comment WHY, not WHAT

---

# Python Guidelines

## Formatting

- PEP8 compliant
- Use type hints when possible
- Use dataclasses where appropriate

## Logging

Use structured logging.

Preferred:
```python
logger.info("Drive temperature updated", extra={
    "drive": drive.name,
    "temperature": drive.temperature
})
```

Avoid:
```python
print("Temp updated")
```

---

# Performance Requirements

The UI must:
- Launch quickly
- Use minimal RAM
- Remain responsive during disk activity
- Never freeze during SMART polling

Use:
- Background workers
- Threads
- Async operations where appropriate

Never block the UI thread.

---

# Animation Guidelines

Animations should be:
- Fast
- Subtle
- Smooth
- Functional

Preferred transitions:
- Horizontal sliding
- Fade-in panels
- Radar-like sweeps
- Scanning effects

Avoid:
- Excessive bounce
- Overly playful animations
- Mobile-app style gimmicks

---

# Touchscreen UX

The interface is designed for:
- Finger interaction
- Embedded usage
- Quick diagnostics

Requirements:
- Large buttons
- Swipe navigation
- Minimal keyboard input
- Simple menus
- Fast access to information

---

# Filesystem Structure

Suggested structure:

```text
pinas/
├── app/
│   ├── screens/
│   ├── widgets/
│   ├── services/
│   ├── animations/
│   ├── themes/
│   └── assets/
├── config/
├── logs/
├── data/
└── main.py
```

---

# Hardware Awareness

The system runs on:
- ARM64
- Raspberry Pi 5
- OpenMediaVault
- Linux framebuffer/Wayland/X11 depending on deployment

Code must remain compatible with:
- Raspberry Pi OS
- Debian-based systems

---

# Error Handling

The UI must degrade gracefully.

Examples:
- Missing SMART data
- Disconnected drives
- Network unavailable
- ZFS unavailable

Never crash the entire UI because one metric failed.

---

# Future Expansion

Future possible features:
- RAID rebuild monitoring
- Docker container monitoring
- Network throughput graphs
- UPS monitoring
- Fan controller
- RGB lighting
- AI assistant integration
- Remote dashboard
- Cluster monitoring

Architecture should remain extensible.

---

# Development Workflow

Before major implementation:
1. Define architecture
2. Define UI behavior
3. Consider touchscreen ergonomics
4. Consider Raspberry Pi performance constraints

Prioritize:
1. Reliability
2. Readability
3. Performance
4. Visual polish

---

# Git Commit Guidelines

Commit messages should be:
- Clear
- Concise
- Descriptive

Preferred:
```text
Add SMART temperature polling service
Implement swipe animation between screens
Create UNSC-inspired HUD panel widget
```

Avoid:
```text
fix stuff
update ui
changes
```

---

# Final Objective

PiNAS should feel like:
- A premium embedded appliance
- A futuristic tactical device
- A professional NAS dashboard
- A Halo-inspired UNSC terminal

The experience should combine:
- Functionality
- Reliability
- Tactical sci-fi aesthetics
- Smooth interaction
- Clean engineering
