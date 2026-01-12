# PokeMacro - Automated Shiny/Gradient Hunter

An automated OCR-powered macro for Alpha Modded (PBB on Roblox) that helps you hunt for Shiny, Gradient, and Reskin Pokemon by automatically soft resetting eggs and monitoring chat notifications.

## 🎯 Overview

PokeMacro automates the tedious process of hunting rare Pokemon variants by:
- Automatically rejoining the game and executing click sequences
- Using OCR (Optical Character Recognition) to monitor chat messages
- Detecting when you've obtained Shiny, Gradient, or Reskin Pokemon
- Automatically saving the game when a match is found
- Supporting Discord webhook notifications
- Including automatic update checking from GitHub

## ✨ Features

- **OCR-Powered Detection**: Automatically reads chat messages using EasyOCR to detect rare Pokemon
- **Automated Clicking**: Executes precise click sequences to navigate through the game UI
- **Pixel Color Detection**: Waits for specific UI elements to appear before proceeding
- **Flexible Matching Modes**: Hunt for specific types (Shiny, Gradient, Reskin) or any combination
- **Discord Integration**: Optional webhook notifications when rare Pokemon are found
- **Auto-Updates**: Built-in GitHub update checker with optional auto-install
- **Visual Config Tool**: Advanced GUI tool for easily configuring click positions
- **Cross-Platform**: Works on Windows (macOS support may vary)
- **YAML Configuration**: Easy-to-edit configuration file
- **Comprehensive Logging**: Tracks all detected chat messages to `history.log`

## 📋 Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows (primary support), macOS (may require additional setup)
- **Dependencies**: All listed in `requirements.txt`
- **Game Setup**: Roblox game window visible and accessible
- **Internet Connection**: Required for first-time EasyOCR model download (~100MB)

## 🚀 Installation

### Method 1: From Source

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv ENV
   ENV\Scripts\activate  # On Windows
   # On macOS/Linux: source ENV/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**:
   - Edit `configs.yaml` with your settings (see Configuration section)
   - Set your username, wishlist, and positions

5. **Run the macro**:
   ```bash
   python poke_macro_main.py
   ```

### Method 2: Using Pre-built Executable

1. **Download** `PokeMacro.exe` from releases
2. **Place** `configs.yaml` in the same directory as the executable
3. **Configure** `configs.yaml` with your settings
4. **Run** `PokeMacro.exe`

**Note**: On first run, EasyOCR will download required models. Ensure you have an internet connection.

## ⚙️ Configuration

**⚠️ IMPORTANT: You MUST configure the program before use!**

All configuration is done in `configs.yaml` at the root of the project. The default values are examples and will likely not work for your setup.

### Configuration File Structure

```yaml
# Your Roblox username (display name)
Username: "YourUsername"

# Discord webhook URL (optional - leave empty to skip webhook notifications)
DiscordWebhook: ""

# Pokemon wishlist - add names you want to hunt for
Wishlist:
  Reskins:
    - "Whiteout"
    - "Phantom"
    - "Glitch"
  Gradients:
    - "Gaia"
    - "Chronos"
    - "Nereus"
    # ... add more as needed

# UI element positions (coordinates for your screen resolution)
Positions:
  TitleFiller: [1360, 277]
  Continue: [840, 507]
  EggManPosition: [1238, 615]
  DialogueYES: [1493, 390]
  QuickRejoinSprite: [1883, 944]
  QuickRejoinButton: [1057, 614]
  MenuButton: [21, 438]
  SaveButton: [74, 757]

# Chat window region for OCR (defines the area to capture)
ChatWindow:
  LeftCorner: [14, 90]
  RightCorner: [445, 345]

# Matching mode flags (only one should be true)
IsReskin: false
IsShiny: true
IsGradient: false
IsAny: false
IsGood: false

# Update settings
Update:
  CheckOnStartup: false  # Set to true to check for updates on startup
  AutoInstall: false     # Set to true to automatically install updates
```

### 1. Username Configuration

Set your Roblox display name:
```yaml
Username: "YourRobloxUsername"
```

### 2. Wishlist Configuration

Add Pokemon names you want to hunt for:
```yaml
Wishlist:
  Reskins:
    - "Whiteout"
    - "Phantom"
    - "Glitch"
  Gradients:
    - "Gaia"
    - "Chronos"
    - "Nereus"
    # Add more as needed
```

### 3. Positions Configuration

