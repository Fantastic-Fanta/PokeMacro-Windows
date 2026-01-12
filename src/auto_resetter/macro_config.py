from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple, Union
import sys

import pyautogui
import yaml

ClickDict = Dict[str, Any]
ClickTuple = Union[
    Tuple[int, int],
    Tuple[int, int, float],
    Tuple[int, int, float, int, int, int, int, int, float],
]
ClickConfig = Union[ClickDict, ClickTuple]


@dataclass
class RegionConfig:
    x: int
    y: int
    width: int
    height: int


@dataclass
class PositionsConfig:
    egg_man_position: Tuple[int, int]
    dialogue_yes: Tuple[int, int]
    menu_button: Tuple[int, int]
    quick_rejoin_sprite: Tuple[int, int]
    quick_rejoin_button: Tuple[int, int]
    save_button: Tuple[int, int]
    title: Tuple[int, int]
    continue_card: Tuple[int, int]


def get_config_path() -> Optional[Path]:
    if getattr(sys, 'frozen', False):
        exe_dir = Path(sys.executable).parent
        user_config = exe_dir / "configs.yaml"
        if user_config.exists():
            return user_config
        else:
            base = Path(sys._MEIPASS)
            bundled = base / "configs.yaml"
            if bundled.exists():
                return bundled
    else:
        current = Path(__file__)
        base = current.parent.parent.parent
        config = base / "configs.yaml"
        return config
    return None


