# screens_auth.py
# ─────────────────────────────────────────────
#  LOGIN & REGISTRATION SCREENS
# ─────────────────────────────────────────────

import tkinter as tk
from tkinter import messagebox

from constants import (
    C_PURPLE_DARK, C_PURPLE_LIGHT, C_BG, C_WHITE, C_TEXT, C_ACCENT, C_TEAL,
    C_PINK_BG, C_RED, C_GREEN, C_SUBTEXT,
    FONT_TITLE, FONT_H2, FONT_BODY, FONT_SMALL, FONT_BTN, FONT_LABEL,
)
from widgets import field, big_button, menu_card, scrollable
from auth import login_user, register_user, login_rider, register_rider


# ══════════════════════════════════════════════
#  WELCOME / LOGIN GATEWAY
# ══════════════════════════════════════════════

def build_welcome_login(app):
    frm = app.clear()
    frm.configure(bg=C_PURPLE_DARK)

    top = tk.Frame(frm, bg=C_PURPLE_DARK, padx=20, pady=16)
    top.pack(fill="x")
    tk.Button(top, text="←  Back", font=("Helvetica", 12),
              bg=C_PURPLE_DARK, fg="#C4B5FD", bd=0,
              activebackground=C_PURPLE_DARK, activeforeground="#C4B5FD",
              cursor="hand2",
              command=app.show_splash).pack(anchor="w")

    center = tk.Frame(frm, bg=C_PURPLE_DARK)
    center.pack(fill="both", expand=True)

    tk.Frame(center, bg=C_PURPLE_DARK, height=60).pack()

    cv = tk.Canvas(center, width=80, height=80, bg=C_PURPLE_DARK, highlightthickness=0)
    cv.pack()
    cv.create_oval(2, 2, 78, 78, fill=C_WHITE, outline="")
    cv.create_text(40, 40, text="H", font=("Helvetica", 32, "bold"), fill=C_ACCENT)

    tk.Label(center, text="Welcome!", font=("Helvetica", 26, "bold"),
             bg=C_PURPLE_DARK, fg=C_WHITE).pack(pady=(16, 4))
    tk.Label(center, text="Login as who?", font=("Helvetica", 12),
             bg=C_PURPLE_DARK, fg="#C4B5FD").pack()

    bottom = tk.Frame(frm, bg=C_PURPLE_DARK, padx=20, pady=24)
    bottom.pack(fill="x", side="bottom")

    def _login_choice_btn(parent, icon, text, bg, fg, cmd):
        btn = tk.Button(parent, text=f"{icon}   {text}",
                        font=("Helvetica", 13, "bold"),
                        bg=bg, fg=fg, bd=0, pady=14,
                        cursor="hand2", relief="flat",
                        activebackground=bg, activeforeground=fg,
                        command=cmd)
        btn.pack(fill="x", pady=(0, 12))

    _login_choice_btn(bottom, "👤", "Login as User", C_WHITE, C_PURPLE_DARK,
                       app.show_user_login)
    _login_choice_btn(bottom, "🚗", "Login as Rider", C_PURPLE_LIGHT, C_WHITE,
                       app.show_rider_gateway)

    lnk = tk.Frame(bottom, bg=C_PURPLE_DARK)
    lnk.pack()
    tk.Label(lnk, text="Don't have an account?  ", font=("Helvetica", 11),
             bg=C_PURPLE_DARK, fg=C_WHITE).pack(side="left")
    tk.Button(lnk, text="Register", font=("Helvetica", 11, "bold"),
              bg=C_PURPLE_DARK, fg="#C084FC", bd=0, cursor="hand2",
              activebackground=C_PURPLE_DARK, activeforeground="#C084FC",
              command=app.show_register_choice).pack(side="left")


# ══════════════════════════════════════════════
#  USER LOGIN
# ══════════════════════════════════════════════

