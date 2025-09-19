# src/skills/todo.py
import json
import time
from pathlib import Path
from typing import Optional, List, Dict, Any


class TodoStore:
    """
    Tiny JSON-backed task store for hackathon demos.
    Schema:
      {
        "tasks": [
          {"id": 1712345678901, "text": "buy milk", "done": false, "due": "2025-09-20"}
        ]
      }
    """

    def __init__(self, path: str = "tasks.json"):
        self.path = Path(path)
        if not self.path.exists():
            self._write({"tasks": []})
        self._load()

    def _load(self) -> None:
        self.data = json.loads(self.path.read_text())

    def _write(self, d: Dict[str, Any]) -> None:
        self.path.write_text(json.dumps(d, indent=2))
        self.data = d

    def add(self, text: str, due: Optional[str] = None) -> int:
        tid = int(time.time() * 1000)
        self.data["tasks"].append(
            {"id": tid, "text": text.strip(), "done": False, "due": due}
        )
        self._write(self.data)
        return tid

    def list_open(self) -> List[Dict[str, Any]]:
        return [t for t in self.data["tasks"] if not t.get("done")]

    def complete(self, query: str) -> Optional[Dict[str, Any]]:
        q = query.strip().lower()
        for t in self.data["tasks"]:
            if str(t["id"]) == q or q in t["text"].lower():
                t["done"] = True
                self._write(self.data)
                return t
        return None