All UI element positions need to be configured for your screen resolution. **Recommended**: Use the Config Tool (see below) to easily find coordinates.

**Available positions**:
- `TitleFiller`: Position on the title screen
- `Continue`: Continue button position
- `EggManPosition`: Position of the Egg NPC (may need frequent updates)
- `DialogueYES`: "YES" button in dialogue boxes
- `QuickRejoinSprite`: Quick rejoin sprite position
- `QuickRejoinButton`: Quick rejoin confirmation button
- `MenuButton`: Menu button (must be positioned on white text for pixel detection)
- `SaveButton`: Save button position

### 4. Chat Window Configuration

Define the region where the chat window appears for OCR:
```yaml
ChatWindow:
  LeftCorner: [14, 90]    # Top-left corner of chat window
  RightCorner: [445, 345] # Bottom-right corner of chat window
```

### 5. Matching Mode Configuration

Control what the macro should detect. **Only one flag should be `true` at a time**:

- `IsShiny: true` - Only matches Shiny Pokemon
- `IsReskin: true` - Only matches Reskins from your wishlist
- `IsGradient: true` - Only matches Gradients from your wishlist
- `IsAny: true` - Matches any Pokemon in your Reskins or Gradients wishlist
- `IsGood: true` - Matches "good" combinations (Reskin+Gradient or Shiny+Gradient)

**Example**: Hunt for any Shiny:
```yaml
IsShiny: true
IsAny: false
IsReskin: false
IsGradient: false
IsGood: false
```

### 6. Discord Webhook (Optional)

To receive Discord notifications when rare Pokemon are found:
```yaml
DiscordWebhook: "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
```

Leave empty to disable webhook notifications.

### 7. Update Settings

Control automatic update checking:
```yaml
Update:
  CheckOnStartup: true   # Check for updates when starting
  AutoInstall: false     # Automatically install updates without prompting
```

## 🛠️ Config Tool

A visual configuration tool is included to help you find mouse coordinates and configure positions easily.

### Building the Config Tool

```bash
build_config_tool.bat
```

Or manually:
```bash
pyinstaller config_tool.spec
```

### Using the Config Tool

1. **Run** `dist\ConfigTool.exe`
2. **Visual overlay** appears on your screen with draggable crosshairs
3. **Drag** the crosshairs to the correct positions on your game window
4. **Click Save** in the control panel to update `configs.yaml`
5. **Click Reset** to revert to original positions
6. **Close** the tool when done

The tool provides:
- Full-screen transparent overlay
- Draggable position markers for all UI elements
- Visual chat window region preview
- Real-time coordinate updates

## 📦 Building Executables

### Building the Main Application

To create a standalone Windows executable:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Build the executable**:
   ```bash
   pyinstaller poke_macro.spec
   ```

   Or use the batch file:
   ```batch
   build_exe.bat
   ```

3. **Find your executable**: The built executable will be in the `dist` folder as `PokeMacro.exe`

### Building the Config Tool

```bash
build_config_tool.bat
```

Or:
```bash
pyinstaller config_tool.spec
```

### Distribution Notes

- **Executable size**: The executable will be large (200-500MB) as it includes Python and all dependencies
- **First run**: EasyOCR will download models (~100MB) - users need internet connection
- **Config file**: Place `configs.yaml` next to `PokeMacro.exe` to customize settings
  - The executable will use your config file if it exists next to the executable
  - If no user config exists, it falls back to the bundled config
  - This allows users to edit their config without rebuilding

## 🎮 Usage

1. **Configure** `configs.yaml` with your settings (see Configuration section)

2. **Position your game window**:
   - Make sure Roblox is visible and the chat window is in the configured region
   - The game should be ready to be rejoined

3. **Run the macro**:
   ```bash
   python poke_macro_main.py
   ```
   
   Or if using the executable:
   ```bash
   PokeMacro.exe
   ```

4. **Stop the macro**:
   - Move your mouse to the top-left corner of the screen (PyAutoGUI failsafe)
   - Or press `Ctrl+C` in the terminal

## 🔄 How It Works

1. **Initialization**: The macro waits for an initial delay, then starts the loop

2. **Click Sequence**: Executes the configured click sequence to:
   - Navigate through the game UI
   - Wait for specific UI elements (using pixel color detection)
   - Select save slots
   - Navigate to the Egg NPC
   - Click through dialogue
   - Focus on the chat window

3. **OCR Detection**: 
   - Captures the chat window region
   - Uses EasyOCR to extract text
   - Processes text (removes noise, trims to relevant portions)