def build_user_login(app, error=""):
    frm = app.clear()

    top = tk.Frame(frm, bg=C_BG, pady=10, padx=20)
    top.pack(fill="x")
    tk.Button(top, text="←", font=("Helvetica", 16),
              bg=C_BG, fg=C_TEXT, bd=0, cursor="hand2",
              command=app.show_welcome_login).pack(anchor="w")
    tk.Label(top, text="Welcome Back, User!", font=FONT_TITLE,
             bg=C_BG, fg=C_ACCENT).pack(anchor="w", pady=(4, 0))
    tk.Label(top, text="Login to continue.", font=FONT_BODY,
             bg=C_BG, fg=C_TEXT).pack(anchor="w")

    body = tk.Frame(frm, bg=C_BG, padx=20)
    body.pack(fill="both", expand=True)

    if error:
        err_box = tk.Frame(body, bg=C_PINK_BG, bd=1, relief="solid", padx=10, pady=8)
        err_box.pack(fill="x", pady=(10, 0))
        tk.Label(err_box, text=error, font=FONT_SMALL,
                 bg=C_PINK_BG, fg=C_RED, wraplength=300).pack()

    _, u_ent = field(body, "Username", "Enter username")
    _, p_ent = field(body, "Password", "Enter password", password=True)

    rem_frm = tk.Frame(body, bg=C_BG)
    rem_frm.pack(fill="x", pady=8)
    tk.Checkbutton(rem_frm, bg=C_BG, activebackground=C_BG).pack(side="left")
    tk.Label(rem_frm, text="Remember Me", font=FONT_BODY, bg=C_BG).pack(side="left")

    def do_login():
        uname = u_ent.get().strip()
        pw    = p_ent.get().strip()
        if not uname or uname == "Enter username" or not pw or pw == "Enter password":
            app.show_user_login("Invalid username or password.")
            return
        user = login_user(uname, pw)
        if user:
            app.current_user = user
            app.current_role = "user"
            app.show_user_home()
        else:
            app.show_user_login("Invalid username or password.")

    big_button(body, "Login", do_login, pady=14)

    tk.Button(body, text="Forgot Password?", font=FONT_BODY,
              bg=C_BG, fg=C_ACCENT, bd=0, cursor="hand2",
              command=lambda: messagebox.showinfo(
                  "Forgot Password", "Please contact support to reset your password.")
              ).pack(pady=6)


# ══════════════════════════════════════════════
#  REGISTER CHOICE
# ══════════════════════════════════════════════

def build_register_choice(app):
    frm = app.clear()

    top = tk.Frame(frm, bg=C_BG, pady=10, padx=20)
    top.pack(fill="x")
    tk.Button(top, text="←", font=("Helvetica", 16),
              bg=C_BG, fg=C_TEXT, bd=0, cursor="hand2",
              command=app.show_splash).pack(anchor="w")
    tk.Label(top, text="User Registration", font=FONT_TITLE,
             bg=C_BG, fg=C_ACCENT).pack(anchor="w")
    tk.Label(top, text="Join us by creating an account.",
             font=FONT_BODY, bg=C_BG, fg=C_TEXT).pack(anchor="w")

    body = tk.Frame(frm, bg=C_BG, padx=20)
    body.pack(fill="both", expand=True, pady=20)
    tk.Label(body, text="I want to register as:", font=("Helvetica", 12, "bold"),
             bg=C_BG, fg=C_TEXT, anchor="w").pack(fill="x", pady=(0, 10))

    def _make_choice_card(parent, icon, icon_bg, title, title_color, desc, cmd):
        card = tk.Frame(parent, bg=C_WHITE, bd=2, relief="solid", cursor="hand2")
        card.pack(fill="x", pady=6)
        row = tk.Frame(card, bg=C_WHITE, padx=12, pady=12)
        row.pack(fill="x")

        ib = tk.Frame(row, bg=icon_bg, width=52, height=52)
        ib.pack(side="left", padx=(0, 10))
        ib.pack_propagate(False)
        icon_lbl = tk.Label(ib, text=icon, font=("Helvetica", 20), bg=icon_bg)
        icon_lbl.place(relx=0.5, rely=0.5, anchor="center")

        tx = tk.Frame(row, bg=C_WHITE)
        tx.pack(side="left", fill="both", expand=True)
        tk.Label(tx, text=title, font=("Helvetica", 13, "bold"),
                 bg=C_WHITE, fg=title_color).pack(anchor="w")
        tk.Label(tx, text=desc, font=FONT_SMALL, bg=C_WHITE, fg=C_SUBTEXT,
                 wraplength=200, justify="left").pack(anchor="w")

        tk.Label(row, text="›", font=("Helvetica", 20), bg=C_WHITE, fg=title_color).pack(side="right")

        def _bind_all(w):
            w.bind("<Button-1>", lambda e: cmd())
            w.configure(cursor="hand2")
            for ch in w.winfo_children():
                _bind_all(ch)
        _bind_all(card)

    _make_choice_card(body, "👤", "#DDD6FE", "User", C_ACCENT,
                      "Book rides, track trips, and travel easily.",
                      app.show_user_register)
    _make_choice_card(body, "🚗", "#CCFBF1", "Rider", C_TEAL,
                      "Ride with us, accept bookings, and drive easily.",
                      app.show_rider_register)

    sep = tk.Frame(body, bg=C_BG)
    sep.pack(fill="x", pady=10)
    tk.Label(sep, text="or", font=FONT_SMALL, bg=C_BG, fg=C_SUBTEXT).pack()

    lnk = tk.Frame(body, bg=C_BG)
    lnk.pack()
    tk.Label(lnk, text="Already have an account? ", font=FONT_BODY,
             bg=C_BG, fg=C_TEXT).pack(side="left")
    tk.Button(lnk, text="Login", font=FONT_BODY, bg=C_BG, fg=C_ACCENT, bd=0,
              cursor="hand2", command=app.show_welcome_login).pack(side="left")


