"""Load shared logic from server/server.py for Vercel serverless functions."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_SERVER_PATH = ROOT / "server" / "server.py"

_spec = importlib.util.spec_from_file_location("practice_server", _SERVER_PATH)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)

load_catalog = _mod.load_catalog
load_deep = _mod.load_deep
offline_explain = _mod.offline_explain
