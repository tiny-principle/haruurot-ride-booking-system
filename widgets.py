# widgets.py
# ─────────────────────────────────────────────
#  REUSABLE HELPER WIDGETS
# ─────────────────────────────────────────────

import tkinter as tk
from constants import (
    C_PURPLE_DARK, C_PURPLE_MID, C_BG, C_WHITE, C_TEXT, C_SUBTEXT,
    C_ACCENT, C_RED, C_BTN_DARK,
    FONT_H2, FONT_BODY, FONT_SMALL, FONT_BTN, FONT_LABEL,
)


def header(parent, title, subtitle=None, back_cmd=None):
    """Dark purple header banner with optional back arrow."""
    frm = tk.Frame(parent, bg=C_PURPLE_DARK, padx=20, pady=14)
    frm.pack(fill="x")
    if back_cmd:
        tk.Button(
            frm, text="←", font=("Helvetica", 16),
            bg=C_PURPLE_DARK, fg=C_WHITE, bd=0,
            activebackground=C_PURPLE_DARK, activeforeground=C_WHITE,
            cursor="hand2", command=back_cmd,
        ).pack(anchor="w")
    tk.Label(frm, text=title, font=FONT_H2, bg=C_PURPLE_DARK, fg=C_WHITE).pack(anchor="w")
    if subtitle:
        tk.Label(frm, text=subtitle, font=FONT_BODY, bg=C_PURPLE_DARK, fg="#C4B5FD").pack(anchor="w")


def scrollable(parent):
    """Return (outer_frame, canvas, inner_frame) for a scrollable content area."""
    outer = tk.Frame(parent, bg=C_BG)
    outer.pack(fill="both", expand=True)

    canvas = tk.Canvas(outer, bg=C_BG, highlightthickness=0)
    vsb    = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    inner = tk.Frame(canvas, bg=C_BG)
    win   = canvas.create_window((0, 0), window=inner, anchor="nw")

    def _resize(e):
        canvas.itemconfig(win, width=e.width)

    def _scroll(e):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _mousewheel(e):
        try:
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        except tk.TclError:
            pass

    def _bind_wheel(e):
        canvas.bind_all("<MouseWheel>", _mousewheel)

    def _unbind_wheel(e):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Configure>", _resize)
    inner.bind("<Configure>", _scroll)
    canvas.bind("<Enter>", _bind_wheel)
    canvas.bind("<Leave>", _unbind_wheel)
    canvas.bind("<Destroy>", _unbind_wheel)

    return outer, canvas, inner


def field(parent, label_text, placeholder="", password=False, error_var=None):
    """Labelled input field with purple border. Returns (frame, entry)."""
    frm = tk.Frame(parent, bg=C_BG)
    frm.pack(fill="x", pady=(0, 4))

    tk.Label(frm, text=label_text, font=FONT_LABEL, bg=C_BG, fg=C_TEXT, anchor="w").pack(fill="x")

    entry_frm = tk.Frame(frm, bg=C_ACCENT, bd=0, padx=1, pady=1)
    entry_frm.pack(fill="x")
    inner = tk.Frame(entry_frm, bg=C_WHITE)
    inner.pack(fill="x")

    show = "*" if password else ""
    ent  = tk.Entry(inner, font=FONT_BODY, bd=0, bg=C_WHITE, fg=C_TEXT, show=show, relief="flat")
    ent.pack(side="left", fill="x", expand=True, padx=10, pady=10)

    if placeholder:
        ent.insert(0, placeholder)
        ent.config(fg=C_SUBTEXT)

        def on_focus_in(e):
            if ent.get() == placeholder:
                ent.delete(0, "end")
                ent.config(fg=C_TEXT)

        def on_focus_out(e):
            if not ent.get():
                ent.insert(0, placeholder)
                ent.config(fg=C_SUBTEXT)

        ent.bind("<FocusIn>",  on_focus_in)
        ent.bind("<FocusOut>", on_focus_out)

    if password:
        vis = [False]
        eye_btn = tk.Button(inner, text="👁", font=FONT_SMALL, bd=0,
                            bg=C_WHITE, fg=C_SUBTEXT, cursor="hand2")

        def toggle_vis():
            vis[0] = not vis[0]
            ent.config(show="" if vis[0] else "*")

        eye_btn.config(command=toggle_vis)
        eye_btn.pack(side="right", padx=6)

    if error_var is not None:
        tk.Label(frm, textvariable=error_var, font=FONT_SMALL,
                 bg=C_BG, fg=C_RED, anchor="w").pack(fill="x")

    return frm, ent


