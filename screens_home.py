# screens_home.py
# ─────────────────────────────────────────────
#  USER HOME, BOOK RIDE, VIEW BOOKINGS,
#  SETTINGS, RIDER HOME  —  all screens
# ─────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk, messagebox

from constants import (
    C_PURPLE_DARK, C_PURPLE_MID, C_PURPLE_LIGHT,
    C_BG, C_WHITE, C_TEXT, C_SUBTEXT, C_ACCENT, C_TEAL,
    C_GREEN, C_RED,
    FONT_H2, FONT_BODY, FONT_SMALL, FONT_LABEL,
)
from widgets import scrollable, field
from booking import (
    create_booking, get_user_bookings,
    get_pending_bookings_for_vehicle, get_rider_bookings, assign_booking,
    cancel_booking, complete_booking,
)
from storage import load, save, hash_pw, USERS_FILE, RIDERS_FILE

PHP = "₱"   # peso sign used everywhere instead of $

def _vehicle_display(vtype: str) -> str:
    """Return the user-facing label for a vehicle type key."""
    return "Motorcycle" if vtype == "Bike" else vtype


# ── Project credits data ───────────────────────
PROJECT_CREDITS = [
    {
        "name": "Marianne E. Salvador",
        "email": "marianneesalvador@gmail.com",
        "role": "QA Tester",
        "social": [
            ("LinkedIn", "www.linkedin.com/in/marianne-salvador-908010387"),
            ("Facebook", "https://www.facebook.com/marianne.cosmos8267"),
        ],
        "contributions": [
            "Designed the project logo.",
            'Implemented "About Us" features.',
            "Assisted in testing and debugging.",
            "Prepared project documentation.",
        ],
    },
    {
        "name": "Sy Gian Daniel S.",
        "email": "Giansy0919@gmail.com",
        "role": "Backend Developer",
        "social": [],
        "contributions": [
            "Implemented system features and different vehicle types.",
            "Assisted in testing and debugging.",
        ],
    },
    {
        "name": "Cliff Bradley Sanchez",
        "email": "cliffbradley730@gmail.com",
        "role": "Backend Developer",
        "social": [],
        "contributions": [
            "Developed core booking features.",
            "Designed a feature to view all bookings in the program using Tkinter.",
            "Designed a cancel booking feature using Tkinter.",
        ],
    },
    {
        "name": "Anika Sophia C. Basa",
        "email": "anikasophia.cabigbasa@gmail.com",
        "role": "UI/UX Designer",
        "social": [],
        "contributions": [
            "Designed the overall user interface and user experience of the Ride Booking System.",
            "Co-developed the graphical user interface (GUI) using Tkinter.",
            "Assisted in testing and refining the user interface to ensure a smooth user experience.",
        ],
    },
    {
        "name": "Rexchelle Ann T. Imperial",
        "email": "rexchelleanncet@gmail.com",
        "role": "UI/UX Designer",
        "social": [],
        "contributions": [
            "Designed a logo for the Ride Booking System.",
            "Created the name and the tagline for the Ride Booking System.",
            "Co-developed the graphical user interface (GUI) using Tkinter.",
        ],
    },
    {
        "name": "Cristian M. Talidong",
        "email": "cristiantalidong06@gmail.com",
        "role": "Backend Developer",
        "social": [],
        "contributions": [
            "Developed the JSON-based file uploading system for ride records.",
            "Implemented file handling functions to save and load ride data.",
        ],
    },
    {
        "name": "Arshe Jay N. Cabildo",
        "email": "cabildo.arshejay.norte@gmail.com",
        "role": "UI/UX Designer and Backend Developer",
        "social": [
            ("Facebook", "https://www.facebook.com/profile.php?id=100021747714241"),
        ],
        "contributions": [
            "Fixed bugs within the system.",
            "Added features to the application.",
            "Co-developed the core application modules.",
        ],
    },
    {
        "name": "Suzanne Sharrie N. Luzano",
        "email": "shaneluzano53@gmail.com",
        "role": "Project Manager / QA Tester",
        "social": [
            ("LinkedIn", "https://www.linkedin.com/in/suzanne-luzano/"),
        ],
        "contributions": [
            "Led the planning of the project.",
            "Established the workflow and structure of the project.",
            "Assisted in testing and documentation.",
        ],
    },
    {
        "name": "Stephanie Rose F. Garcia",
        "email": "stephyrose172@gmail.com",
        "role": "QA Tester",
        "social": [],
        "contributions": [
            "Assisted in testing the application.",
            "Prepared project documentation.",
        ],
    },
]


def _render_credits(body):
    """Render the Project Credits section into the given scrollable body."""
    _section_label(body, "Project Credits")

    for person in PROJECT_CREDITS:
        card = _card(body)

        tk.Label(card, text=person["name"], font=("Helvetica", 13, "bold"),
                 bg=C_WHITE, fg=C_TEXT, anchor="w").pack(fill="x")
        tk.Label(card, text=person["role"], font=("Helvetica", 10, "bold"),
                 bg=C_WHITE, fg=C_ACCENT, anchor="w").pack(fill="x", pady=(0, 4))
        tk.Label(card, text=f"✉  {person['email']}", font=("Helvetica", 9),
                 bg=C_WHITE, fg=C_SUBTEXT, anchor="w").pack(fill="x")

        for label, link in person["social"]:
            tk.Label(card, text=f"🔗 {label}: {link}", font=("Helvetica", 9),
                     bg=C_WHITE, fg=C_SUBTEXT, anchor="w",
                     wraplength=300, justify="left").pack(fill="x")

        tk.Label(card, text="Contributions:", font=("Helvetica", 9, "bold"),
                 bg=C_WHITE, fg=C_TEXT, anchor="w").pack(fill="x", pady=(6, 0))
        for item in person["contributions"]:
            tk.Label(card, text=f"•  {item}", font=("Helvetica", 9),
                     bg=C_WHITE, fg=C_SUBTEXT, anchor="w",
                     wraplength=300, justify="left").pack(fill="x")

# ─────────────────────────────────────────────
#  SHARED UI PRIMITIVES
# ─────────────────────────────────────────────

