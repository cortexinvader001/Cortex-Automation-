from .engine import BrowserEngine

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
    action = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    eng = _get_engine()
    log_step = None
    try:
        if action == "open":
            res = eng.open(arg)
        elif action == "click":
            res = eng.click(arg)
        elif action == "type":
            selector, _, text = arg.partition(" ")
            res = eng.type(selector, text)
        elif action == "wait":
            res = eng.wait(float(arg))
        elif action == "refresh":
            res = eng.refresh()
        else:
            raise ValueError(f"Unknown command {action}")

        log_step = {"action": action.upper(), "arg": arg}
        return {
            "success": True,
            "log_step": log_step,
            "message": res["message"],
            "screenshot": eng.get_screenshot_base64()
        }
    except Exception as e:
        try:
            screenshot = eng.get_screenshot_base64()
        except Exception:
            screenshot = ""
        return {
            "success": False,
            "message": str(e),
            "screenshot": screenshot,
            "log_step": None
        }