4. **Keyword Matching**: 
   - Checks if your username appears in the text
   - Logs to `history.log` if username is detected
   - Matches against configured wishlist and matching mode

5. **Match Found**: 
   - Clicks dialogue YES button multiple times
   - Opens menu
   - Saves the game
   - Sends Discord webhook notification (if configured)
   - Stops the macro

6. **No Match**: 
   - Clicks quick rejoin sprite
   - Clicks quick rejoin confirmation button
   - Waits for delay between iterations
   - Repeats the process

## 📝 Logging

When the macro detects your username in the chat, it automatically logs the detected text to `history.log` in the project root (or next to the executable). This helps you:
- Track what the OCR is detecting
- Debug configuration issues
- Review hunt history

## 🐛 Troubleshooting

### OCR Not Detecting Text

- Ensure the chat window region is correctly configured in `configs.yaml`
- Make sure the chat window is visible and not obscured
- Check that EasyOCR is properly installed (`pip install easyocr`)
- Ensure you have an internet connection for the first run (models need to be downloaded)
- Try adjusting the `ChatWindow` coordinates to capture more of the chat
- Check `history.log` to see what text is being detected

### Clicks Not Working

- Verify all positions in `configs.yaml` are correct for your screen resolution
- Use the Config Tool to verify positions visually
- Ensure the game window is in the foreground
- Check that your screen resolution matches the configured coordinates
- On Windows, ensure `pywinauto` is installed

### Pixel Color Detection Timing Out

- The click sequence includes pixel color detection for UI elements
- If timeouts occur, the game UI may have changed colors
- Check the terminal for timeout messages showing which pixel/color failed
- Verify `MenuButton` is positioned on white text

### Macro Stops Unexpectedly

- Check the terminal for error messages
- Verify all coordinates in `configs.yaml` are within your screen bounds
- Ensure the game hasn't changed its UI layout
- Check `history.log` to see if OCR is working correctly
- Verify your username is correctly set in the config

### Wrong Pokemon Detected

- Verify your matching mode flags in `configs.yaml` (only one should be true)
- Check that your wishlist contains the correct Pokemon names
- Ensure your username is correctly set
- Review `history.log` to see what text OCR is detecting
- Verify the matching mode logic matches your expectations

### Update Check Failing

- Check your internet connection
- Verify the repository name and owner in `github_updater.py` if you've forked
- Disable update checking by setting `CheckOnStartup: false` in config

## 🔒 Safety Features

- **Failsafe**: Move mouse to top-left corner to stop the macro immediately
- **Timeout Protection**: Pixel color detection has timeouts to prevent infinite waiting
- **Error Handling**: OCR errors are caught and handled gracefully
- **Logging**: All username detections are logged for debugging
- **Config Validation**: Configuration is validated on startup

## 📁 Project Structure

```
PokeMacro/
├── configs.yaml              # Main configuration file
├── history.log               # OCR detection log
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Package configuration
├── poke_macro_main.py        # Main entry point
├── poke_macro.spec           # PyInstaller spec for main app
├── config_tool.py            # Configuration tool source
├── config_tool.spec          # PyInstaller spec for config tool
├── build_config_tool.bat     # Build script for config tool
├── src/
│   └── auto_resetter/
│       ├── __init__.py
│       ├── macro_runner.py   # Main macro logic
│       ├── macro_config.py   # Configuration loading
│       ├── click_executor.py # Click sequence execution
│       ├── windows_clicker.py # Windows-specific clicking
│       ├── img_funcs.py      # OCR and image processing
│       ├── pixel_utils.py    # Pixel color detection
│       └── github_updater.py # Update checking
└── README.md
```

## 📌 Important Notes

- **Screen Resolution**: Screen coordinates are absolute and depend on your screen resolution. If you change resolution, you'll need to reconfigure positions.
- **Game Updates**: The macro assumes a specific game UI layout. If the game updates, you may need to adjust positions.
- **Testing**: Always test the macro in a safe environment before using it for extended periods
- **EggManPosition**: The `EggManPosition` may need frequent updates as it can change
- **Windows Focus**: The game window should remain in focus for best results
- **Internet Required**: First-time setup requires internet for EasyOCR model download

## 📄 License

MIT License

## 👤 Author

Manta

## 🙏 Acknowledgments

- EasyOCR for OCR capabilities
- PyAutoGUI for automation
- All contributors and users