def _pill_btn(parent, text, cmd, bg=C_ACCENT, fg=C_WHITE, pady=13):
    tk.Button(parent, text=text, font=("Helvetica", 13, "bold"),
              bg=bg, fg=fg, bd=0, pady=pady, cursor="hand2",
              relief="flat", activebackground=C_PURPLE_MID,
              activeforeground=C_WHITE,
              command=cmd).pack(fill="x", padx=20, pady=(6, 0))


def _section_label(parent, text):
    tk.Label(parent, text=text, font=("Helvetica", 13, "bold"),
             bg=C_BG, fg=C_TEXT, anchor="w").pack(
             fill="x", padx=20, pady=(18, 6))


def _card(parent, **kw):
    """White rounded-look card frame."""
    f = tk.Frame(parent, bg=C_WHITE, padx=16, pady=14, **kw)
    f.pack(fill="x", padx=16, pady=6)
    return f


def _divider(parent):
    tk.Frame(parent, bg="#E5E7EB", height=1).pack(fill="x", padx=16)


# ── Bottom nav bar ────────────────────────────
def _nav(parent, active, app):
    """
    3-tab bottom nav: Home · Settings · Info
    active = "home" | "settings" | "info"
    """
    bar = tk.Frame(parent, bg=C_WHITE, pady=0)
    bar.pack(side="bottom", fill="x")
    tk.Frame(bar, bg="#E5E7EB", height=1).pack(fill="x")

    tabs = [
        ("🏠", "Home",     "home",     app.show_user_home),
        ("⚙️",  "Settings", "settings", app.show_user_settings),
        ("ℹ️",  "Info",     "info",     app.show_user_info),
    ]
    inner = tk.Frame(bar, bg=C_WHITE)
    inner.pack(fill="x")
    for icon, label, key, cmd in tabs:
        col = tk.Frame(inner, bg=C_WHITE, pady=8, cursor="hand2")
        col.pack(side="left", fill="both", expand=True)
        clr = C_ACCENT if key == active else C_SUBTEXT
        icon_lbl = tk.Label(col, text=icon, font=("Helvetica", 18),
                             bg=C_WHITE, fg=clr, cursor="hand2")
        icon_lbl.pack()
        text_lbl = tk.Label(col, text=label, font=("Helvetica", 9),
                             bg=C_WHITE, fg=clr, cursor="hand2")
        text_lbl.pack()
        for w in (col, icon_lbl, text_lbl):
            w.bind("<Button-1>", lambda e, c=cmd: c())


def _rider_nav(parent, active, app):
    """3-tab nav for rider: Jobs · Settings · Info"""
    bar = tk.Frame(parent, bg=C_WHITE, pady=0)
    bar.pack(side="bottom", fill="x")
    tk.Frame(bar, bg="#E5E7EB", height=1).pack(fill="x")

    tabs = [
        ("🚖", "Jobs",     "jobs",     app.show_rider_home),
        ("⚙️",  "Settings", "settings", app.show_rider_settings),
        ("ℹ️",  "Info",     "info",     app.show_rider_info),
    ]
    inner = tk.Frame(bar, bg=C_WHITE)
    inner.pack(fill="x")
    for icon, label, key, cmd in tabs:
        col = tk.Frame(inner, bg=C_WHITE, pady=8, cursor="hand2")
        col.pack(side="left", fill="both", expand=True)
        clr = C_ACCENT if key == active else C_SUBTEXT
        icon_lbl = tk.Label(col, text=icon, font=("Helvetica", 18),
                             bg=C_WHITE, fg=clr, cursor="hand2")
        icon_lbl.pack()
        text_lbl = tk.Label(col, text=label, font=("Helvetica", 9),
                             bg=C_WHITE, fg=clr, cursor="hand2")
        text_lbl.pack()
        for w in (col, icon_lbl, text_lbl):
            w.bind("<Button-1>", lambda e, c=cmd: c())


# ── Purple gradient header ─────────────────────
def _header(parent, title, subtitle=None, back_cmd=None, show_avatar=False, avatar_letter="U"):
    hdr = tk.Frame(parent, bg=C_PURPLE_DARK, padx=20, pady=20)
    hdr.pack(fill="x")

    if back_cmd:
        tk.Button(hdr, text="←", font=("Helvetica", 16),
                  bg=C_PURPLE_DARK, fg=C_WHITE, bd=0,
                  activebackground=C_PURPLE_DARK,
                  cursor="hand2", command=back_cmd).pack(anchor="w")

    row = tk.Frame(hdr, bg=C_PURPLE_DARK)
    row.pack(fill="x")

    left = tk.Frame(row, bg=C_PURPLE_DARK)
    left.pack(side="left", fill="both", expand=True)

    tk.Label(left, text=title, font=("Helvetica", 22, "bold"),
             bg=C_PURPLE_DARK, fg=C_WHITE, anchor="w").pack(fill="x")
    if subtitle:
        tk.Label(left, text=subtitle, font=("Helvetica", 11),
                 bg=C_PURPLE_DARK, fg="#C4B5FD", anchor="w").pack(fill="x")

    if show_avatar:
        av = tk.Canvas(row, width=44, height=44,
                       bg=C_PURPLE_DARK, highlightthickness=0)
        av.pack(side="right")
        av.create_oval(2, 2, 42, 42, fill=C_PURPLE_MID, outline=C_WHITE, width=2)
        av.create_text(22, 22, text=avatar_letter,
                       font=("Helvetica", 16, "bold"), fill=C_WHITE)


# ── App logo strip ─────────────────────────────
def _logo_strip(parent):
    strip = tk.Frame(parent, bg=C_PURPLE_DARK, padx=20, pady=12)
    strip.pack(fill="x")
    row = tk.Frame(strip, bg=C_PURPLE_DARK)
    row.pack(anchor="w")

    cv = tk.Canvas(row, width=36, height=36,
                   bg=C_PURPLE_DARK, highlightthickness=0)
    cv.pack(side="left")
    cv.create_oval(2, 2, 34, 34, fill=C_WHITE, outline="")
    cv.create_text(18, 18, text="H", font=("Helvetica", 14, "bold"), fill=C_ACCENT)

    tx = tk.Frame(row, bg=C_PURPLE_DARK, padx=8)
    tx.pack(side="left")
    tk.Label(tx, text="HARUUROT!", font=("Helvetica", 13, "bold"),
             bg=C_PURPLE_DARK, fg=C_WHITE).pack(anchor="w")
    tk.Label(tx, text="Ride Fast. Ride Safe. Ride Haruurot!",
             font=("Helvetica", 9), bg=C_PURPLE_DARK, fg="#C4B5FD").pack(anchor="w")


