from seleniumbase import SB


class BrowserEngine:
    def __init__(self):
        # Start persistent SeleniumBase session
        self.sb = SB(
            uc=True,
            headed=False,
            browser="chrome",
            chromium_arg=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--window-size=1200,900",
                "--headless=new"
            ]
        )
        # Manually enter the context (since we want persistence)
        self.sb.__enter__()

    # -------- Core Controls -------- #

    def open(self, url: str):
        self.sb.open(url)
        return {"success": True, "message": f"Opened {url}"}

    def click(self, selector: str):
        self.sb.click(selector)
        return {"success": True, "message": f"Clicked {selector}"}

    def type(self, selector: str, text: str):
        self.sb.type(selector, text, human=True)
        return {"success": True, "message": f"Typed into {selector}"}

    def wait(self, seconds: float):
        self.sb.sleep(seconds)
        return {"success": True, "message": f"Waited {seconds}s"}

    def refresh(self):
        self.sb.refresh()
        return {"success": True, "message": "Refreshed page"}

    # -------- Data Extraction -------- #

    def get_screenshot_base64(self):
        return self.sb.driver.get_screenshot_as_base64()

    def get_cookies(self):
        return self.sb.driver.get_cookies()

    def add_cookies(self, cookies):
        for cookie in cookies:
            try:
                self.sb.driver.add_cookie(cookie)
            except Exception:
                pass

        self.sb.refresh()
        return {"success": True, "message": f"Loaded {len(cookies)} cookies"}

    # -------- Proper Shutdown -------- #

    def close(self):
        """Cleanly stop browser (IMPORTANT)."""
        if self.sb:
            self.sb.__exit__(None, None, None)
            self.sb = None