def load_config() -> Dict[str, Any]:
    config_path = get_config_path()
    
    if config_path is None or not config_path.exists():
        return {}
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def update_username(username: str) -> bool:
    config_path = get_config_path()
    
    if config_path is None or not config_path.exists():
        return False
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith("Username") or line.strip().startswith("username"):
                if ":" in line:
                    leading = line[:len(line) - len(line.lstrip())]
                    lines[i] = f'{leading}Username: "{username}"\n'
                    updated = True
                    break
        
        if updated:
            with open(config_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return True
        else:
            lines.insert(0, f'Username: "{username}"\n')
            with open(config_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return True
    except Exception as e:
        print(f"Warning: Failed to update username in config file: {e}")
        return False


def update_webhook(webhook: str) -> bool:
    config_path = get_config_path()
    
    if config_path is None or not config_path.exists():
        return False
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith("DiscordWebhook") or line.strip().startswith("discordwebhook"):
                if ":" in line:
                    leading = line[:len(line) - len(line.lstrip())]
                    if webhook:
                        lines[i] = f'{leading}DiscordWebhook: "{webhook}"\n'
                    else:
                        lines[i] = f'{leading}DiscordWebhook: ""\n'
                    updated = True
                    break
        
        if updated:
            with open(config_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return True
        else:
            username_idx = -1
            for i, line in enumerate(lines):
                if line.strip().startswith("Username") or line.strip().startswith("username"):
                    username_idx = i
                    break
            
            if username_idx >= 0:
                if webhook:
                    lines.insert(username_idx + 1, f'DiscordWebhook: "{webhook}"\n')
                else:
                    lines.insert(username_idx + 1, 'DiscordWebhook: ""\n')
            else:
                if webhook:
                    lines.insert(0, f'DiscordWebhook: "{webhook}"\n')
                else:
                    lines.insert(0, 'DiscordWebhook: ""\n')
            
            with open(config_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return True
    except Exception as e:
        print(f"Warning: Failed to update webhook in config file: {e}")
        return False


def prompt_username() -> str:
    while True:
        username = input("Please enter your display name: ").strip()
        if username:
            return username
        print("Username cannot be empty. Please try again.")


def prompt_webhook() -> str:
    webhook = input("Please enter your Discord webhook URL (or press Enter to skip): ").strip()
    return webhook


def print_matching_criteria():
    active = []
    if IS_RESKIN:
        active.append("Reskins")
    if IS_SHINY:
        active.append("Shiny")
    if IS_GRADIENT:
        active.append("Gradients")
    if IS_ANY:
        active.append("Any (Reskins or Gradients)")
    if IS_GOOD:
        active.append("Good (Reskin+Gradient or Shiny+Gradient)")
    
    if active:
        print(f"Hunting mode: {', '.join(active)} | Change this in configs.yaml in the matching criteria section if needed")
    else:
        print("Hunting mode: None (no matching criteria enabled)")
    
    print(f"\nReskins wishlist ({len(RESKINS)}): {', '.join(RESKINS)}")
    print(f"Gradients wishlist ({len(GRADIENTS)}): {', '.join(GRADIENTS)}")
    print(f"Username: {USERNAME if USERNAME else '(not set)'}")
    print()
    print("Instructions, please read and do them:")
    print("1. Go to settings, turn UI background transparency to max (opaque) for better OCR accuracy")
    print("2. A history.log file will be created in the same folder to track everything you've gotten")
    print("3. Recommended to test by faking a shiny in chat to see if saving works fine before you AFK")
    print()
    print("Software created by Manta, MIT license, refer to GitHub repo for source code, please minimise this window and wait for 60-70 seconds on the game's loading screen while this initialises...")


config = load_config()

wishlist = config.get("Wishlist", {})
RESKINS = wishlist.get("Reskins", ["Whiteout", "Phantom", "Glitch"])
GRADIENTS = wishlist.get("Gradients", ["Chronos", "Helios", "Gaia", "Nereus", "Nyx"])
USERNAME = config.get("Username", "")
DISCORD_WEBHOOK = config.get("DiscordWebhook", "")

if not USERNAME or USERNAME.strip() == "":
    new_username = prompt_username()
    if update_username(new_username):
        USERNAME = new_username
        config = load_config()
        USERNAME = config.get("Username", new_username)
        print(f"Username '{USERNAME}' has been saved to configs.yaml")
    else:
        USERNAME = new_username
        print(f"Warning: Could not save username to file. Using '{USERNAME}' for this session.")

if not DISCORD_WEBHOOK or DISCORD_WEBHOOK.strip() == "":
    new_webhook = prompt_webhook()
    if update_webhook(new_webhook):
        DISCORD_WEBHOOK = new_webhook
        config = load_config()
        DISCORD_WEBHOOK = config.get("DiscordWebhook", new_webhook)
        if DISCORD_WEBHOOK:
            print(f"Discord webhook has been saved to configs.yaml")
        else:
            print("Discord webhook left blank - webhook notifications disabled")
    else:
        DISCORD_WEBHOOK = new_webhook
        if DISCORD_WEBHOOK:
            print(f"Warning: Could not save webhook to file. Using webhook for this session.")
        else:
            print("Discord webhook left blank - webhook notifications disabled")

IS_RESKIN = config.get("IsReskin", False)
IS_SHINY = config.get("IsShiny", False)
IS_GRADIENT = config.get("IsGradient", False)
IS_ANY = config.get("IsAny", True)
IS_GOOD = config.get("IsGood", False)

print_matching_criteria()

@dataclass
class MacroConfig:
    region: RegionConfig
    click_sequence: Sequence[ClickConfig]
    positions: PositionsConfig
    username: str = USERNAME
    discord_webhook: str = DISCORD_WEBHOOK
    reskins: Optional[Sequence[str]] = None
    gradients: Optional[Sequence[str]] = None
    is_reskin: bool = IS_RESKIN
    is_shiny: bool = IS_SHINY
    is_gradient: bool = IS_GRADIENT
    is_any: bool = IS_ANY
    is_good: bool = IS_GOOD
    initial_delay_seconds: float = 3.0
    post_click_delay_seconds: float = 0.0
    between_iterations_delay_seconds: float = 2.0
    
    def __post_init__(self):
        if self.reskins is None:
            self.reskins = RESKINS
        if self.gradients is None:
            self.gradients = GRADIENTS


def load_positions() -> PositionsConfig:
    positions_yaml = config.get("Positions", {})
    
    def to_tuple(value: Any) -> Tuple[int, int]:
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            return (int(value[0]), int(value[1]))
        raise ValueError(value)
    
    return PositionsConfig(
        egg_man_position=to_tuple(positions_yaml.get("EggManPosition", [675, 739])),
        dialogue_yes=to_tuple(positions_yaml.get("DialogueYES", [1170, 405])),
        menu_button=to_tuple(positions_yaml.get("MenuButton", [43, 451])),
        quick_rejoin_sprite=to_tuple(positions_yaml.get("QuickRejoinSprite", [1475, 850])),
        quick_rejoin_button=to_tuple(positions_yaml.get("QuickRejoinButton", [1000, 580])),
        save_button=to_tuple(positions_yaml.get("SaveButton", [70, 735])),
        title=to_tuple(positions_yaml.get("TitleFiller", [70, 735])),
        continue_card=to_tuple(positions_yaml.get("Continue", [70, 735])),
    )


def load_region() -> RegionConfig:
    chat_window_yaml = config.get("ChatWindow", {})
    def to_tuple(value: Any) -> Tuple[int, int]:
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            return (int(value[0]), int(value[1]))
        raise ValueError(f"Invalid corner value: {value}")
    left = to_tuple(chat_window_yaml.get("LeftCorner", [13, 136]))
    right = to_tuple(chat_window_yaml.get("RightCorner", [440, 354]))
    
    return RegionConfig(
        x=left[0],
        y=left[1],
        width=right[0] - left[0],
        height=right[1] - left[1],
    )


def get_screen_center() -> Tuple[int, int]:
    size = pyautogui.size()
    return (size.width // 2, size.height // 2)


def get_chat_center(region: RegionConfig) -> Tuple[int, int]:
    return (
        region.x + region.width // 2,
        region.y + region.height // 2,
    )


def create_click_sequence(
    positions: PositionsConfig,
    screen_center: Tuple[int, int],
    chat_center: Tuple[int, int],
) -> Sequence[ClickConfig]:
    return [
        {
            "position": screen_center,
            "sleep": 1.0,
            "wait_for_pixel": {
                "position": positions.title,
                "color": (251, 239, 131),
                "timeout": 50.0,
            },
        },
        {
            "position": (10, screen_center[1]),
            "sleep": 0.2,
        },
        {
            "position": (10, screen_center[1] + 50),
            "sleep": 0.05,
        },
        {
            "position": screen_center,
            "sleep": 1.0,
            "wait_for_pixel": {
                "position": positions.continue_card,
                "color": (102, 255, 204),
                "timeout": 50.0,
            },
        },
        {
            "position": screen_center,
            "sleep": 0.05,
        },
        {
            "position": positions.egg_man_position,
            "sleep": 0.5,
            "wait_for_pixel": {
                "position": positions.menu_button,
                "color": (255, 255, 255),
                "timeout": 50.0,
            },
        },
        {
            "position": positions.egg_man_position,
            "sleep": 0.1,
        },
        {
            "position": positions.egg_man_position,
            "sleep": 0.2,
            "button": "right",
        },
        {
            "position": positions.dialogue_yes,
            "sleep": 0.2,
        },
        {
            "position": positions.dialogue_yes,
            "sleep": 0.1,
        },
        {
            "position": chat_center,
            "sleep": 0.1,
        },
    ]


DEFAULT_POSITIONS = load_positions()
DEFAULT_REGION = load_region()
SCREEN_CENTER = get_screen_center()
CHAT_WINDOW_CENTER = get_chat_center(DEFAULT_REGION)
DEFAULT_CLICK_SEQUENCE = create_click_sequence(
    DEFAULT_POSITIONS, SCREEN_CENTER, CHAT_WINDOW_CENTER
)

DEFAULT_MACRO_CONFIG = MacroConfig(
    region=DEFAULT_REGION,
    click_sequence=DEFAULT_CLICK_SEQUENCE,
    positions=DEFAULT_POSITIONS,
    username=USERNAME,
    discord_webhook=DISCORD_WEBHOOK,
    reskins=RESKINS,
    gradients=GRADIENTS,
    is_reskin=IS_RESKIN,
    is_shiny=IS_SHINY,
    is_gradient=IS_GRADIENT,
    is_any=IS_ANY,
    is_good=IS_GOOD,
)
