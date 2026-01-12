# PokeMacro

An automated OCR-powered macro for Alpha Modded (PBB on Roblox) that automates the process of hunting Shiny, Gradient, and Reskin Pokemon by soft resetting eggs and monitoring chat notifications.

## Overview

PokeMacro automates the hunting process by:
- Automatically rejoining the game and executing click sequences
- Using OCR to monitor chat messages for rare Pokemon notifications
- Detecting Shiny, Gradient, or Reskin Pokemon based on configured criteria
- Automatically saving the game when matches are found
- Supporting optional Discord webhook notifications
- Including automatic update checking from GitHub

## Requirements

- Python 3.10 or higher
- Windows (primary support; macOS may require additional setup)
- Internet connection for first-time EasyOCR model download (~100MB)
- Roblox game window visible and accessible

## Installation

### From Source

1. Clone or download this repository

2. Create a virtual environment (recommended):
   ```bash
   python -m venv ENV
   ENV\Scripts\activate  # Windows
   # source ENV/bin/activate  # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure `configs.yaml` (see Configuration section)

5. Run the macro:
   ```bash
   python poke_macro_main.py
   ```

### Pre-built Executable

1. Download `PokeMacro.exe` from releases
2. Place `configs.yaml` in the same directory
3. Configure `configs.yaml` with your settings
4. Run `PokeMacro.exe`

Note: EasyOCR will download required models on first run. Internet connection required.

## Configuration

Configuration is done in `configs.yaml`. Default values are examples and must be configured for your setup.

### Configuration Structure

```yaml
# Roblox username (display name)
Username: "YourUsername"

# Discord webhook URL (optional, leave empty to disable)
DiscordWebhook: ""

# Pokemon wishlist
Wishlist:
  Reskins:
    - "Whiteout"
    - "Phantom"
    - "Glitch"
  Gradients:
    - "Gaia"
    - "Chronos"
    - "Nereus"

# UI element positions (screen coordinates)
Positions:
  TitleFiller: [1360, 277]
  Continue: [840, 507]
  EggManPosition: [1238, 615]
  DialogueYES: [1493, 390]
  QuickRejoinSprite: [1883, 944]
  QuickRejoinButton: [1057, 614]
  MenuButton: [21, 438]
  SaveButton: [74, 757]

# Chat window region for OCR
ChatWindow:
  LeftCorner: [14, 90]
  RightCorner: [445, 345]

# Matching mode (only one should be true)
IsReskin: false
IsShiny: true
IsGradient: false
IsAny: false
IsGood: false

# Update settings
Update:
  CheckOnStartup: false
  AutoInstall: false
```

### Matching Modes

- `IsShiny: true` - Matches Shiny Pokemon only
- `IsReskin: true` - Matches Reskins from wishlist only
- `IsGradient: true` - Matches Gradients from wishlist only
- `IsAny: true` - Matches any Pokemon in Reskins or Gradients wishlist
- `IsGood: true` - Matches combinations (Reskin+Gradient or Shiny+Gradient)

Only one matching mode flag should be `true` at a time.

### Distribution Notes

- Executable size: 200-500MB (includes Python and dependencies)
- First run: EasyOCR downloads models (~100MB), internet required
- Config file: Place `configs.yaml` next to `PokeMacro.exe` to customize settings
  - User config takes precedence over bundled config
  - Allows editing config without rebuilding

## Usage

1. Configure `configs.yaml` with your settings
2. Ensure Roblox is visible with chat window in configured region
3. Run: `python poke_macro_main.py` or `PokeMacro.exe`
4. Stop: Move mouse to top-left corner (failsafe) or press `Ctrl+C`

## Logging

Detected chat messages containing your username are logged to `history.log` (project root or next to executable). This assists with debugging and tracking hunt history.


## Important Notes

- Screen coordinates are absolute and resolution-dependent. Reconfigure if resolution changes.
- Game UI updates may require position adjustments.
- Test in a safe environment before extended use.
- `EggManPosition` may require frequent updates.
- Game window should remain in focus for best results.
- Internet required for first-time EasyOCR model download.

## License

MIT License

## Author

Manta

---

**Disclaimer**: This tool is for educational purposes. Use responsibly and in accordance with Roblox's Terms of Service.
