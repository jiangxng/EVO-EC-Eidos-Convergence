from __future__ import annotations
from datetime import datetime, timezone
from uuid import uuid4
import json
from pathlib import Path

def now(): return datetime.now(timezone.utc).isoformat()
def uid(prefix:str): return f"{prefix}-{uuid4()}"
def load_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def dump_json(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");return p
