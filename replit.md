# CORTEX AUTOMATION GRID

## Overview
A browser automation tool with a cyberpunk-themed web UI. Users can issue commands (open, click, type, wait, refresh) through a SocketIO-based interface, and the app uses SeleniumBase with headless Chromium to execute them and return screenshots.

## Project Architecture
- **Backend**: Python Flask + Flask-SocketIO with eventlet async
- **Frontend**: Single `index.html` served by Flask (no separate frontend build)
- **Browser Engine**: SeleniumBase with headless Chromium
- **Port**: 5000 (Flask serves both API and frontend)

### Directory Structure
```
app/
  main.py          - Flask app, routes, SocketIO handlers
  core/
    engine.py      - BrowserEngine class wrapping SeleniumBase
    executor.py    - Command parser and execution logic
  logging/
    logger.py      - LogManager for saving/loading project logs
index.html         - Frontend UI (served by Flask)
requirements.txt   - Python dependencies
```

### Key Dependencies
- Flask, flask-socketio, eventlet
- seleniumbase (browser automation)
- System: chromium, chromedriver, xvfb

## Recent Changes
- 2026-02-18: Initial Replit setup
  - Added __init__.py files for Python packages
  - Fixed download_log route bug (walrus operator misuse)
  - Made BrowserEngine lazy-initialized to avoid startup timeout
  - Configured chromium/chromedriver paths for Nix environment
  - Added error handling for screenshot in executor
  - Set deployment target to VM (stateful - maintains browser session)
