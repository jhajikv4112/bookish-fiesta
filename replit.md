# Firefox Browser Proxy

## Overview
A web-based visual browser proxy that allows users to browse websites through a Firefox-powered interface with built-in ad-blocking capabilities (similar to uBlock Origin). Users can access this through their browser and interact with websites visually in real-time.

## Architecture
- **Backend**: Python with aiohttp and WebSocket for real-time communication
- **Browser Engine**: Camoufox (Firefox-based) with built-in uBlock Origin for ad-blocking
- **Ad-blocking**: Built-in uBlock Origin addon in Camoufox
- **Frontend**: Vanilla JavaScript with Canvas for rendering, Tailwind CSS for styling

## Recent Changes
- 2025-11-17: Migrated from Playwright to Camoufox for better anti-detection and built-in ad-blocking
- 2025-11-17: Added keyboard input handling for interactive browsing
- 2025-11-17: Initial project setup

## Project Structure
```
/
├── server.py           # Main server with aiohttp, WebSocket, and Camoufox
├── public/
│   └── index.html      # Frontend UI with browser controls and keyboard input
├── requirements.txt    # Python dependencies
└── package.json        # Build configuration
```

## Features
- Real-time visual browsing through Firefox
- Ad-blocking via request interception
- Interactive controls (URL input, navigation, clicks)
- WebSocket-based screenshot streaming
- Public access for multiple users