# ══════════════════════════════════════════════
#  USER REGISTER
# ══════════════════════════════════════════════

def build_user_register(app, error=""):
    frm = app.clear()

    top = tk.Frame(frm, bg=C_BG, pady=10, padx=20)
    top.pack(fill="x")
    tk.Button(top, text="←", font=("Helvetica", 16),
              bg=C_BG, fg=C_TEXT, bd=0, cursor="hand2",
              command=app.show_register_choice).pack(anchor="w")
    tk.Label(top, text="User Registration", font=FONT_TITLE,
             bg=C_BG, fg=C_ACCENT).pack(anchor="w")
    tk.Label(top, text="Fill in the details to create your account as a user.",
             font=FONT_BODY, bg=C_BG, fg=C_TEXT, wraplength=340, justify="left").pack(anchor="w")

    body = tk.Frame(frm, bg=C_BG, padx=20)
    body.pack(fill="both", expand=True)

    u_err = tk.StringVar()
    _, u_ent  = field(body, "Username",                  "Enter username",                       error_var=u_err)
    _, p_ent  = field(body, "Password",                  "Enter password",                       password=True)
    _, n_ent  = field(body, "Full Name",                 "Enter your full name")
    _, pm_ent = field(body, "Payment Method (Optional)", "Credit/Debit Cards, Cash, E-Wallet")

    rem_frm = tk.Frame(body, bg=C_BG)
    rem_frm.pack(fill="x", pady=6)
    tk.Checkbutton(rem_frm, bg=C_BG, activebackground=C_BG).pack(side="left")
    tk.Label(rem_frm, text="Remember Me", font=FONT_BODY, bg=C_BG).pack(side="left")

    status_lbl = tk.Label(body, text="", font=FONT_BODY, bg=C_BG, fg=C_GREEN)
    status_lbl.pack()

    def do_register():
        uname = u_ent.get().strip()
        pw    = p_ent.get().strip()
        name  = n_ent.get().strip()
        pm    = pm_ent.get().strip()

        if not uname or uname == "Enter username":
            u_err.set("Username is required"); return
        if not pw or pw == "Enter password":
            messagebox.showerror("Error", "Password is required"); return
        if not name or name == "Enter your full name":
            messagebox.showerror("Error", "Full Name is required"); return

        if pm in ("Credit/Debit Cards, Cash, E-Wallet", ""):
            pm = "Cash"

        ok, err = register_user(uname, pw, name, pm)
        if not ok:
            u_err.set(err); return

        u_err.set("")
        status_lbl.config(text="Registration successful!")
        frm.after(1000, app.show_user_login)

    big_button(body, "Register", do_register, pady=14)

    lnk = tk.Frame(body, bg=C_BG)
    lnk.pack(pady=6)
    tk.Label(lnk, text="Already have an account? ", font=FONT_BODY,
             bg=C_BG, fg=C_TEXT).pack(side="left")
    tk.Button(lnk, text="Login", font=FONT_BODY, bg=C_BG, fg=C_ACCENT, bd=0,
              cursor="hand2", command=app.show_user_login).pack(side="left")


