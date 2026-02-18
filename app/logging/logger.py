import os
import json

class LogManager:
    def __init__(self, project_dir="projects"):
        self.project_dir = project_dir
        os.makedirs(project_dir, exist_ok=True)
        self.current_log = []
        self.step_counter = 0

    def append_step(self, step):
        self.step_counter += 1
        step["step"] = self.step_counter
        self.current_log.append(step)

    def save_project(self, name):
        project_path = os.path.join(self.project_dir, name)
        os.makedirs(project_path, exist_ok=True)
        log_file = os.path.join(project_path, "execution_log.json")
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(self.current_log, f, indent=2)
        self.current_log = []
        self.step_counter = 0
        return {"success": True, "message": f"Project saved to {log_file}"}

    def load_project(self, name):
        project_path = os.path.join(self.project_dir, name, "execution_log.json")
        if os.path.exists(project_path):
            with open(project_path, "r", encoding="utf-8") as f:
                self.current_log = json.load(f)
            self.step_counter = len(self.current_log)
            return {"success": True, "message": f"Loaded project {name}"}
        return {"success": False, "message": "Project not found"}
