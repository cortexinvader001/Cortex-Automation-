from flask import Flask, jsonify, send_file
from flask_socketio import SocketIO, emit
from app.core.executor import execute_command
from app.logging.logger import LogManager
import json, io, tempfile

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
log_manager = LogManager()

@app.route("")
def index():
    return send_file("../index.html")

@app.route("/save_project/<name>")
def save_project(name):
    return jsonify(log_manager.save_project(name))

@app.route("/projects")
def list_projects():
    import os as _os
    projects = []
    if _os.path.exists("projects"):
        for p in _os.listdir("projects"):
            path = f"projects/{p}"
            if _os.path.isdir(path):
                meta = {"name": p}
                log_file = f"{path}/execution_log.json"
                if _os.path.exists(log_file):
                    with open(log_file) as f:
                        meta["steps"] = len(json.load(f))
                projects.append(meta)
    return jsonify(projects)

@app.route("/download_log")
def download_current_log():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(log_manager.current_log, f, indent=2)
        temp_path = f.name
    return send_file(temp_path, mimetype="application/json", as_attachment=True, download_name="current_log.json")

@socketio.on("execute_command")
def handle_command(data):
    cmd = data.get("cmd", "")
    res = execute_command(cmd)
    if res["success"] and res["log_step"]:
        log_manager.append_step(res["log_step"])
    emit("command_result", {
        "success": res["success"],
        "message": res["message"],
        "screenshot": res["screenshot"]
    })

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)