# ── Menu action card ───────────────────────────
def _menu_action_card(parent, icon, icon_bg, title, desc, cmd):
    card = tk.Frame(parent, bg=C_WHITE, cursor="hand2")
    card.pack(fill="x", padx=16, pady=8)

    # left colour accent bar
    tk.Frame(card, bg=C_ACCENT, width=4).pack(side="left", fill="y")

    row = tk.Frame(card, bg=C_WHITE, padx=14, pady=16)
    row.pack(side="left", fill="both", expand=True)

    ib = tk.Frame(row, bg=icon_bg, width=52, height=52)
    ib.pack(side="left", padx=(0, 14))
    ib.pack_propagate(False)
    tk.Label(ib, text=icon, font=("Helvetica", 22),
             bg=icon_bg).place(relx=.5, rely=.5, anchor="center")

    tx = tk.Frame(row, bg=C_WHITE)
    tx.pack(side="left", fill="both", expand=True)
    tk.Label(tx, text=title, font=("Helvetica", 13, "bold"),
             bg=C_WHITE, fg=C_TEXT, anchor="w").pack(fill="x")
    tk.Label(tx, text=desc, font=("Helvetica", 10),
             bg=C_WHITE, fg=C_SUBTEXT, wraplength=190,
             justify="left", anchor="w").pack(fill="x")

    tk.Label(row, text="›", font=("Helvetica", 22),
             bg=C_WHITE, fg=C_ACCENT).pack(side="right")

    def _bind(w):
        w.bind("<Button-1>", lambda e: cmd())
        for ch in w.winfo_children():
            _bind(ch)
    _bind(card)


# ─────────────────────────────────────────────
#  USER HOME  (dashboard with 2 menu cards)
# ─────────────────────────────────────────────

# ══════════════════════════════════════════════
#  USER HOME SCREEN (FIXED: NO SCROLLBARS)
# ══════════════════════════════════════════════

def build_user_home(app):
    frm  = app.clear()
    frm.configure(bg=C_BG)
    user = app.current_user or {}
    name = user.get("full_name", "User")
    first_name = name.split()[0] if name else "User"
    avatar = name[0].upper() if name else "U"

    _logo_strip(frm)
    _header(frm,
            title=f"Good Day,\n{name}",
            show_avatar=True, avatar_letter=avatar)

    _nav(frm, "home", app)

    body = tk.Frame(frm, bg=C_BG)
    body.pack(fill="both", expand=True)

    tk.Frame(body, bg=C_BG, height=6).pack()

    _menu_action_card(body, "🚕", "#EDE9FE",
                      "Book a Ride",
                      "Book a ride to your destination",
                      app.show_book_ride)

    _menu_action_card(body, "📋", "#EDE9FE",
                      "View Bookings",
                      "View your past and upcoming bookings",
                      app.show_view_bookings)

    tk.Frame(body, bg=C_BG, height=16).pack()
# ─────────────────────────────────────────────
#  BOOK A RIDE SCREEN
# ─────────────────────────────────────────────


def build_book_ride(app):
    frm = app.clear()
    frm.configure(bg=C_BG)

    _header(frm, title="Book a Ride",
            subtitle="Fill in your trip details",
            back_cmd=app.show_user_home)
    _nav(frm, "home", app)

    body = tk.Frame(frm, bg=C_BG)
    body.pack(fill="both", expand=True)
    pad = tk.Frame(body, bg=C_BG, padx=16)
    pad.pack(fill="x", pady=12)

    # Vehicle selector
    tk.Label(pad, text="Vehicle Type", font=("Helvetica", 11, "bold"),
             bg=C_BG, fg=C_TEXT, anchor="w").pack(fill="x", pady=(0, 6))

    vrow = tk.Frame(pad, bg=C_BG)
    vrow.pack(fill="x", pady=(0, 12))

    # Track buttons so we can update their colours in-place
    _vtab_btns = {}

    def _select_vehicle(label):
        app._selected_vehicle = label
        for lbl, btn in _vtab_btns.items():
            if lbl == label:
                btn.config(bg=C_ACCENT, fg=C_WHITE)
            else:
                btn.config(bg=C_WHITE, fg=C_SUBTEXT)

    # Restore previous selection across redraws (default Car)
    current_vehicle = getattr(app, "_selected_vehicle", "Car")

    def _vtab(label, icon):
        selected = label == current_vehicle
        bg_ = C_ACCENT if selected else C_WHITE
        fg_ = C_WHITE  if selected else C_SUBTEXT
        btn = tk.Button(vrow, text=f"{icon}\n{label}",
                        font=("Helvetica", 10, "bold"),
                        bg=bg_, fg=fg_, bd=0, pady=10,
                        cursor="hand2", relief="flat",
                        width=7,
                        command=lambda l=label: _select_vehicle(l))
        btn.pack(side="left", expand=True, padx=4)
        _vtab_btns[label] = btn

    _vtab("Car",        "🚗")
    _vtab("Van",        "🚐")
    _vtab("Motorcycle", "🛵")

    card = tk.Frame(pad, bg=C_WHITE, padx=14, pady=14)
    card.pack(fill="x")

    _, ent_start = field(card, "Pickup Location", "Enter start address")
    _, ent_end   = field(card, "Dropoff Location", "Enter destination address")
    _, ent_dist  = field(card, "Distance (km)", "e.g. 5.5")

    # Fare preview
    fare_var = tk.StringVar(value="Estimated fare: —")
    fare_lbl = tk.Label(pad, textvariable=fare_var,
                        font=("Helvetica", 12, "bold"),
                        bg=C_BG, fg=C_ACCENT, anchor="w")
    fare_lbl.pack(fill="x", pady=(10, 2))

    def _preview_fare(e=None):
        try:
            d = float(ent_dist.get().strip())
            from vehicle import get_vehicle
            v   = get_vehicle(getattr(app, "_selected_vehicle", "Car"))
            est = round(v.calculate_cost(d), 2)
            fare_var.set(f"Estimated fare: {PHP}{est:,.2f}")
        except Exception:
            fare_var.set("Estimated fare: —")

    ent_dist.bind("<KeyRelease>", _preview_fare)

    def submit_booking():
        start_loc = ent_start.get().strip()
        end_loc   = ent_end.get().strip()
        if not start_loc or start_loc == "Enter start address" \
                or not end_loc or end_loc == "Enter destination address":
            messagebox.showerror("Error", "All routing fields are mandatory.")
            return
        try:
            distance = float(ent_dist.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid distance number.")
            return
        try:
            booking = create_booking(
                app.current_user["username"],
                getattr(app, "_selected_vehicle", "Car"), start_loc, end_loc, distance)
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))
            return
        messagebox.showinfo("Booking Confirmed",
                            f"Trip requested!\nFare: {PHP}{booking['total_cost']:,.2f}")
        app._selected_vehicle = "Car"   # reset for next booking
        app.show_user_home()

    tk.Frame(pad, bg=C_BG, height=4).pack()
    _pill_btn(pad, "Confirm Booking", submit_booking)
    tk.Frame(body, bg=C_BG, height=16).pack()

