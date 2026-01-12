import warnings
import sys
from pathlib import Path

project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import pyautogui

warnings.filterwarnings("ignore", message=".*CUDA.*")
warnings.filterwarnings("ignore", message=".*MPS.*")
warnings.filterwarnings("ignore", message=".*pin_memory.*")
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

from auto_resetter.macro_config import load_config
from auto_resetter.macro_runner import MacroRunner
from auto_resetter.github_updater import GitHubUpdater
from auto_resetter.macro_config import DEFAULT_MACRO_CONFIG


def check_updates_on_startup():
    config = load_config()
    update_config = config.get("Update", {})
    
    check_on_startup = update_config.get("CheckOnStartup", True)
    if not check_on_startup:
        return
    
    auto_install = update_config.get("AutoInstall", False)
    
    try:
        updater = GitHubUpdater(
            repo_owner="Fantastic-Fanta",
            repo_name="PokeMacro-Windows"
        )
        
        updater.check_and_update(auto_install=auto_install, silent=False)
    except Exception as e:
        print(f"Error during update check: {e}")
        print("Continuing with current version...")


def main() -> None:
    check_updates_on_startup()
    
    pyautogui.FAILSAFE = True
    runner = MacroRunner(DEFAULT_MACRO_CONFIG)
    runner.run()


if __name__ == "__main__":
    main()