def big_button(parent, text, cmd, bg=C_BTN_DARK, fg=C_WHITE, pady=14):
    """Wide, flat-styled action button."""
    btn = tk.Button(
        parent, text=text, font=FONT_BTN, bg=bg, fg=fg,
        activebackground=C_PURPLE_MID, activeforeground=C_WHITE,
        bd=0, padx=20, pady=pady, cursor="hand2", relief="flat", command=cmd,
    )
    btn.pack(fill="x", padx=20, pady=(6, 0))
    return btn


def nav_bar(parent, buttons):
    """Bottom navigation bar. buttons = list of (icon, label, cmd)."""
    bar = tk.Frame(parent, bg=C_PURPLE_DARK, pady=6)
    bar.pack(side="bottom", fill="x")
    for icon, lbl, cmd in buttons:
        col = tk.Frame(bar, bg=C_PURPLE_DARK)
        col.pack(side="left", expand=True)
        tk.Button(col, text=icon, font=("Helvetica", 18), bg=C_PURPLE_DARK,
                  fg=C_WHITE, bd=0, activebackground=C_PURPLE_MID,
                  cursor="hand2", command=cmd).pack()
        tk.Label(col, text=lbl, font=FONT_SMALL, bg=C_PURPLE_DARK, fg=C_WHITE).pack()


def menu_card(parent, icon, title, desc, cmd, icon_bg="#E8E8F4"):
    """White card row with icon, title, description, and chevron."""
    card = tk.Frame(parent, bg=C_WHITE, bd=0, relief="flat", cursor="hand2")
    card.pack(fill="x", padx=20, pady=8)
    card.bind("<Button-1>", lambda e: cmd())

    # subtle bottom shadow line
    tk.Frame(parent, bg="#D1D5DB", height=2).pack(fill="x", padx=22)

    inner = tk.Frame(card, bg=C_WHITE)
    inner.pack(fill="x", padx=14, pady=12)

    icon_box = tk.Frame(inner, bg=icon_bg, width=56, height=56)
    icon_box.pack(side="left", padx=(0, 12))
    icon_box.pack_propagate(False)
    icon_lbl = tk.Label(icon_box, text=icon, font=("Helvetica", 22), bg=icon_bg)
    icon_lbl.place(relx=0.5, rely=0.5, anchor="center")

    txt = tk.Frame(inner, bg=C_WHITE)
    txt.pack(side="left", fill="both", expand=True)
    title_lbl = tk.Label(txt, text=title, font=("Helvetica", 13, "bold"),
                          bg=C_WHITE, fg=C_TEXT, anchor="w")
    title_lbl.pack(fill="x")
    desc_lbl = tk.Label(txt, text=desc, font=FONT_SMALL, bg=C_WHITE, fg=C_SUBTEXT,
                         anchor="w", wraplength=210, justify="left")
    desc_lbl.pack(fill="x")

    chevron = tk.Label(inner, text="›", font=("Helvetica", 20), bg=C_WHITE, fg=C_ACCENT)
    chevron.pack(side="right")

    def _bind_all(w):
        w.bind("<Button-1>", lambda e: cmd())
        w.configure(cursor="hand2")
        for ch in w.winfo_children():
            _bind_all(ch)
    _bind_all(card)


def divider(parent):
    tk.Frame(parent, bg="#D1D5DB", height=1).pack(fill="x", padx=0)