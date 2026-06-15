# main.py
# ─────────────────────────────────────────────
#  HARUUROT Ride Booking System — Entry Point
#  Run:  python main.py
# ─────────────────────────────────────────────

import tkinter as tk

from constants import C_BG, C_PURPLE_DARK, C_WHITE, C_ACCENT, C_SUBTEXT, PHONE_W, PHONE_H
from screens_auth import (
    build_welcome_login,
    build_user_login, build_user_register,
    build_register_choice,
    build_rider_gateway, build_rider_login, build_rider_register,
)
from screens_home import (
    build_user_home, build_book_ride, build_view_bookings,
    build_user_settings, build_user_info,
    build_rider_home, build_rider_settings,
    build_rider_jobs, build_rider_assigned, build_rider_availability,
    build_rider_info,
)


class HaruurotApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("HARUUROT Ride Booking")
        self.root.geometry(f"{PHONE_W}x{PHONE_H}")
        self.root.resizable(False, False)
        self.root.configure(bg=C_BG)

        self.current_user:  dict | None = None   # logged-in user/rider dict
        self.current_role:  str  | None = None   # "user" | "rider"
        self.current_frame: tk.Frame | None = None

        self.show_splash()

    # ── SCREEN MANAGEMENT ──────────────────────

    def clear(self) -> tk.Frame:
        """Destroy the current frame and return a fresh one."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, bg=C_BG)
        self.current_frame.pack(fill="both", expand=True)
        return self.current_frame

    # ── SCREEN DELEGATES ───────────────────────

    def show_splash(self):
        self._build_splash()

    def show_welcome_login(self):
        build_welcome_login(self)

    def show_user_login(self, error=""):
        build_user_login(self, error)

    def show_user_register(self, error=""):
        build_user_register(self, error)

    def show_register_choice(self):
        build_register_choice(self)

    def show_rider_gateway(self):
        build_rider_gateway(self)

    def show_rider_login(self, error=""):
        build_rider_login(self, error)

    def show_rider_register(self, error=""):
        build_rider_register(self, error)

    def show_user_home(self):
        build_user_home(self)

    def show_book_ride(self):
        build_book_ride(self)

    def show_view_bookings(self):
        build_view_bookings(self)

    def show_user_settings(self):
        build_user_settings(self)

    def show_user_info(self):
        build_user_info(self)

    def show_rider_home(self):
        build_rider_home(self)

    def show_rider_jobs(self):
        build_rider_jobs(self)

    def show_rider_assigned(self):
        build_rider_assigned(self)

    def show_rider_availability(self):
        build_rider_availability(self)

    def show_rider_settings(self):
        build_rider_settings(self)

    def show_rider_info(self):
        build_rider_info(self)

    # ══════════════════════════════════════════
    #  SPLASH SCREEN  (kept here; no external deps)
    # ══════════════════════════════════════════

    def _build_splash(self):
        frm = self.clear()
        frm.configure(bg=C_PURPLE_DARK)

        # ── Logo block (centered, upper half) ──
        logo_frm = tk.Frame(frm, bg=C_PURPLE_DARK)
        logo_frm.pack(expand=True, fill="both")

        # Spacer to push logo toward vertical center
        tk.Frame(logo_frm, bg=C_PURPLE_DARK, height=180).pack()

        # Circle + H icon
        canvas = tk.Canvas(logo_frm, width=100, height=100,
                           bg=C_PURPLE_DARK, highlightthickness=0)
        canvas.pack()
        canvas.create_oval(5, 5, 95, 95, fill=C_WHITE, outline="")
        canvas.create_text(50, 50, text="H",
                           font=("Helvetica", 36, "bold"), fill=C_ACCENT)

        tk.Label(logo_frm, text="HARUUROT",
                 font=("Helvetica", 26, "bold"),
                 bg=C_PURPLE_DARK, fg=C_WHITE).pack(pady=(14, 6))
        tk.Label(logo_frm, text="Ride Fast. Ride Safe. Ride Haruurot!",
                 font=("Helvetica", 11),
                 bg=C_PURPLE_DARK, fg="#C4B5FD").pack()

        # ── Buttons (pinned to bottom) ──
        btn_frm = tk.Frame(frm, bg=C_PURPLE_DARK)
        btn_frm.pack(fill="x", padx=24, pady=(0, 50))

        tk.Button(btn_frm, text="Login",
                  font=("Helvetica", 13, "bold"),
                  bg=C_WHITE, fg=C_PURPLE_DARK,
                  bd=0, padx=20, pady=14,
                  cursor="hand2", relief="flat",
                  command=self.show_welcome_login).pack(fill="x", pady=(0, 12))

        lnk = tk.Frame(btn_frm, bg=C_PURPLE_DARK)
        lnk.pack()
        tk.Label(lnk, text="Don't have an account? ",
                 font=("Helvetica", 12),
                 bg=C_PURPLE_DARK, fg=C_WHITE).pack(side="left")
        tk.Button(lnk, text="Register",
                  font=("Helvetica", 12),
                  bg=C_PURPLE_DARK, fg="#C084FC",
                  bd=0, cursor="hand2",
                  activebackground=C_PURPLE_DARK,
                  activeforeground="#C084FC",
                  command=self.show_register_choice).pack(side="left")


# ── RUN ────────────────────────────────────────
if __name__ == "__main__":
    window = tk.Tk()
    app    = HaruurotApp(window)
    window.mainloop()