# ══════════════════════════════════════════════
#  RIDER GATEWAY
# ══════════════════════════════════════════════

def build_rider_gateway(app):
    frm = app.clear()

    top = tk.Frame(frm, bg=C_BG, pady=10, padx=20)
    top.pack(fill="x")
    tk.Button(top, text="←", font=("Helvetica", 16),
              bg=C_BG, fg=C_TEXT, bd=0, cursor="hand2",
              command=app.show_welcome_login).pack(anchor="w")

    body = tk.Frame(frm, bg=C_BG)
    body.pack(fill="both", expand=True, pady=40)

    tk.Label(body, text="📋", font=("Helvetica", 64), bg=C_BG).pack(pady=(0, 10))
    tk.Label(body, text="Do you have an\nexisting account?",
             font=("Helvetica", 18, "bold"), bg=C_BG, fg=C_ACCENT, justify="center").pack()
    tk.Label(body, text="Please choose an option to continue.",
             font=FONT_BODY, bg=C_BG, fg=C_TEXT, justify="center").pack(pady=10)

    big_button(body, "Yes, I have an account", app.show_rider_login, pady=14)
    tk.Button(body, text="No, I'm a new rider", font=FONT_BTN,
              bg=C_WHITE, fg=C_ACCENT, bd=1, relief="solid", padx=20, pady=14,
              cursor="hand2", command=app.show_rider_register).pack(fill="x", padx=20, pady=6)


# ══════════════════════════════════════════════
#  RIDER LOGIN
# ══════════════════════════════════════════════

def build_rider_login(app, error=""):
    frm = app.clear()

    top = tk.Frame(frm, bg=C_BG, pady=10, padx=20)
    top.pack(fill="x")
    tk.Button(top, text="←", font=("Helvetica", 16),
              bg=C_BG, fg=C_TEXT, bd=0, cursor="hand2",
              command=app.show_rider_gateway).pack(anchor="w")
    tk.Label(top, text="Welcome Back, Rider!", font=FONT_TITLE,
             bg=C_BG, fg=C_ACCENT).pack(anchor="w", pady=(4, 0))
    tk.Label(top, text="Login to continue.", font=FONT_BODY,
             bg=C_BG, fg=C_TEXT).pack(anchor="w")

    body = tk.Frame(frm, bg=C_BG, padx=20)
    body.pack(fill="both", expand=True)

    if error:
        err_box = tk.Frame(body, bg=C_PINK_BG, bd=1, relief="solid", padx=10, pady=8)
        err_box.pack(fill="x", pady=(10, 0))
        tk.Label(err_box, text=error, font=FONT_SMALL,
                 bg=C_PINK_BG, fg=C_RED).pack()

    _, u_ent = field(body, "Username", "Enter username")
    _, p_ent = field(body, "Password", "Enter password", password=True)

    rem_frm = tk.Frame(body, bg=C_BG)
    rem_frm.pack(fill="x", pady=8)
    tk.Checkbutton(rem_frm, bg=C_BG, activebackground=C_BG).pack(side="left")
    tk.Label(rem_frm, text="Remember Me", font=FONT_BODY, bg=C_BG).pack(side="left")

    def do_login():
        uname = u_ent.get().strip()
        pw    = p_ent.get().strip()
        if not uname or uname == "Enter username" or not pw or pw == "Enter password":
            app.show_rider_login("Invalid username or password.")
            return
        rider = login_rider(uname, pw)
        if rider:
            app.current_user = rider
            app.current_role = "rider"
            app.show_rider_home()
        else:
            app.show_rider_login("Invalid username or password.")

    big_button(body, "Login", do_login, pady=14)

    tk.Button(body, text="Forgot Password?", font=FONT_BODY,
              bg=C_BG, fg=C_ACCENT, bd=0, cursor="hand2",
              command=lambda: messagebox.showinfo(
                  "Forgot Password", "Please contact support to reset your password.")
              ).pack(pady=6)