# ─────────────────────────────────────────────
#  VIEW BOOKINGS SCREEN
# ─────────────────────────────────────────────

def build_view_bookings(app):
    frm = app.clear()
    frm.configure(bg=C_BG)

    _header(frm, title="My Bookings",
            subtitle="Your trip history",
            back_cmd=app.show_user_home)
    _nav(frm, "home", app)

    _, _, body = scrollable(frm)
    tk.Frame(body, bg=C_BG, height=6).pack()

    user_bookings = get_user_bookings(app.current_user["username"])

    if not user_bookings:
        tk.Label(body, text="✈️", font=("Helvetica", 40),
                 bg=C_BG).pack(pady=(60, 10))
        tk.Label(body, text="No trips yet",
                 font=("Helvetica", 15, "bold"), bg=C_BG, fg=C_TEXT).pack()
        tk.Label(body, text="Book your first ride to get started.",
                 font=("Helvetica", 11), bg=C_BG, fg=C_SUBTEXT).pack()
    else:
        status_colors = {
            "Pending":   "#FEF3C7",
            "Assigned":  "#DCFCE7",
            "Completed": "#DBEAFE",
            "Cancelled": "#F3F4F6",
        }
        status_text = {
            "Pending":   "#92400E",
            "Assigned":  "#166534",
            "Completed": "#1D4ED8",
            "Cancelled": "#6B7280",
        }
        for b in reversed(user_bookings):
            card = tk.Frame(body, bg=C_WHITE)
            card.pack(fill="x", padx=16, pady=6)

            # top row: ID + status badge
            top = tk.Frame(card, bg=C_WHITE, padx=14, pady=10)
            top.pack(fill="x")
            tk.Label(top, text=f"#{b['booking_id'].upper()}",
                     font=("Helvetica", 11, "bold"),
                     bg=C_WHITE, fg=C_TEXT).pack(side="left")
            st = b["status"]
            badge_bg = status_colors.get(st, "#F3F4F6")
            badge_fg = status_text.get(st, C_TEXT)
            tk.Label(top, text=f"  {st}  ",
                     font=("Helvetica", 9, "bold"),
                     bg=badge_bg, fg=badge_fg).pack(side="right")

            _divider(card)

            # details
            det = tk.Frame(card, bg=C_WHITE, padx=14, pady=10)
            det.pack(fill="x")

            def _row(p, icon, text):
                r = tk.Frame(p, bg=C_WHITE)
                r.pack(fill="x", pady=2)
                tk.Label(r, text=icon, font=("Helvetica", 11),
                         bg=C_WHITE, fg=C_ACCENT, width=2).pack(side="left")
                tk.Label(r, text=text, font=("Helvetica", 10),
                         bg=C_WHITE, fg=C_TEXT, anchor="w",
                         wraplength=270, justify="left").pack(side="left", fill="x")

            _row(det, "📍", f"{b['start']}")
            _row(det, "🏁", f"{b['end']}")
            _row(det, "🚗", f"{b['vehicle_type']}  •  {b['distance']} km")
            _row(det, "💰", f"{PHP}{float(b['total_cost']):,.2f}")
            if b.get("assigned_rider") and b["assigned_rider"] != "None":
                _row(det, "👤", f"Rider: {b['assigned_rider']}")

            if b["status"] == "Pending":
                def cancel(bid=b["booking_id"]):
                    if messagebox.askyesno("Cancel Booking",
                                            "Are you sure you want to cancel this booking?"):
                        if cancel_booking(bid, app.current_user["username"]):
                            messagebox.showinfo("Cancelled", "Booking has been cancelled.")
                            app.show_view_bookings()
                        else:
                            messagebox.showerror("Error", "Unable to cancel this booking.")

                cancel_row = tk.Frame(card, bg=C_WHITE, padx=14, pady=0)
                cancel_row.pack(fill="x", pady=(0, 12))
                tk.Button(cancel_row, text="Cancel Booking",
                          font=("Helvetica", 10, "bold"),
                          bg="#FEE2E2", fg=C_RED, bd=0, pady=8,
                          cursor="hand2", relief="flat",
                          command=cancel).pack(fill="x")

    tk.Frame(body, bg=C_BG, height=16).pack()


# ─────────────────────────────────────────────
#  USER SETTINGS
# ─────────────────────────────────────────────

