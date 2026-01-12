from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError


class WindowsClicker:
    def __init__(self, roblox_window_title: str = "Roblox") -> None:
        self.window_title = roblox_window_title
        self.app = None
        self.window = None
        self.window_rect = None
        self.connect()
    
    def connect(self) -> None:
        methods = [
            lambda: Application(backend="uia").connect(title_re=self.window_title),
            lambda: Application(backend="uia").connect(class_name="RobloxApp"),
            lambda: Application(backend="uia").connect(process="RobloxPlayerBeta.exe"),
            lambda: Application(backend="win32").connect(title_re=self.window_title),
            lambda: Application(backend="win32").connect(class_name="RobloxApp"),
        ]
        
        for method in methods:
            try:
                self.app = method()
                self.window = self.app.top_window()
                self.window_rect = self.window.rectangle()
                return
            except (ElementNotFoundError, Exception):
                continue
        
        raise RuntimeError(
            f"Could not connect to Roblox window. Make sure Roblox is running.\n"
            f"Tried to find window with title: '{self.window_title}'"
        )
    
    def get_window_rect(self) -> tuple:
        try:
            if self.window_rect is not None:
                self.window_rect = self.window.rectangle()
                return self.window_rect
        except Exception:
            pass
        
        if self.app is None or self.window is None:
            self.connect()
        else:
            try:
                self.window = self.app.top_window()
                self.window_rect = self.window.rectangle()
            except Exception:
                self.connect()
        
        return self.window_rect
    
    def click(self, x: int, y: int) -> None:
        self._click(x, y, button="left")
    
    def right_click(self, x: int, y: int) -> None:
        self._click(x, y, button="right")
    
    def _click(self, x: int, y: int, button: str = "left") -> None:
        if self.app is None or self.window is None:
            self.connect()
        
        try:
            rect = self.get_window_rect()
            window_x = rect.left
            window_y = rect.top
            rel_x = x - window_x
            rel_y = y - window_y
            
            if button == "right":
                self.window.click_input(button="right", coords=(rel_x, rel_y))
            else:
                self.window.click_input(coords=(rel_x, rel_y))
                
        except Exception as e:
            self.window = None
            self.window_rect = None
            error_msg = (
                f"Click failed: {e}\n"
                f"Attempted {button} click at absolute coordinates ({x}, {y})\n"
                f"Make sure Roblox window is open and accessible."
            )
            print(f"[Click] ERROR: {error_msg}")
            try:
                self.connect()
            except Exception:
                pass
            raise RuntimeError(error_msg) from e
