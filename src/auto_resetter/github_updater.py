import sys
import shutil
import subprocess
import time
import requests
from pathlib import Path
from typing import Optional, Tuple
from packaging import version

try:
    from . import __version__ as current_version
except ImportError:
    current_version = "0.1.2"


class GitHubUpdater:
    
    def __init__(self, repo_owner: str, repo_name: str):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        self.current_version = current_version
        
    def check_for_updates(self) -> Tuple[bool, Optional[str], Optional[str], Optional[str]]:
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            latest_version = data.get("tag_name", "0.0.0").lstrip('v')
            release_notes = data.get("body", "")
            
            assets = data.get("assets", [])
            download_url = None
            for asset in assets:
                asset_name = asset.get("name", "").lower()
                if asset_name.endswith(".exe") and "pokemacro" in asset_name:
                    download_url = asset.get("browser_download_url")
                    break
            
            if not download_url:
                for asset in assets:
                    if asset.get("name", "").endswith(".exe"):
                        download_url = asset.get("browser_download_url")
                        break
            
            if download_url and version.parse(latest_version) > version.parse(self.current_version):
                return True, latest_version, download_url, release_notes
            return False, latest_version, None, release_notes
            
        except requests.exceptions.RequestException as e:
            print(f"Error checking for updates: {e}")
            return False, None, None, None
        except Exception as e:
            print(f"Unexpected error checking for updates: {e}")
            return False, None, None, None
    
    def download_update(self, download_url: str, save_path: Optional[Path] = None) -> bool:
        try:
            if save_path is None:
                if getattr(sys, 'frozen', False):
                    exe_dir = Path(sys.executable).parent
                else:
                    exe_dir = Path(__file__).parent.parent.parent
                save_path = exe_dir / "PokeMacro_new.exe"
            
            print(f"\nDownloading update from GitHub...")
            print(f"Save location: {save_path}")
            
            headers = {
                'User-Agent': f'PokeMacro-Updater/{self.current_version}'
            }
            
            response = requests.get(download_url, stream=True, headers=headers, timeout=60)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            mb_downloaded = downloaded // 1024 // 1024
                            mb_total = total_size // 1024 // 1024
                            print(f"\rProgress: {percent:.1f}% ({mb_downloaded}MB / {mb_total}MB)", 
                                  end='', flush=True)
            
            print("\nDownload complete!")
            return True
            
        except Exception as e:
            print(f"\nError downloading update: {e}")
            return False
    
    def install_update(self, new_exe_path: Path) -> bool:
        try:
            if getattr(sys, 'frozen', False):
                current_exe = Path(sys.executable)
                exe_dir = current_exe.parent
            else:
                print("Cannot auto-update in development mode.")
                return False
            
            time.sleep(0.5)
            
            print(f"Installing update...")
            old_exe_path = exe_dir / f"{current_exe.stem}_old.exe"
            
            if old_exe_path.exists():
                try:
                    old_exe_path.unlink()
                except:
                    pass
            
            if current_exe.exists():
                try:
                    current_exe.rename(old_exe_path)
                except Exception as e:
                    print(f"Warning: Could not rename old executable: {e}")
                    try:
                        if sys.platform == 'win32':
                            subprocess.Popen(
                                f'timeout /t 1 /nobreak > nul && del /f "{current_exe}"',
                                shell=True,
                                creationflags=subprocess.CREATE_NO_WINDOW
                            )
                            time.sleep(1.5)
                        else:
                            current_exe.unlink()
                    except:
                        pass
            
            shutil.move(str(new_exe_path), str(current_exe))
            
            print("Cleaning up temporary files...")
            
            if old_exe_path.exists():
                try:
                    old_exe_path.unlink()
                except:
                    if sys.platform == 'win32':
                        try:
                            subprocess.Popen(
                                f'timeout /t 1 /nobreak > nul && del /f "{old_exe_path}"',
                                shell=True,
                                creationflags=subprocess.CREATE_NO_WINDOW
                            )
                        except:
                            pass
            
            for backup_file in exe_dir.glob(f"{current_exe.stem}_backup_*.exe"):
                try:
                    backup_file.unlink()
                except:
                    pass
            
            for new_file in exe_dir.glob(f"{current_exe.stem}_new.exe"):
                try:
                    new_file.unlink()
                except:
                    pass
            
            print("Update installed successfully!")
            print("Restarting application...")
            
            subprocess.Popen([str(current_exe)])
            sys.exit(0)
            
        except Exception as e:
            print(f"Error installing update: {e}")
            return False
    
    def check_and_update(self, auto_install: bool = False, silent: bool = False) -> bool:
        if not silent:
            print("Checking for updates...")
        
        has_update, latest_version, download_url, release_notes = self.check_for_updates()
        
        if not has_update:
            if not silent:
                print(f"Already up to date! (v{self.current_version})")
            return False
        
        if not silent:
            print()
            print(f"NEW VERSION AVAILABLE!")
            print(f"Current version: v{self.current_version}")
            print(f"Latest version:  v{latest_version}")
            print()
            if release_notes:
                print(f"\nRelease notes:\n{release_notes}")
                print(f"{'='*60}")
        
        if not auto_install:
            response = input("\nWould you like to install the update now? (y/n): ")
            if response.lower() != 'y':
                return False
        
        if getattr(sys, 'frozen', False):
            exe_dir = Path(sys.executable).parent
        else:
            exe_dir = Path(__file__).parent.parent.parent
        
        new_exe_path = exe_dir / "PokeMacro_new.exe"
        
        if self.download_update(download_url, new_exe_path):
            return self.install_update(new_exe_path)
        
        return False
