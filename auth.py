# auth.py
# ─────────────────────────────────────────────
#  AUTHENTICATION & REGISTRATION LOGIC
# ─────────────────────────────────────────────

from storage import load, save, hash_pw, USERS_FILE, RIDERS_FILE


# ── Users ──────────────────────────────────────

def login_user(username: str, password: str) -> dict | None:
    """Return the user dict if credentials match, else None."""
    for u in load(USERS_FILE):
        if u["username"] == username and u["password"] == hash_pw(password):
            return u
    return None


def register_user(username: str, password: str,
                  full_name: str, payment_method: str = "Cash") -> tuple[bool, str]:
    """
    Create a new user account.
    Returns (True, "") on success or (False, error_message) on failure.
    """
    users = load(USERS_FILE)
    if any(u["username"] == username for u in users):
        return False, "Username is already taken."

    users.append({
        "username":       username,
        "password":       hash_pw(password),
        "full_name":      full_name,
        "payment_method": payment_method,
        "email":          f"{username}@gmail.com",
    })
    save(USERS_FILE, users)
    return True, ""


# ── Riders ─────────────────────────────────────

def login_rider(username: str, password: str) -> dict | None:
    """Return the rider dict if credentials match, else None."""
    for r in load(RIDERS_FILE):
        if r["username"] == username and r["password"] == hash_pw(password):
            return r
    return None


def register_rider(username: str, password: str, full_name: str,
                   vehicle_type: str, vehicle_capacity: str) -> tuple[bool, str]:
    """
    Create a new rider account.
    Returns (True, "") on success or (False, error_message) on failure.
    """
    riders = load(RIDERS_FILE)
    if any(r["username"] == username for r in riders):
        return False, "Username is already taken."

    riders.append({
        "username":         username,
        "password":         hash_pw(password),
        "full_name":        full_name,
        "vehicle_type":     vehicle_type,
        "vehicle_capacity": vehicle_capacity,
        "available":        True,
        "email":            f"{username}@gmail.com",
    })
    save(RIDERS_FILE, riders)
    return True, ""
