from .engine import BrowserEngine

engine = BrowserEngine()

def execute_command(cmd: str):
    cmd = cmd.strip()
    if not cmd:
        raise ValueError("Empty command")

    parts = cmd.split(maxsplit=1)
    action = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    log_step = None
    try:
        if action == "open":
            res = engine.open(arg)
        elif action == "click":
            res = engine.click(arg)
        elif action == "type":
            selector, _, text = arg.partition(" ")
            res = engine.type(selector, text)
        elif action == "wait":
            res = engine.wait(float(arg))
        elif action == "refresh":
            res = engine.refresh()
        else:
            raise ValueError(f"Unknown command {action}")

        log_step = {"action": action.upper(), "arg": arg}
        return {
            "success": True,
            "log_step": log_step,
            "message": res["message"],
            "screenshot": engine.get_screenshot_base64()
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "screenshot": engine.get_screenshot_base64(),
            "log_step": None
        }