def build_user_settings(app):
    frm = app.clear()
    frm.configure(bg=C_BG)
    user = app.current_user or {}
    name = user.get("full_name", "User")

    _header(frm, title="Settings", subtitle="Manage your account")
    _nav(frm, "settings", app)

    _, _, body = scrollable(frm)

    # Profile avatar
    av_frm = tk.Frame(body, bg=C_BG)
    av_frm.pack(pady=20)
    cv = tk.Canvas(av_frm, width=72, height=72, bg=C_BG, highlightthickness=0)
    cv.pack()
    cv.create_oval(2, 2, 70, 70, fill=C_ACCENT, outline="")
    cv.create_text(36, 36, text=(name[0].upper() if name else "U"),
                   font=("Helvetica", 26, "bold"), fill=C_WHITE)
    tk.Label(av_frm, text=name, font=("Helvetica", 14, "bold"),
             bg=C_BG, fg=C_TEXT).pack(pady=(8, 2))
    tk.Label(av_frm, text=user.get("email", ""),
             font=("Helvetica", 10), bg=C_BG, fg=C_SUBTEXT).pack()

    _section_label(body, "Account Information")

    card = _card(body)

    def _info_row(parent, label, value):
        r = tk.Frame(parent, bg=C_WHITE, pady=6)
        r.pack(fill="x")
        tk.Label(r, text=label, font=("Helvetica", 10),
                 bg=C_WHITE, fg=C_SUBTEXT, width=14, anchor="w").pack(side="left")
        tk.Label(r, text=value, font=("Helvetica", 10, "bold"),
                 bg=C_WHITE, fg=C_TEXT, anchor="w").pack(side="left", fill="x", expand=True)
        tk.Frame(parent, bg="#F3F4F6", height=1).pack(fill="x")

    _info_row(card, "Username",  user.get("username", "—"))
    _info_row(card, "Full Name", user.get("full_name", "—"))
    _info_row(card, "Payment",   user.get("payment_method", "Cash"))

    _section_label(body, "Edit Account")

    edit_card = _card(body)

    _, u_ent  = field(edit_card, "New Username",  user.get("username", ""))
    _, n_ent  = field(edit_card, "New Full Name", user.get("full_name", ""))
    _, pm_ent = field(edit_card, "Payment Method", user.get("payment_method", "Cash"))
    _, p_ent  = field(edit_card, "New Password (leave blank to keep)", "", password=True)

    status_var = tk.StringVar()
    tk.Label(edit_card, textvariable=status_var,
             font=("Helvetica", 10), bg=C_WHITE,
             fg=C_GREEN, anchor="w").pack(fill="x", pady=(4, 0))

    def save_changes():
        new_u  = u_ent.get().strip()
        new_n  = n_ent.get().strip()
        new_pm = pm_ent.get().strip()
        new_p  = p_ent.get().strip()

        if not new_u:
            messagebox.showerror("Error", "Username cannot be empty."); return
        if not new_n:
            messagebox.showerror("Error", "Full name cannot be empty."); return

        users = load(USERS_FILE)
        for u in users:
            if u["username"] == app.current_user["username"]:
                # check username taken by someone else
                if new_u != u["username"]:
                    if any(x["username"] == new_u for x in users if x is not u):
                        messagebox.showerror("Error", "Username already taken."); return
                u["username"]       = new_u
                u["full_name"]      = new_n
                u["payment_method"] = new_pm if new_pm else "Cash"
                if new_p:
                    u["password"]   = hash_pw(new_p)
                app.current_user = u
                break
        save(USERS_FILE, users)
        status_var.set("✓ Changes saved successfully!")

    _pill_btn(edit_card, "Save Changes", save_changes, pady=11)

    # Logout
    tk.Frame(body, bg=C_BG, height=8).pack()
    tk.Button(body, text="Logout",
              font=("Helvetica", 13, "bold"),
              bg="#FEE2E2", fg=C_RED,
              bd=0, pady=13, cursor="hand2", relief="flat",
              command=app.show_splash).pack(fill="x", padx=16)
    tk.Frame(body, bg=C_BG, height=16).pack()


# ─────────────────────────────────────────────
#  USER INFO / ABOUT
# ─────────────────────────────────────────────

def build_user_info(app):
    frm = app.clear()
    frm.configure(bg=C_BG)

    _header(frm, title="About", subtitle="HARUUROT Ride Booking")
    _nav(frm, "info", app)

    _, _, body = scrollable(frm)
    tk.Frame(body, bg=C_BG, height=20).pack()

    cv = tk.Canvas(body, width=80, height=80, bg=C_BG, highlightthickness=0)
    cv.pack()
    cv.create_oval(2, 2, 78, 78, fill=C_ACCENT, outline="")
    cv.create_text(40, 40, text="H", font=("Helvetica", 30, "bold"), fill=C_WHITE)

    tk.Label(body, text="HARUUROT", font=("Helvetica", 18, "bold"),
             bg=C_BG, fg=C_TEXT).pack(pady=(10, 2))
    tk.Label(body, text="Ride Fast. Ride Safe. Ride Haruurot!",
             font=("Helvetica", 11), bg=C_BG, fg=C_SUBTEXT).pack()

    tk.Frame(body, bg=C_BG, height=20).pack()

    infos = [
        ("Team",      "BSCpE 1-3 Group 4"),
        ("Version",   "1.0.0"),
        ("Platform",  "Desktop (Tkinter)"),
        ("Currency",  "Philippine Peso (PHP ₱)"),
        ("Support",   "support@haruurot.ph"),
    ]
    card = _card(body)
    for label, val in infos:
        r = tk.Frame(card, bg=C_WHITE, pady=8)
        r.pack(fill="x")
        tk.Label(r, text=label, font=("Helvetica", 10),
                 bg=C_WHITE, fg=C_SUBTEXT, width=12, anchor="w").pack(side="left")
        tk.Label(r, text=val, font=("Helvetica", 10, "bold"),
                 bg=C_WHITE, fg=C_TEXT, anchor="w").pack(side="left")
        tk.Frame(card, bg="#F3F4F6", height=1).pack(fill="x")

    _render_credits(body)

    tk.Frame(body, bg=C_BG, height=16).pack()


# ─────────────────────────────────────────────
#  RIDER HOME
# ─────────────────────────────────────────────

