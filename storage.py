# storage.py
# ─────────────────────────────────────────────
#  DATA STORAGE  (JSON files, same folder)
# ─────────────────────────────────────────────

import os
import json
import hashlib

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
USERS_FILE    = os.path.join(BASE_DIR, "users.json")
RIDERS_FILE   = os.path.join(BASE_DIR, "riders.json")
BOOKINGS_FILE = os.path.join(BASE_DIR, "bookings.json")


def load(path):
    """Load a JSON file and return its contents, or an empty list on failure."""
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save(path, data):
    """Persist data to a JSON file."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def hash_pw(pw):
    """Return SHA-256 hex digest of a password string."""
    return hashlib.sha256(pw.encode()).hexdigest()
