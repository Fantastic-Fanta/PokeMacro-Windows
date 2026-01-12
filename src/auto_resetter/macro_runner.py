import time
import sys
from pathlib import Path
from typing import Optional

import requests

from .click_executor import ClickExecutor
from .windows_clicker import WindowsClicker
from .img_funcs import (
    OcrService,
    ScreenRegion,
    matches_config,
    trim_text_from_username_to_attempts,
    remove_chronos_event_phrase,
)
from .macro_config import DEFAULT_MACRO_CONFIG, MacroConfig


class MacroRunner:
    def __init__(
        self,
        config: MacroConfig,
        click_executor: Optional[ClickExecutor] = None,
        ocr_service: Optional[OcrService] = None,
        clicker: Optional[WindowsClicker] = None,
    ) -> None:
        self.config = config
        self.clicker = clicker or WindowsClicker()
        self.click_executor = click_executor or ClickExecutor(clicker=self.clicker)
        self.ocr_service = ocr_service or OcrService()
        
        self.screen_region = ScreenRegion(
            x=config.region.x,
            y=config.region.y,
            width=config.region.width,
            height=config.region.height,
        )
        
        if getattr(sys, 'frozen', False):
            exe_dir = Path(sys.executable).parent
            self.log_path = exe_dir / "history.log"
        else:
            current_file = Path(__file__)
            project_root = current_file.parent.parent.parent
            self.log_path = project_root / "history.log"

    def matches_config(self, text: str) -> bool:
        return matches_config(
            text,
            self.config.username,
            self.config.reskins,
            self.config.gradients,
            self.config.is_reskin,
            self.config.is_shiny,
            self.config.is_gradient,
            self.config.is_any,
            self.config.is_good,
        )

    def run(self) -> None:
        time.sleep(self.config.initial_delay_seconds)
        
        while True:
            self.click_executor.execute_mouse_clicks(self.config.click_sequence)
            time.sleep(self.config.post_click_delay_seconds)
            
            image = self.screen_region.capture()
            text = self.ocr_service.extract_text(image)
            text = remove_chronos_event_phrase(text)
            text = trim_text_from_username_to_attempts(text, self.config.username)
            
            if self.config.username.lower() in text.lower():
                self.log_username_detection(text)
            
            if self.matches_config(text):
                print(f"*** MATCH FOUND! ***\nMatched text: {text}")
                self.handle_match_found(text)
                break
            
            self.handle_no_match()
            time.sleep(self.config.between_iterations_delay_seconds)

    def handle_match_found(self, text: str) -> None:
        positions = self.config.positions
        
        for _ in range(3):
            self.clicker.click(*positions.dialogue_yes)
            time.sleep(0.1)
        
        self.clicker.click(*positions.menu_button)
        time.sleep(1.0)
        self.clicker.click(*positions.save_button)
        time.sleep(1.0)
        self.clicker.click(*positions.dialogue_yes)

    def handle_no_match(self) -> None:
        positions = self.config.positions
        self.clicker.click(*positions.quick_rejoin_sprite)
        time.sleep(0.2)
        self.clicker.click(*positions.quick_rejoin_button)

    def send_discord_webhook(self, text: str) -> None:
        webhook_url = self.config.discord_webhook
        if not webhook_url or not webhook_url.strip():
            return
        
        try:
            payload = {
                "content": f"```{text}```"
            }
            
            response = requests.post(webhook_url, json=payload, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Warning: Failed to send Discord webhook: {e}")

    def log_username_detection(self, text: str) -> None:
        with open(self.log_path, "a", encoding="utf-8") as log_file:
            log_file.write(text)
            log_file.write("\n" + "=" * 80 + "\n")
        
        self.send_discord_webhook(text)