def build_rider_home(app):
    frm   = app.clear()
    frm.configure(bg=C_PURPLE_DARK)
    user  = app.current_user or {}
    name  = user.get("full_name", "Rider")
    vtype = user.get("vehicle_type", "Car")
    is_available = user.get("available", True)

    _logo_strip(frm)

    hdr = tk.Frame(frm, bg=C_PURPLE_DARK, padx=20, pady=4)
    hdr.pack(fill="x")
    row = tk.Frame(hdr, bg=C_PURPLE_DARK)
    row.pack(fill="x")

    left = tk.Frame(row, bg=C_PURPLE_DARK)
    left.pack(side="left", fill="both", expand=True)
    tk.Label(left, text="Good Day,", font=("Helvetica", 16),
             bg=C_PURPLE_DARK, fg=C_WHITE, anchor="w").pack(fill="x")
    tk.Label(left, text=name, font=("Helvetica", 22, "bold"),
             bg=C_PURPLE_DARK, fg=C_WHITE, anchor="w").pack(fill="x")

    status_color = C_GREEN if is_available else C_SUBTEXT
    status_text  = "Available" if is_available else "Offline"
    st_row = tk.Frame(left, bg=C_PURPLE_DARK)
    st_row.pack(fill="x", pady=(4, 0), anchor="w")
    tk.Label(st_row, text="Status: ", font=("Helvetica", 12),
             bg=C_PURPLE_DARK, fg="#C4B5FD").pack(side="left")
    tk.Label(st_row, text=status_text, font=("Helvetica", 12, "bold"),
             bg=C_PURPLE_DARK, fg=status_color).pack(side="left")

    av = tk.Canvas(row, width=46, height=46,
                   bg=C_PURPLE_DARK, highlightthickness=0)
    av.pack(side="right")
    av.create_oval(2, 2, 44, 44, fill=C_PURPLE_MID, outline=C_WHITE, width=2)
    av.create_text(23, 23, text="👤", font=("Helvetica", 16), fill=C_WHITE)

    tk.Frame(frm, bg=C_PURPLE_DARK, height=20).pack(fill="x")

    body_outer = tk.Frame(frm, bg=C_PURPLE_DARK)
    body_outer.pack(fill="both", expand=True)

    _rider_nav(frm, "jobs", app)

    body = tk.Frame(body_outer, bg=C_PURPLE_DARK)
    body.pack(fill="both", expand=True)

    pending_count = len(get_pending_bookings_for_vehicle(vtype))
    assigned_count = len(get_rider_bookings(app.current_user["username"]))

    def _dash_card(parent, icon, icon_bg, title, desc, cmd, badge=None):
        card = tk.Frame(parent, bg=C_WHITE, cursor="hand2")
        card.pack(fill="x", padx=16, pady=8)

        row = tk.Frame(card, bg=C_WHITE, padx=16, pady=18)
        row.pack(fill="x")

        ib = tk.Frame(row, bg=icon_bg, width=52, height=52)
        ib.pack(side="left", padx=(0, 14))
        ib.pack_propagate(False)
        tk.Label(ib, text=icon, font=("Helvetica", 22),
                 bg=icon_bg).place(relx=.5, rely=.5, anchor="center")

        tx = tk.Frame(row, bg=C_WHITE)
        tx.pack(side="left", fill="both", expand=True)

        title_row = tk.Frame(tx, bg=C_WHITE)
        title_row.pack(fill="x", anchor="w")
        tk.Label(title_row, text=title, font=("Helvetica", 14, "bold"),
                 bg=C_WHITE, fg=C_TEXT, anchor="w").pack(side="left")
        if badge:
            tk.Label(title_row, text=f"  {badge}  ", font=("Helvetica", 9, "bold"),
                     bg="#DCFCE7", fg="#166534").pack(side="left", padx=(8, 0))

        tk.Label(tx, text=desc, font=("Helvetica", 10),
                 bg=C_WHITE, fg=C_SUBTEXT, wraplength=200,
                 justify="left", anchor="w").pack(fill="x")

        tk.Label(row, text="›", font=("Helvetica", 22),
                 bg=C_WHITE, fg=C_ACCENT).pack(side="right")

        def _bind(w):
            w.bind("<Button-1>", lambda e: cmd())
            for ch in w.winfo_children():
                _bind(ch)
        _bind(card)

    tk.Frame(body, bg=C_PURPLE_DARK, height=4).pack()

    _dash_card(body, "🚖", "#EDE9FE", "Accept Booking",
               "View and accept incoming bookings", app.show_rider_jobs,
               badge=str(pending_count) if pending_count else None)

    _dash_card(body, "📄", "#EDE9FE", "View Assigned Bookings",
               "View your past and upcoming bookings", app.show_rider_assigned,
               badge=str(assigned_count) if assigned_count else None)

    _dash_card(body, "👤", "#EDE9FE", "Update Availability",
               "Go offline or update your availability status",
               app.show_rider_availability)

    tk.Frame(body, bg=C_PURPLE_DARK, height=16).pack()


# ─────────────────────────────────────────────
#  RIDER: ACCEPT BOOKING (job list)
# ─────────────────────────────────────────────

def build_rider_jobs(app):
    frm = app.clear()
    frm.configure(bg=C_BG)
    user  = app.current_user or {}
    vtype = user.get("vehicle_type", "Car")
    is_available = user.get("available", True)

    _header(frm, title="Accept Booking",
            subtitle="View and accept incoming bookings",
            back_cmd=app.show_rider_home)
    _rider_nav(frm, "jobs", app)

    if not is_available:
        body = tk.Frame(frm, bg=C_BG)
        body.pack(fill="both", expand=True, pady=40)

        tk.Label(body, text="⚫", font=("Helvetica", 48), bg=C_BG).pack(pady=(0, 10))
        tk.Label(body, text="You're Offline", font=("Helvetica", 16, "bold"),
                 bg=C_BG, fg=C_TEXT).pack()
        tk.Label(body, text="Go online to view and accept incoming bookings.",
                 font=("Helvetica", 11), bg=C_BG, fg=C_SUBTEXT,
                 wraplength=300, justify="center").pack(pady=(4, 20))

        tk.Button(body, text="Go Available", font=("Helvetica", 13, "bold"),
                  bg="#DCFCE7", fg="#166534", bd=0, pady=14,
                  cursor="hand2", relief="flat",
                  command=app.show_rider_availability).pack(fill="x", padx=20)
        return

    _, _, body = scrollable(frm)
    tk.Frame(body, bg=C_BG, height=6).pack()

    active = get_pending_bookings_for_vehicle(vtype)
    if not active:
        tk.Label(body, text="🚦", font=("Helvetica", 36), bg=C_BG).pack(pady=(40, 6))
        tk.Label(body, text="No active requests",
                 font=("Helvetica", 13, "bold"), bg=C_BG, fg=C_TEXT).pack()
        tk.Label(body, text="Check back soon for new jobs.",
                 font=("Helvetica", 10), bg=C_BG, fg=C_SUBTEXT).pack()
    else:
        for b in active:
            card = tk.Frame(body, bg=C_WHITE)
            card.pack(fill="x", padx=16, pady=6)

            top = tk.Frame(card, bg=C_WHITE, padx=14, pady=10)
            top.pack(fill="x")
            tk.Label(top, text=f"#{b['booking_id'].upper()}",
                     font=("Helvetica", 11, "bold"),
                     bg=C_WHITE, fg=C_TEXT).pack(side="left")
            tk.Label(top, text=f"  {PHP}{float(b['total_cost']):,.2f}  ",
                     font=("Helvetica", 11, "bold"),
                     bg="#DCFCE7", fg="#166534").pack(side="right")

            _divider(card)

            det = tk.Frame(card, bg=C_WHITE, padx=14, pady=10)
            det.pack(fill="x")

            def _row(p, icon, text):
                r = tk.Frame(p, bg=C_WHITE)
                r.pack(fill="x", pady=2)
                tk.Label(r, text=icon, font=("Helvetica", 11),
                         bg=C_WHITE, fg=C_ACCENT, width=2).pack(side="left")
                tk.Label(r, text=text, font=("Helvetica", 10),
                         bg=C_WHITE, fg=C_TEXT, anchor="w",
                         wraplength=270, justify="left").pack(side="left", fill="x")

            _row(det, "📍", b["start"])
            _row(det, "🏁", b["end"])
            _row(det, "📏", f"{b['distance']} km")

            btn_row = tk.Frame(card, bg=C_WHITE, padx=14, pady=0)
            btn_row.pack(fill="x", pady=(0, 12))

            def accept_job(bid=b["booking_id"]):
                if assign_booking(bid, app.current_user["username"]):
                    messagebox.showinfo("Accepted", "You have claimed this trip!")
                    app.show_rider_jobs()
                else:
                    messagebox.showerror("Error", "This job is no longer available.")
                    app.show_rider_jobs()

            tk.Button(btn_row, text="Accept Job",
                      font=("Helvetica", 11, "bold"),
                      bg=C_TEAL, fg=C_WHITE, bd=0, pady=9,
                      cursor="hand2", relief="flat",
                      command=accept_job).pack(fill="x")

    tk.Frame(body, bg=C_BG, height=16).pack()


