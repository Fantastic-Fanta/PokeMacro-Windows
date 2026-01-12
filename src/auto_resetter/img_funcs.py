import os
import re
import warnings
from contextlib import redirect_stdout, redirect_stderr
from dataclasses import dataclass
from io import StringIO
from typing import Sequence

os.environ["PYTHONWARNINGS"] = "ignore"
warnings.filterwarnings("ignore", message=".*CUDA.*")
warnings.filterwarnings("ignore", message=".*MPS.*")
warnings.filterwarnings("ignore", message=".*pin_memory.*")
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

import easyocr
import numpy as np
import pyautogui
from PIL import Image, ImageEnhance, ImageFilter


@dataclass
class ScreenRegion:
    x: int
    y: int
    width: int
    height: int

    def capture(self, save_debug: bool = False) -> Image.Image:
        screenshot = pyautogui.screenshot(
            region=(self.x, self.y, self.width, self.height)
        )
        if save_debug:
            screenshot.save("screenshot.png")
        return screenshot


class OcrService:
    def __init__(self, use_gpu: bool = True, max_image_size: int = 1920) -> None:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                self.ocr_engine = easyocr.Reader(['en'], gpu=use_gpu)
        self.max_image_size = max_image_size
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        width, height = image.size
        if width > self.max_image_size or height > self.max_image_size:
            if width > height:
                new_width = self.max_image_size
                new_height = int(height * (self.max_image_size / width))
            else:
                new_height = self.max_image_size
                new_width = int(width * (self.max_image_size / height))
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        image = image.filter(ImageFilter.SHARPEN)
        
        return image

    def extract_text(self, image: Image.Image) -> str:
        processed_image = self.preprocess_image(image)
        image_array = np.array(processed_image)
        
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            results = self.ocr_engine.readtext(image_array)
        
        text_parts = []
        for result in results:
            if isinstance(result, (list, tuple)) and len(result) >= 2:
                text_parts.append(str(result[1]))
        
        return " ".join(text_parts).strip()


def remove_chronos_event_phrase(text: str) -> str:
    pattern = r'\b[Cc]hronos\s+[Ee]vent\s+2025\s+is\s+out\b'
    result = re.sub(pattern, '', text, flags=re.IGNORECASE)
    result = re.sub(r'\s+', ' ', result).strip()
    return result


def trim_text_from_username_to_attempts(text: str, username: str) -> str:
    text_lower = text.lower()
    username_lower = username.lower()
    
    if username_lower not in text_lower:
        return text
    
    username_index = text_lower.find(username_lower)
    search_text_lower = text_lower[username_index:]
    attempts_index = search_text_lower.find("attempts")
    
    if attempts_index == -1:
        return text[username_index:]
    
    end_index = username_index + attempts_index + len("attempts")
    return text[username_index:end_index]


def matches_config(
    text: str,
    username: str,
    reskins: Sequence[str],
    gradients: Sequence[str],
    is_reskin: bool,
    is_shiny: bool,
    is_gradient: bool,
    is_any: bool,
    is_good: bool,
) -> bool:
    text_lower = text.lower()
    username_lower = username.lower()
    
    if "attemp" not in text_lower:
        return False
    if username_lower not in text_lower:
        return False
    
    has_reskin = any(reskin.lower() in text_lower for reskin in reskins)
    has_gradient = any(gradient.lower() in text_lower for gradient in gradients)
    has_shiny = "shiny" in text_lower
    
    if is_any:
        if not (has_reskin or has_gradient):
            return False
    
    if is_reskin and not has_reskin:
        return False
    
    if is_shiny and not has_shiny:
        return False
    
    if is_gradient and not has_gradient:
        return False
    
    if is_good:
        if not ((has_reskin and has_gradient) or (has_shiny and has_gradient)):
            return False
    
    return True
