from .engine import BrowserEngine
import shlex
import json
import time

engine = None

def _get_engine():
    global engine
    if engine is None:
        engine = BrowserEngine()
    return engine

def execute_command(cmd: str):
    cmd = cmd.strip()
    if not cmd:
        raise ValueError("Empty command")

    parts = cmd.split(maxsplit=1)
    action = parts[0]
    arg = parts[1] if len(parts) > 1 else ""
    eng = _get_engine()
    log_step = None

    try:
        action_lower = action.lower()

        # --- Built-in wrappers ---
        if action_lower == "open":
            res = eng.open(arg)
        elif action_lower == "click":
            res = eng.click(arg)
        elif action_lower == "type":
            args_list = shlex.split(arg)
            selector = args_list[0]
            text = " ".join(args_list[1:])
            res = eng.type(selector, text)
        elif action_lower == "wait":
            res = eng.wait(float(arg))
        elif action_lower == "refresh":
            res = eng.refresh()
        elif action_lower == "get_cookies":
            res = {"cookies": eng.get_cookies(), "message": "Cookies fetched"}
        elif action_lower == "add_cookies":
            url, _, cookie_data = arg.partition(" ")
            cookies = json.loads(cookie_data)
            res = eng.add_cookies(url, cookies)
        elif action_lower == "close":
            eng.close()
            global engine
            engine = None
            res = {"message": "Browser closed"}

        # --- Dynamic SB passthrough ---
        else:
            args_list = shlex.split(arg)
            result = eng.sb_action(action_lower, *args_list)
            res = {"message": f"Called {action_lower} with args {args_list}", "result": result}

        log_step = {"action": action.upper(), "arg": arg}
        return {
            "success": True,
            "log_step": log_step,
            "message": res.get("message", ""),
            "result": res.get("result"),
            "cookies": res.get("cookies"),
            "screenshot": eng.get_screenshot_base64()
        }

    except Exception as e:
        try:
            time.sleep(1)
            screenshot = eng.get_screenshot_base64()
        except Exception:
            screenshot = ""
        return {
            "success": False,
            "message": str(e),
            "screenshot": screenshot,
            "log_step": None
        }