# ─────────────────────────────────────────────
#  RIDER: VIEW ASSIGNED BOOKINGS
# ─────────────────────────────────────────────

def build_rider_assigned(app):
    frm = app.clear()
    frm.configure(bg=C_BG)

    _header(frm, title="Assigned Bookings",
            subtitle="Your past and upcoming bookings",
            back_cmd=app.show_rider_home)
    _rider_nav(frm, "jobs", app)

    _, _, body = scrollable(frm)
    tk.Frame(body, bg=C_BG, height=6).pack()

    my_jobs = get_rider_bookings(app.current_user["username"])
    if not my_jobs:
        tk.Label(body, text="📄", font=("Helvetica", 36), bg=C_BG).pack(pady=(40, 6))
        tk.Label(body, text="No claimed jobs yet",
                 font=("Helvetica", 13, "bold"), bg=C_BG, fg=C_TEXT).pack()
        tk.Label(body, text="Accepted bookings will appear here.",
                 font=("Helvetica", 10), bg=C_BG, fg=C_SUBTEXT).pack()
    else:
        for b in reversed(my_jobs):
            card = tk.Frame(body, bg=C_WHITE)
            card.pack(fill="x", padx=16, pady=6)

            top = tk.Frame(card, bg=C_WHITE, padx=14, pady=10)
            top.pack(fill="x")
            tk.Label(top, text=f"#{b['booking_id'].upper()}",
                     font=("Helvetica", 11, "bold"),
                     bg=C_WHITE, fg=C_TEXT).pack(side="left")

            _badge_colors = {
                "Assigned":  ("#DCFCE7", "#166534"),
                "Completed": ("#DBEAFE", "#1D4ED8"),
            }
            badge_bg, badge_fg = _badge_colors.get(b["status"], ("#F3F4F6", C_TEXT))
            tk.Label(top, text=f"  {b['status']}  ",
                     font=("Helvetica", 9, "bold"),
                     bg=badge_bg, fg=badge_fg).pack(side="right")

            _divider(card)

            det = tk.Frame(card, bg=C_WHITE, padx=14, pady=10)
            det.pack(fill="x")

            def _row(p, icon, text):
                r = tk.Frame(p, bg=C_WHITE)
                r.pack(fill="x", pady=2)
                tk.Label(r, text=icon, font=("Helvetica", 11),
                         bg=C_WHITE, fg=C_ACCENT, width=2).pack(side="left")
                tk.Label(r, text=text, font=("Helvetica", 10),
                         bg=C_WHITE, fg=C_TEXT, anchor="w",
                         wraplength=270, justify="left").pack(side="left", fill="x")

            _row(det, "📍", b["start"])
            _row(det, "🏁", b["end"])
            _row(det, "🚗", f"{b['vehicle_type']}  •  {b['distance']} km")
            _row(det, "💰", f"{PHP}{float(b['total_cost']):,.2f}")

            if b["status"] == "Assigned":
                def mark_done(bid=b["booking_id"]):
                    if messagebox.askyesno("Complete Booking",
                                            "Mark this trip as completed?"):
                        if complete_booking(bid, app.current_user["username"]):
                            messagebox.showinfo("Completed", "Trip marked as completed!")
                            app.show_rider_assigned()
                        else:
                            messagebox.showerror("Error", "Unable to complete this booking.")

                btn_row = tk.Frame(card, bg=C_WHITE, padx=14, pady=0)
                btn_row.pack(fill="x", pady=(0, 12))
                tk.Button(btn_row, text="Mark as Done",
                          font=("Helvetica", 11, "bold"),
                          bg=C_TEAL, fg=C_WHITE, bd=0, pady=9,
                          cursor="hand2", relief="flat",
                          command=mark_done).pack(fill="x")

    tk.Frame(body, bg=C_BG, height=16).pack()


# ─────────────────────────────────────────────
#  RIDER: UPDATE AVAILABILITY
# ─────────────────────────────────────────────

