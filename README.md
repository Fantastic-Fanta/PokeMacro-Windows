# PokeMacro

An automated OCR-powered macro for Alpha Modded (PBB on Roblox) that automates hunting Shiny, Gradient, and Reskin Pokemon by soft resetting eggs and monitoring chat notifications.

## Using Release Files

1. Download `PokeMacro.exe` from releases
2. Place `configs.yaml` in the same directory as the executable
3. Configure `configs.yaml` with your settings
4. Run `PokeMacro.exe`

Note: EasyOCR will download required models on first run. Internet connection required.

## Configuration

Edit `configs.yaml` with your settings:

```yaml
# Your Roblox username
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

## Matching Criteria

The matching mode flags control what the macro detects. Only one flag should be `true` at a time:

- **`IsShiny: true`** - Matches Shiny Pokemon only. Detects any Shiny Pokemon regardless of name.

- **`IsReskin: true`** - Matches Reskins from your wishlist only. Detects Pokemon that are Reskins AND appear in your `Wishlist.Reskins` list.

- **`IsGradient: true`** - Matches Gradients from your wishlist only. Detects Pokemon that are Gradients AND appear in your `Wishlist.Gradients` list.

- **`IsAny: true`** - Matches any Pokemon in your Reskins or Gradients wishlist. Detects Pokemon that appear in either `Wishlist.Reskins` or `Wishlist.Gradients`, regardless of whether they are Shiny.

- **`IsGood: true`** - Matches "good" combinations. Detects Pokemon that are either:
  - Reskin + Gradient (both variants)
  - Shiny + Gradient

## License

MIT License

## Author

Manta
