from seleniumbase import SB
import os
import subprocess
import time
from selenium.webdriver.common.keys import Keys

os.environ["DISPLAY"] = ":99"

def _find_binary(name):
    result = subprocess.run(["which", name], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None

class BrowserEngine:
    def __init__(self):
        chromium_path = _find_binary("chromium") or _find_binary("chromium-browser")
        chromedriver_path = _find_binary("chromedriver")

        sb_kwargs = {
            "uc": False,
            "headed": False,
            "browser": "chrome",
            "chromium_arg": [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--window-size=1200,900",
                "--headless=new",
                "--disable-setuid-sandbox",
                "--disable-extensions",
            ],
        }
        if chromium_path:
            sb_kwargs["binary_location"] = chromium_path
        if chromedriver_path:
            os.environ["CHROMEDRIVER_PATH"] = chromedriver_path

        self.sb_cm = SB(**sb_kwargs)
        self.sb = self.sb_cm.__enter__()
        self.sb.sleep(0.5)

    # --- Core wrappers ---
    def open(self, url: str):
        self.sb.open(url)
        return {"success": True, "message": f"Opened {url}"}

    def click(self, selector: str):
        self.sb.click(selector)
        return {"success": True, "message": f"Clicked {selector}"}

    def type(self, selector: str, text: str):
        self.sb.click(selector)
        for ch in text:
            self.sb.send_keys(selector, ch)
            self.sb.sleep(0.05)
        self.sb.sleep(0.4)
        self.sb.send_keys(selector, Keys.ENTER)
        return {"success": True, "message": f"Typed into {selector}"}

    def wait(self, seconds: float):
        self.sb.sleep(seconds)
        return {"success": True, "message": f"Waited {seconds}s"}

    def refresh(self):
        self.sb.refresh()
        return {"success": True, "message": "Refreshed page"}

    # --- Cookies ---
    def get_cookies(self):
        return self.sb.driver.get_cookies()

    def add_cookies(self, url: str, cookies):
        self.sb.open(url)
        for cookie in cookies:
            try:
                self.sb.driver.add_cookie(cookie)
            except Exception:
                pass
        self.sb.refresh()
        return {"success": True, "message": f"Loaded {len(cookies)} cookies"}

    # --- Generic SB passthrough ---
    def sb_action(self, method_name: str, *args, **kwargs):
        method = getattr(self.sb, method_name, None)
        if not method:
            raise ValueError(f"No such SeleniumBase method '{method_name}'")
        return method(*args, **kwargs)

    # --- Screenshots ---
    def get_screenshot_base64(self):
        return self.sb.driver.get_screenshot_as_base64()

    # --- Proper shutdown ---
    def close(self):
        if self.sb_cm:
            self.sb_cm.__exit__(None, None, None)
            self.sb_cm = None
            self.sb = None