# ══════════════════════════════════════════════
#  RIDER REGISTER
# ══════════════════════════════════════════════

def build_rider_register(app, error=""):
    frm = app.clear()

    top = tk.Frame(frm, bg=C_BG, pady=10, padx=20)
    top.pack(fill="x")
    tk.Button(top, text="←", font=("Helvetica", 16),
              bg=C_BG, fg=C_TEXT, bd=0, cursor="hand2",
              command=app.show_register_choice).pack(anchor="w")
    tk.Label(top, text="Rider Registration", font=FONT_TITLE,
             bg=C_BG, fg=C_ACCENT).pack(anchor="w")
    tk.Label(top, text="Fill in the details to create your account as a rider.",
             font=FONT_BODY, bg=C_BG, fg=C_TEXT, wraplength=340, justify="left").pack(anchor="w")

    _, _, body_scroll = scrollable(frm)
    pad = tk.Frame(body_scroll, bg=C_BG, padx=20)
    pad.pack(fill="x")

    u_err = tk.StringVar()
    _, u_ent  = field(pad, "Username",                    "Enter username",        error_var=u_err)
    _, p_ent  = field(pad, "Password",                    "Enter password",        password=True)
    _, n_ent  = field(pad, "Full Name",                   "Enter your full name")
    _, vt_ent = field(pad, "Vehicle Type (Car/Van/Motorcycle)", "Enter vehicle type")
    _, vc_ent = field(pad, "Vehicle Capacity",            "Enter vehicle capacity")

    rem_frm = tk.Frame(pad, bg=C_BG)
    rem_frm.pack(fill="x", pady=6)
    tk.Checkbutton(rem_frm, bg=C_BG, activebackground=C_BG).pack(side="left")
    tk.Label(rem_frm, text="Remember Me", font=FONT_BODY, bg=C_BG).pack(side="left")

    status_lbl = tk.Label(pad, text="", font=FONT_BODY, bg=C_BG, fg=C_GREEN)
    status_lbl.pack()

    def do_register():
        uname = u_ent.get().strip()
        pw    = p_ent.get().strip()
        name  = n_ent.get().strip()
        vtype = vt_ent.get().strip().capitalize()
        vcap  = vc_ent.get().strip()

        if not uname or uname == "Enter username":
            u_err.set("Username is required"); return
        if not pw or pw == "Enter password":
            messagebox.showerror("Error", "Password is required"); return
        if not name or name == "Enter your full name":
            messagebox.showerror("Error", "Full Name is required"); return
        if vtype not in ("Car", "Van", "Bike", "Motorcycle"):
            messagebox.showerror("Error", "Vehicle Type must be Car, Van, or Motorcycle"); return
        if not vcap or vcap == "Enter vehicle capacity":
            messagebox.showerror("Error", "Vehicle Capacity is required"); return

        ok, err = register_rider(uname, pw, name, vtype, vcap)
        if not ok:
            u_err.set(err); return

        u_err.set("")
        status_lbl.config(text="Registration successful!")
        pad.after(1000, app.show_rider_login)

    btn_frm = tk.Frame(pad, bg=C_BG)
    btn_frm.pack(fill="x")
    big_button(btn_frm, "Register", do_register, pady=14)

    lnk = tk.Frame(pad, bg=C_BG)
    lnk.pack(pady=6)
    tk.Label(lnk, text="Already have an account? ", font=FONT_BODY,
             bg=C_BG, fg=C_TEXT).pack(side="left")
    tk.Button(lnk, text="Login", font=FONT_BODY, bg=C_BG, fg=C_ACCENT, bd=0,
              cursor="hand2", command=app.show_rider_login).pack(side="left")