def build_rider_availability(app):
    frm = app.clear()
    frm.configure(bg=C_BG)
    user = app.current_user or {}

    _header(frm, title="Availability",
            subtitle="Go online or offline",
            back_cmd=app.show_rider_home)
    _rider_nav(frm, "jobs", app)

    body = tk.Frame(frm, bg=C_BG)
    body.pack(fill="both", expand=True, pady=40)

    is_available = user.get("available", True)

    icon = "🟢" if is_available else "⚫"
    tk.Label(body, text=icon, font=("Helvetica", 56), bg=C_BG).pack(pady=(0, 10))

    status_var = tk.StringVar(value="Available" if is_available else "Offline")
    tk.Label(body, textvariable=status_var, font=("Helvetica", 18, "bold"),
             bg=C_BG, fg=C_TEXT).pack()
    tk.Label(body, text="Toggle your status to start or stop receiving bookings.",
             font=("Helvetica", 11), bg=C_BG, fg=C_SUBTEXT,
             wraplength=300, justify="center").pack(pady=(4, 20))

    def toggle():
        riders = load(RIDERS_FILE)
        for r in riders:
            if r["username"] == app.current_user["username"]:
                r["available"] = not r.get("available", True)
                app.current_user = r
                break
        save(RIDERS_FILE, riders)
        app.show_rider_availability()

    btn_text = "Go Offline" if is_available else "Go Available"
    btn_bg   = "#FEE2E2" if is_available else "#DCFCE7"
    btn_fg   = C_RED if is_available else "#166534"

    tk.Button(body, text=btn_text, font=("Helvetica", 13, "bold"),
              bg=btn_bg, fg=btn_fg, bd=0, pady=14,
              cursor="hand2", relief="flat",
              command=toggle).pack(fill="x", padx=20)


# ─────────────────────────────────────────────
#  RIDER SETTINGS
# ─────────────────────────────────────────────

def build_rider_settings(app):
    frm = app.clear()
    frm.configure(bg=C_BG)
    user  = app.current_user or {}
    name  = user.get("full_name", "Rider")

    _header(frm, title="Settings", subtitle="Manage your rider account")
    _rider_nav(frm, "settings", app)

    _, _, body = scrollable(frm)

    av_frm = tk.Frame(body, bg=C_BG)
    av_frm.pack(pady=20)
    cv = tk.Canvas(av_frm, width=72, height=72, bg=C_BG, highlightthickness=0)
    cv.pack()
    cv.create_oval(2, 2, 70, 70, fill=C_TEAL, outline="")
    cv.create_text(36, 36, text=(name[0].upper() if name else "R"),
                   font=("Helvetica", 26, "bold"), fill=C_WHITE)
    tk.Label(av_frm, text=name, font=("Helvetica", 14, "bold"),
             bg=C_BG, fg=C_TEXT).pack(pady=(8, 2))
    tk.Label(av_frm, text=f"Vehicle: {_vehicle_display(user.get('vehicle_type','—'))}",
             font=("Helvetica", 10), bg=C_BG, fg=C_SUBTEXT).pack()

    _section_label(body, "Edit Account")
    edit_card = _card(body)

    _, u_ent = field(edit_card, "New Username",  user.get("username", ""))
    _, n_ent = field(edit_card, "New Full Name", user.get("full_name", ""))
    _, p_ent = field(edit_card, "New Password (leave blank to keep)", "", password=True)

    status_var = tk.StringVar()
    tk.Label(edit_card, textvariable=status_var,
             font=("Helvetica", 10), bg=C_WHITE,
             fg=C_GREEN, anchor="w").pack(fill="x", pady=(4, 0))

    def save_changes():
        new_u = u_ent.get().strip()
        new_n = n_ent.get().strip()
        new_p = p_ent.get().strip()
        if not new_u:
            messagebox.showerror("Error", "Username cannot be empty."); return
        if not new_n:
            messagebox.showerror("Error", "Full name cannot be empty."); return

        riders = load(RIDERS_FILE)
        for r in riders:
            if r["username"] == app.current_user["username"]:
                if new_u != r["username"]:
                    if any(x["username"] == new_u for x in riders if x is not r):
                        messagebox.showerror("Error", "Username already taken."); return
                r["username"]  = new_u
                r["full_name"] = new_n
                if new_p:
                    r["password"] = hash_pw(new_p)
                app.current_user = r
                break
        save(RIDERS_FILE, riders)
        status_var.set("✓ Changes saved successfully!")

    _pill_btn(edit_card, "Save Changes", save_changes, pady=11)

    tk.Frame(body, bg=C_BG, height=8).pack()
    tk.Button(body, text="Logout",
              font=("Helvetica", 13, "bold"),
              bg="#FEE2E2", fg=C_RED,
              bd=0, pady=13, cursor="hand2", relief="flat",
              command=app.show_splash).pack(fill="x", padx=16)
    tk.Frame(body, bg=C_BG, height=16).pack()


# ─────────────────────────────────────────────
#  RIDER INFO / ABOUT
# ─────────────────────────────────────────────

def build_rider_info(app):
    frm = app.clear()
    frm.configure(bg=C_BG)

    _header(frm, title="About", subtitle="HARUUROT Ride Booking")
    _rider_nav(frm, "info", app)

    _, _, body = scrollable(frm)
    tk.Frame(body, bg=C_BG, height=20).pack()

    cv = tk.Canvas(body, width=80, height=80, bg=C_BG, highlightthickness=0)
    cv.pack()
    cv.create_oval(2, 2, 78, 78, fill=C_ACCENT, outline="")
    cv.create_text(40, 40, text="H", font=("Helvetica", 30, "bold"), fill=C_WHITE)

    tk.Label(body, text="HARUUROT", font=("Helvetica", 18, "bold"),
             bg=C_BG, fg=C_TEXT).pack(pady=(10, 2))
    tk.Label(body, text="Ride Fast. Ride Safe. Ride Haruurot!",
             font=("Helvetica", 11), bg=C_BG, fg=C_SUBTEXT).pack()

    tk.Frame(body, bg=C_BG, height=20).pack()

    infos = [
        ("Team",      "BSCpE 1-3 Group 4"),
        ("Version",   "1.0.0"),
        ("Platform",  "Desktop (Tkinter)"),
        ("Currency",  "Philippine Peso (PHP ₱)"),
        ("Support",   "support@haruurot.ph"),
    ]
    card = _card(body)
    for label, val in infos:
        r = tk.Frame(card, bg=C_WHITE, pady=8)
        r.pack(fill="x")
        tk.Label(r, text=label, font=("Helvetica", 10),
                 bg=C_WHITE, fg=C_SUBTEXT, width=12, anchor="w").pack(side="left")
        tk.Label(r, text=val, font=("Helvetica", 10, "bold"),
                 bg=C_WHITE, fg=C_TEXT, anchor="w").pack(side="left")
        tk.Frame(card, bg="#F3F4F6", height=1).pack(fill="x")

    _render_credits(body)

    tk.Frame(body, bg=C_BG, height=16).pack()