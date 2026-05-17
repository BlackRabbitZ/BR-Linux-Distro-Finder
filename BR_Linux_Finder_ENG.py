#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BlackRabbitZ Linux Finder GUI FINAL
Start: python3 linux_finder_gui.py
logo.png is located in the same folder and loads automatically.
"""

import os, json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    from PIL import Image, ImageTk
    PIL_OK = True
except Exception:
    PIL_OK = False

APP_TITLE = "BlackRabbitZ Linux Distributions Finder"

COLORS = {
    "bg":"#0b0c0f", "panel":"#111216", "panel2":"#17181d", "card":"#0f1014",
    "border":"#2d3038", "red":"#ff2436", "red2":"#b61726", "line":"#7f141d",
    "text":"#f1f1f1", "muted":"#b9bcc4", "soft":"#858a94", "select":"#20222a"
}
BASE_FONT = ("Segoe UI", 10)
SMALL_FONT = ("Segoe UI", 9)
TITLE_FONT = ("Segoe UI Semibold", 30)
SUB_FONT = ("Segoe UI Semibold", 13)
QUESTION_FONT = ("Segoe UI Semibold", 10)
MONO_FONT = ("Consolas", 10)

# Extended Linux distribution database
DISTROS = {
    # Daily / Office / Beginners
    "Linux Mint": ["beginner","daily","office","stable","windows_like","low","laptop"],
    "Ubuntu": ["beginner","daily","office","dev","support","server","gnome"],
    "Kubuntu": ["beginner","daily","office","kde","windows_like"],
    "Xubuntu": ["beginner","daily","office","xfce","low","old_hw"],
    "Lubuntu": ["beginner","daily","office","lxqt","very_low","old_hw"],
    "Zorin OS": ["beginner","daily","office","modern","windows_like"],
    "elementary OS": ["beginner","daily","office","modern","mac_like"],
    "Pop!_OS": ["beginner","daily","dev","gaming","nvidia","modern","laptop"],
    "KDE neon": ["daily","office","kde","modern"],
    "MX Linux": ["beginner","daily","stable","low","old_hw"],
    "Peppermint OS": ["beginner","daily","low","old_hw"],
    "PCLinuxOS": ["beginner","daily","office","stable"],
    "TUXEDO OS": ["beginner","daily","office","kde","laptop","gaming"],
    "Solus": ["daily","office","modern","gaming"],

    # Gaming
    "Nobara Linux": ["gaming","steam","proton","aaa","nvidia","amd_gpu","performance","beginner","current"],
    "Bazzite": ["gaming","steam","proton","console","aaa","nvidia","amd_gpu","immutable","beginner"],
    "ChimeraOS": ["gaming","steam","console","amd_gpu","proton"],
    "Drauger OS": ["gaming","performance","aaa","nvidia","amd_gpu"],
    "Garuda Linux": ["gaming","arch","performance","kde","rolling","current"],
    "CachyOS": ["gaming","arch","performance","rolling","current"],
    "Regata OS": ["gaming","steam","kde","beginner"],
    "SteamOS": ["gaming","steam","console","amd_gpu"],
    "Fedora Games Spin": ["gaming","current","fedora"],

    # Development
    "Fedora Workstation": ["dev","ai","docker","current","gnome","modern"],
    "Fedora KDE Spin": ["dev","current","kde","modern"],
    "Debian": ["stable","server","daily","office","privacy","dev","low"],
    "openSUSE Leap": ["stable","server","office","kde"],
    "openSUSE Tumbleweed": ["dev","rolling","current","kde","docker"],
    "EndeavourOS": ["arch","advanced","rolling","current","dev","gaming"],
    "Arch Linux": ["expert","arch","rolling","current","control","dev"],
    "Manjaro": ["arch","beginner","current","gaming","daily"],
    "NixOS": ["advanced","dev","docker","reproducible","security"],
    "Void Linux": ["advanced","control","low","dev"],
    "Gentoo": ["expert","control","source","dev"],

    # Pentesting / Ethical Hacking / Security
    "Kali Linux": ["pentest","ethical_hacking","security","tools","wifi","web_pentest","network_pentest","forensics","advanced"],
    "Parrot OS": ["pentest","ethical_hacking","security","privacy","tools","web_pentest","osint","beginner"],
    "BlackArch Linux": ["pentest","ethical_hacking","security","arch","expert","tools","exploit","reverse"],
    "BackBox Linux": ["pentest","ethical_hacking","security","tools","beginner","web_pentest"],
    "Pentoo": ["pentest","security","wifi","forensics","advanced"],
    "ArchStrike": ["pentest","arch","security","advanced"],
    "SamuraiWTF": ["pentest","web_pentest","security","tools"],
    "NST Linux": ["pentest","network_pentest","security","forensics"],
    "CAINE": ["security","forensics","pentest"],
    "REMnux": ["security","malware","reverse","forensics"],
    "Security Onion": ["security","blue_team","monitoring","server"],
    "SELKS": ["security","blue_team","monitoring","server"],

    # Privacy / Anonymity
    "Tails": ["privacy","anonymity","tor","live_usb","security"],
    "Qubes OS": ["privacy","security","compartment","advanced","vm","isolation"],
    "Whonix": ["privacy","anonymity","tor","vm","security"],
    "Kodachi Linux": ["privacy","anonymity","tor","live_usb"],
    "Septor Linux": ["privacy","anonymity","tor","daily"],
    "PureOS": ["privacy","daily","office","security"],
    "Heads": ["privacy","security","expert","live_usb"],
    "Alpine Linux": ["security","server","low","advanced"],

    # Server
    "Ubuntu Server": ["server","stable","support","docker"],
    "Rocky Linux": ["server","stable","enterprise"],
    "AlmaLinux": ["server","stable","enterprise"],
    "Oracle Linux": ["server","stable","enterprise"],
    "Fedora Server": ["server","current","docker"],

    # Old Hardware
    "antiX": ["very_low","old_hw","privacy","daily"],
    "Puppy Linux": ["very_low","old_hw","live_usb"],
    "Bodhi Linux": ["very_low","old_hw","daily"],
    "Tiny Core Linux": ["very_low","old_hw","expert"],
    "LXLE": ["low","old_hw","daily"],
    "SparkyLinux": ["low","old_hw","daily"],
}

RADIO_QUESTIONS = [
    # 1) Main purpose and usage
    ("main_use", "What is your main goal with Linux?", [
        ("daily","Daily Use / Internet / Media"),
        ("office","Office / School / Study"),
        ("gaming","Gaming"),
        ("dev","Programming / Development"),
        ("ethical_hacking","Learn Ethical Hacking"),
        ("pentest","Pentesting / Security Tools"),
        ("security","Cybersecurity / Analysis / Defense"),
        ("privacy","Privacy / Data Protection"),
        ("anonymity","Anonymity / Tor / Live System"),
        ("server","Server / Hosting / Home Server"),
        ("old_hw","Old or Low-End Hardware")
    ]),
    ("install_target", "How do you want to use Linux?", [
        ("linux_only","As main operating system"),
        ("dual","Dual Boot with Windows"),
        ("test","Just testing first"),
        ("vm","Inside a virtual machine"),
        ("live_usb","As a live USB system")
    ]),
    ("device", "What device will Linux run on?", [
        ("desktop","Desktop PC"),
        ("laptop","Laptop"),
        ("mini_pc","Mini-PC / NUC"),
        ("arm","ARM Device / Raspberry Pi / Apple Silicon"),
        ("server_hw","Server Hardware")
    ]),

    # 2) Erfahrung und Wartungsbereitschaft
    ("experience", "How much Linux experience do you have?", [
        ("beginner","Beginner / Never used Linux"),
        ("some","Basic knowledge"),
        ("advanced","Advanced"),
        ("expert","Expert / Power User")
    ]),
    ("install_effort", "How complex can installation and setup be?", [
        ("easy","Very easy"),
        ("medium_setup","Some setup is okay"),
        ("hard","Complex setup is okay")
    ]),
    ("maintenance", "How much maintenance do you want long-term?", [
        ("low_maintenance","As little maintenance as possible"),
        ("normal_maintenance","Normal updates are okay"),
        ("manual_control","I want full control")
    ]),
    ("updates", "What update style do you prefer?", [
        ("stable","Maximum stability / conservative packages"),
        ("balanced","Balanced"),
        ("current","Recent packages"),
        ("rolling","Rolling release / always latest")
    ]),

    # 3) Hardware - fachlich getrennt nach CPU, GPU, RAM, Speicher und Gerätestärke
    ("cpu", "Which CPU do you use?", [
        ("intel","Intel x86_64"),
        ("amd","AMD x86_64"),
        ("arm","ARM / Raspberry Pi / Apple Silicon")
    ]),
    ("gpu", "Which GPU do you use?", [
        ("nvidia","NVIDIA"),
        ("amd_gpu","AMD Radeon"),
        ("intel_gpu","Intel Graphics"),
        ("none","No dedicated GPU")
    ]),
    ("ram", "How much RAM do you have?", [
        ("very_low","Below 4 GB"),
        ("low","4 to 8 GB"),
        ("mid","8 to 16 GB"),
        ("high","16 to 32 GB"),
        ("very_high","32 GB or more")
    ]),
    ("storage", "How much storage space will Linux use?", [
        ("tiny","Below 32 GB"),
        ("small","32 to 64 GB"),
        ("medium_storage","128 to 256 GB"),
        ("large","More than 256 GB")
    ]),
    ("hardware_age", "How powerful is your system overall?", [
        ("new","New / Powerful hardware"),
        ("normal","Normal hardware"),
        ("old_hw","Older hardware"),
        ("very_low","Very weak hardware")
    ]),
    ("battery", "Is laptop battery life important?", [
        ("battery_yes","Yes, very important"),
        ("battery_some","Partially"),
        ("battery_no","No")
    ]),

    # 4) Oberfläche und Alltag
    ("desktop_env", "Which desktop environment fits you best?", [
        ("windows_like","Windows-like"),
        ("kde","KDE Plasma / highly customizable"),
        ("gnome","GNOME / modern and clean"),
        ("xfce","XFCE / lightweight"),
        ("mac_like","MacOS-like"),
        ("minimal","Minimalistic")
    ]),
    ("office_use", "Which office or daily-use tasks are important?", [
        ("private","Private / Daily Use"),
        ("school","School / University"),
        ("business","Business / Home Office"),
        ("documents","Documents, spreadsheets, presentations")
    ]),

    # 5) Datenschutz, Anonymität und Sicherheit - getrennt, weil es nicht dasselbe ist
    ("privacy_level", "How important are privacy and data protection?", [
        ("normal_privacy","Normal"),
        ("privacy","High"),
        ("privacy_strict","Very high / minimal digital footprint")
    ]),
    ("anonymity_level", "Do you need online anonymity?", [
        ("no_anonymity","No"),
        ("tor_optional","Partially mit Tor"),
        ("anonymity","Yes, anonymity is a main goal"),
        ("live_anonymity","Maximum anonymity via live system")
    ]),
    ("security_level", "What security level do you want?", [
        ("standard","Standard daily security"),
        ("security","High"),
        ("hardened","Very high / hardened"),
        ("compartment","Isolation / compartmentalization / Qubes approach")
    ]),

    # 6) Gaming - nur sinnvoll, wenn Gaming relevant ist; No Gaming neutralisiert Gaming-Tags
    ("gaming_type", "Which gaming category fits best?", [
        ("no_gaming","No Gaming"),
        ("steam","Steam / Proton"),
        ("aaa","AAA Games"),
        ("competitive","Competitive Games"),
        ("retro","Retro / Emulators"),
        ("console","Console-like system"),
        ("casual","Casual Gaming")
    ]),
    ("anticheat", "Are anti-cheat games important to you?", [
        ("no_anticheat","No"),
        ("partly","Partially"),
        ("yes","Yes, very important")
    ]),

    # 7) Server und Virtualisierung
    ("server_use", "Do you want to use Linux as a server?", [
        ("no_server","No"),
        ("homeserver","Home Server"),
        ("professional_server","Professional Server"),
        ("docker","Docker / Container / DevOps")
    ]),
    ("virtualization", "Do you need virtualization or containers?", [
        ("no_vm","No"),
        ("docker","Docker / Container"),
        ("vm","Virtual Machines"),
        ("isolation","Strong isolation / sandboxing")
    ]),
]

CHECK_QUESTIONS = [
    ("gaming_extra", "Gaming: What exactly do you need?", [
        ("no_gaming","No Gaming"),
        ("steam","Steam"),
        ("proton","Proton / Windows-Spiele"),
        ("aaa","AAA-Games"),
        ("competitive","Competitive Games"),
        ("retro","Retro / Emulators"),
        ("minecraft","Minecraft"),
        ("performance","Maximum Performance")
    ]),
    ("pentest_extra", "Pentesting / Ethical Hacking: Which areas?", [
        ("no_pentest","NOTHING"),
        ("wifi","WiFi Security"),
        ("web_pentest","Web Pentesting"),
        ("network_pentest","Network Pentesting"),
        ("reverse","Reverse Engineering"),
        ("malware","Malware Analysis"),
        ("exploit","Exploit Development"),
        ("forensics","Forensics"),
        ("red_team","Red Teaming"),
        ("blue_team","Blue Teaming"),
        ("osint","OSINT")
    ]),
    ("dev_extra", "Programming / Development: Was machst du?", [
        ("no_dev","None"),
        ("python","Python"),
        ("webdev","Web Development"),
        ("cpp","C / C++"),
        ("rust","Rust"),
        ("java","Java"),
        ("ai","AI / Machine Learning"),
        ("docker","Docker / DevOps"),
        ("android","Android")
    ]),
    ("office_extra", "Office / Daily Use: What is important?", [
        ("no_office_extra","None Angabe"),
        ("office","Office"),
        ("daily","Internet / Daily Use"),
        ("multimedia","Multimedia"),
        ("printer","Printer / Scanner"),
        ("support","Large Community"),
        ("laptop","Laptop Battery Life")
    ]),
]

TAG_ALIASES = {
    # Erfahrung / Bedienung
    "some":"beginner", "easy":"beginner", "medium_setup":"beginner", "hard":"advanced",
    "low_maintenance":"stable", "normal_maintenance":"balanced", "manual_control":"control",
    "balanced":"current",

    # Installation / Gerät
    "dual":"beginner", "test":"live_usb", "linux_only":"daily", "mini_pc":"daily", "server_hw":"server",
    "battery_yes":"laptop", "battery_some":"laptop", "battery_no":"daily",

    # Office / Daily Use
    "private":"office", "school":"office", "business":"office", "documents":"office",
    "normal_privacy":"daily", "no_anonymity":"daily", "standard":"daily",

    # Hardware
    "new":"current", "normal":"daily", "tiny":"very_low", "small":"low", "medium_storage":"daily",
    "large":"daily", "very_high":"performance", "mid":"daily", "high":"performance",
    "intel_gpu":"daily", "none":"daily", "arm":"advanced",

    # Datenschutz / Sicherheit
    "privacy_strict":"privacy", "tor_optional":"tor", "live_anonymity":"live_usb",
    "hardened":"security", "compartment":"isolation",

    # Gaming / Server / VM
    "yes":"gaming", "partly":"gaming", "no_anticheat":"daily", "casual":"gaming",
    "no_gaming":"daily", "no_server":"daily", "homeserver":"server", "professional_server":"server",
    "no_vm":"daily",

    # Neutrale Multiple Selectionpunkte
    "no_pentest":"daily", "no_dev":"daily", "no_office_extra":"daily"
}

WARNINGS = {
    "Qubes OS": "Qubes OS braucht starke Hardware, Virtualisierung und ist eher für Advancede geeignet.",
    "Tails": "Tails is designed for live USB anonymity, not as a regular daily operating system.",
    "Kali Linux": "Kali Linux is mainly designed for pentesting and is not ideal as a normal daily operating system.",
    "BlackArch Linux": "BlackArch is very extensive and intended for experienced users.",
    "SteamOS": "SteamOS is heavily optimized for gaming and Steam Deck-like usage.",
}

def res_path(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), name)

class ScrollFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Panel.TFrame")
        self.canvas = tk.Canvas(self, bg=COLORS["panel"], highlightthickness=0)
        self.inner = ttk.Frame(self.canvas, style="Panel.TFrame")
        self.scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview, style="Red.Vertical.TScrollbar")
        self.win = self.canvas.create_window((0,0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.win, width=e.width))
        self.canvas.bind_all("<MouseWheel>", self._wheel)
    def _wheel(self, event):
        if self.winfo_containing(event.x_root, event.y_root):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1420x850")
        self.minsize(1120, 720)
        self.configure(bg=COLORS["bg"])
        self.vars, self.check_vars = {}, {}
        self.logo_img = None
        self._style(); self._ui()

    def _style(self):
        s=ttk.Style(self)
        try: s.theme_use("clam")
        except tk.TclError: pass
        s.configure("Root.TFrame", background=COLORS["bg"])
        s.configure("Panel.TFrame", background=COLORS["panel"])
        s.configure("Card.TFrame", background=COLORS["panel"], bordercolor=COLORS["border"], relief="solid", borderwidth=1)
        s.configure("TLabel", background=COLORS["panel"], foreground=COLORS["text"], font=BASE_FONT)
        s.configure("Title.TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=TITLE_FONT)
        s.configure("Tag.TLabel", background=COLORS["bg"], foreground=COLORS["red"], font=("Consolas", 15))
        s.configure("Muted.TLabel", background=COLORS["bg"], foreground=COLORS["muted"], font=BASE_FONT)
        s.configure("Section.TLabel", background=COLORS["panel"], foreground=COLORS["red"], font=SUB_FONT)
        s.configure("Question.TLabel", background=COLORS["panel"], foreground=COLORS["text"], font=QUESTION_FONT)
        s.configure("TRadiobutton", background=COLORS["panel"], foreground=COLORS["muted"], font=BASE_FONT, focuscolor=COLORS["panel"])
        s.map("TRadiobutton", background=[("active", COLORS["panel"])], foreground=[("selected", COLORS["red"]),("active", COLORS["text"])])
        s.configure("TCheckbutton", background=COLORS["panel"], foreground=COLORS["muted"], font=BASE_FONT, focuscolor=COLORS["panel"])
        s.map("TCheckbutton", background=[("active", COLORS["panel"])], foreground=[("selected", COLORS["red"]),("active", COLORS["text"])])
        s.configure("Red.TButton", background=COLORS["panel2"], foreground=COLORS["text"], bordercolor=COLORS["red"], padding=(13,9), font=("Segoe UI Semibold", 9))
        s.map("Red.TButton", background=[("active", COLORS["select"])], foreground=[("active", COLORS["red"])])
        s.configure("Red.Vertical.TScrollbar", background=COLORS["red2"], troughcolor=COLORS["panel2"], arrowcolor=COLORS["red"], bordercolor=COLORS["panel2"])

    def _ui(self):
        root=ttk.Frame(self, style="Root.TFrame", padding=12); root.pack(fill="both", expand=True)
        header=ttk.Frame(root, style="Root.TFrame"); header.pack(fill="x", pady=(0,12))
        logo_frame=tk.Frame(header, bg=COLORS["bg"], highlightbackground=COLORS["border"], highlightthickness=1, width=300, height=300)
        logo_frame.pack(side="left", padx=(0,28)); logo_frame.pack_propagate(False)
        self._load_logo(logo_frame)
        htext=ttk.Frame(header, style="Root.TFrame"); htext.pack(side="left", fill="both", expand=True)
        title_row = ttk.Frame(htext, style="Root.TFrame")
        title_row.pack(anchor="w", pady=(10,4))

        tk.Label(
            title_row,
            text="BlackRabbit",
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=TITLE_FONT
        ).pack(side="left")

        tk.Label(
            title_row,
            text="Z",
            bg=COLORS["bg"],
            fg=COLORS["red"],
            font=TITLE_FONT
        ).pack(side="left")

        tk.Label(
            title_row,
            text=" Linux Distributions Finder",
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=TITLE_FONT
        ).pack(side="left")
        ttk.Label(htext, text="SECURE. PROTECT. ANONYMIZE.", style="Tag.TLabel").pack(anchor="w")
        tk.Frame(htext, bg=COLORS["red2"], height=2).pack(fill="x", pady=14)
        ttk.Label(
            htext,
            text="Professional Linux distribution platform for gaming, cybersecurity, privacy, development and productive Linux workflows.\n\nThe system analyzes hardware, security requirements, privacy needs, user experience, gaming compatibility and development environments to intelligently recommend suitable Linux distributions.",
            style="Muted.TLabel"
        ).pack(anchor="w")

        main=ttk.Frame(root, style="Root.TFrame"); main.pack(fill="both", expand=True)
        left=ttk.Frame(main, style="Card.TFrame", padding=12); left.pack(side="left", fill="both", expand=True, padx=(0,8))
        right=ttk.Frame(main, style="Card.TFrame", padding=12); right.pack(side="right", fill="both", expand=True, padx=(8,0))
        ttk.Label(left, text="❔  QUESTIONS", style="Section.TLabel").pack(anchor="w", pady=(0,10))
        sf=ScrollFrame(left); sf.pack(fill="both", expand=True)
        self._build_questions(sf.inner)

        ttk.Label(right, text="◉  OUTPUT / RECOMMENDATION", style="Section.TLabel").pack(anchor="w", pady=(0,10))
        self.out=tk.Text(right, bg="#090a0d", fg=COLORS["text"], insertbackground=COLORS["red"], relief="solid", bd=1,
                         highlightbackground=COLORS["border"], font=MONO_FONT, wrap="word", padx=18, pady=18)
        self.out.pack(fill="both", expand=True)
        self.out.insert("1.0", "No evaluation yet.\n\nAnswer the questions on the left and click EVALUATE.")
        btns=ttk.Frame(right, style="Panel.TFrame"); btns.pack(fill="x", pady=(12,0))
        ttk.Button(btns, text="▷ EVALUATE", style="Red.TButton", command=self.evaluate).pack(side="left", padx=(0,8))
        ttk.Button(btns, text="▣ SAVE RESULT", style="Red.TButton", command=self.save_result).pack(side="left", padx=8)
        ttk.Button(btns, text="↺ RESET", style="Red.TButton", command=self.reset).pack(side="left", padx=8)
        ttk.Button(btns, text="☰ SHOW DISTRIBUTIONS", style="Red.TButton", command=self.show_distros).pack(side="left", padx=8)
        ttk.Button(btns, text="ⓘ ABOUT ME", style="Red.TButton", command=self.about_me).pack(side="left", padx=8)

    def _load_logo(self, parent):
        """
        Lädt das vollständige BlackRabbitZ-Logo.
        Das Logo wird proportional skaliert, damit NICHT nur ein Ausschnitt sichtbar ist.
        """
        logo_files = ["logo.png", "logo 2.png", "BlackRabbitZ.png", "blackrabbitz.png"]

        for fname in logo_files:
            p = res_path(fname)
            if os.path.exists(p):
                try:
                    if PIL_OK:
                        img = Image.open(p).convert("RGBA")
                        img.thumbnail((280, 280), Image.LANCZOS)
                        self.logo_img = ImageTk.PhotoImage(img)
                    else:
                        self.logo_img = tk.PhotoImage(file=p)

                    tk.Label(
                        parent,
                        image=self.logo_img,
                        bg=COLORS["bg"],
                        borderwidth=0
                    ).pack(expand=True)
                    return
                except Exception as e:
                    print(f"Logo konnte nicht geladen werden: {p} | {e}")

        tk.Label(
            parent,
            text="BlackRabbitZ\nLogo missing",
            bg=COLORS["bg"],
            fg=COLORS["red"],
            font=("Segoe UI Semibold", 16),
            justify="center"
        ).pack(expand=True)

    def _build_questions(self, parent):
        n=1
        for key, title, opts in RADIO_QUESTIONS:
            self._qblock(parent, n, title)
            var=tk.StringVar(value=opts[0][0]); self.vars[key]=var
            for val, label in opts:
                ttk.Radiobutton(parent, text=label, value=val, variable=var).pack(anchor="w", padx=46, pady=2)
            self._sep(parent); n+=1
        for key, title, opts in CHECK_QUESTIONS:
            self._qblock(parent, n, title)
            self.check_vars[key]={}
            for val, label in opts:
                v=tk.BooleanVar(value=False); self.check_vars[key][val]=v
                ttk.Checkbutton(parent, text=label, variable=v).pack(anchor="w", padx=46, pady=2)
            self._sep(parent); n+=1

    def _qblock(self, parent, num, title):
        row=ttk.Frame(parent, style="Panel.TFrame"); row.pack(fill="x", pady=(8,4))
        badge=tk.Label(row, text=str(num), bg=COLORS["panel"], fg=COLORS["red"], font=("Segoe UI Semibold", 11), width=3)
        badge.pack(side="left")
        ttk.Label(row, text=title, style="Question.TLabel").pack(side="left", padx=(5,0))
    def _sep(self, parent):
        tk.Frame(parent, bg=COLORS["line"], height=1).pack(fill="x", padx=14, pady=12)

    def _selected_tags(self):
        tags=[]
        for k,v in self.vars.items():
            val=v.get(); tags.append(val); tags.append(TAG_ALIASES.get(val,val))
        for group, vals in self.check_vars.items():
            for tag,var in vals.items():
                if var.get(): tags.append(tag); tags.append(TAG_ALIASES.get(tag,tag))
        # Fachliche Sonderlogik
        main_use = self.vars.get("main_use", tk.StringVar(value="daily")).get()
        experience = self.vars.get("experience", tk.StringVar(value="beginner")).get()
        ram = self.vars.get("ram", tk.StringVar(value="mid")).get()
        install_target = self.vars.get("install_target", tk.StringVar(value="linux_only")).get()

        if experience == "beginner":
            tags += ["beginner", "easy", "support"]
        if experience == "expert":
            tags += ["expert", "control", "advanced"]

        if main_use in ["privacy", "anonymity"]:
            tags += ["privacy", "security"]
        if self.vars.get("anonymity_level", tk.StringVar(value="no_anonymity")).get() in ["anonymity", "live_anonymity"]:
            tags += ["anonymity", "tor", "privacy"]
        if self.vars.get("privacy_level", tk.StringVar(value="normal_privacy")).get() == "privacy_strict":
            tags += ["privacy", "security"]
        if self.vars.get("security_level", tk.StringVar(value="standard")).get() == "compartment" or self.vars.get("virtualization", tk.StringVar(value="no_vm")).get() == "isolation":
            tags += ["compartment", "isolation", "security", "privacy", "vm"]

        if ram in ["very_low", "low"]:
            tags += ["low", "very_low", "old_hw"]
        if ram in ["high", "very_high"]:
            tags += ["performance", "vm"]
        if install_target == "live_usb":
            tags += ["live_usb", "privacy"]

        # Wenn explizit kein Gaming gewählt wurde, keine Gaming-Tags durch optionale Antworten pushen.
        if self.vars.get("gaming_type", tk.StringVar(value="no_gaming")).get() == "no_gaming" and main_use != "gaming":
            tags = [t for t in tags if t not in ["gaming", "steam", "proton", "aaa", "competitive", "retro", "console", "minecraft"]]

        return tags

    def evaluate(self):
        tags=self._selected_tags()
        scores=[]
        for name, dtags in DISTROS.items():
            score=0; reasons=[]
            for t in tags:
                if t in dtags:
                    score+=3
                    if t not in reasons: reasons.append(t)
            # Abzüge
            if self.vars["experience"].get()=="beginner" and any(x in dtags for x in ["expert","advanced"]): score-=5
            if self.vars["main_use"].get() in ["daily","office"] and "pentest" in dtags: score-=4
            if self.vars["main_use"].get()=="gaming" and "gaming" not in dtags: score-=3
            if self.vars["main_use"].get()=="pentest" and "pentest" not in dtags: score-=3
            if self.vars["main_use"].get()=="anonymity" and "anonymity" not in dtags: score-=2
            if self.vars.get("gaming_type", tk.StringVar(value="no_gaming")).get()=="no_gaming" and self.vars["main_use"].get()!="gaming" and "gaming" in dtags: score-=5
            if self.vars.get("install_target", tk.StringVar(value="linux_only")).get()=="vm" and "live_usb" in dtags: score-=3
            if self.vars["ram"].get()=="very_low" and any(x in dtags for x in ["vm","compartment","gnome"]): score-=6
            if self.vars["gpu"].get()=="nvidia" and "nvidia" in dtags: score+=4
            if self.vars["gpu"].get()=="amd_gpu" and "amd_gpu" in dtags: score+=4
            if score>0: scores.append((score, name, reasons, dtags))
        scores.sort(reverse=True, key=lambda x:x[0])
        top=scores[:10]
        out=[]
        out.append("BLACKRABBITZ LINUX FINDER - RESULTS\n")
        out.append("Top Recommendations:\n")
        for i,(score,name,reasons,dtags) in enumerate(top,1):
            out.append(f"{i:02d}. {name}  | Score: {score}")
            out.append(f"    Matches because of: {', '.join(reasons[:8]) if reasons else 'general compatibility'}")
            out.append(f"    Category Tags: {', '.join(dtags[:12])}")
            if name in WARNINGS: out.append(f"    Note: {WARNINGS[name]}")
            out.append("")
        out.append("\nSelected Answers:\n")
        for key,title,opts in RADIO_QUESTIONS:
            val=self.vars[key].get(); label=next((l for v,l in opts if v==val), val)
            out.append(f"- {title} {label}")
        checked=[]
        for key,title,opts in CHECK_QUESTIONS:
            vals=[label for val,label in opts if self.check_vars[key][val].get()]
            if vals: checked.append(f"- {title} {', '.join(vals)}")
        if checked:
            out.append("\nMultiple Selection:")
            out.extend(checked)
        self.out.delete("1.0","end"); self.out.insert("1.0", "\n".join(out))

    def show_distros(self):
        grouped={"Gaming":[],"Pentesting / Ethical Hacking":[],"Privacy / Anonymity":[],"Office / Daily Use":[],"Server":[],"Old Hardware":[],"Development":[],"Other":[]}
        for n,t in DISTROS.items():
            if "gaming" in t: grouped["Gaming"].append(n)
            elif "pentest" in t or "ethical_hacking" in t: grouped["Pentesting / Ethical Hacking"].append(n)
            elif "privacy" in t or "anonymity" in t: grouped["Privacy / Anonymity"].append(n)
            elif "server" in t: grouped["Server"].append(n)
            elif "old_hw" in t or "very_low" in t: grouped["Old Hardware"].append(n)
            elif "dev" in t: grouped["Development"].append(n)
            elif "daily" in t or "office" in t: grouped["Office / Daily Use"].append(n)
            else: grouped["Other"].append(n)
        lines=[f"Included Distributions: {len(DISTROS)}\n"]
        for g,items in grouped.items():
            if items:
                lines.append(g+":")
                for item in sorted(items): lines.append("  - "+item)
                lines.append("")
        self.out.delete("1.0","end"); self.out.insert("1.0","\n".join(lines))

    def save_result(self):
        text=self.out.get("1.0","end").strip()
        if not text: return
        p=filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File","*.txt"),("JSON","*.json")], initialfile="blackrabbitz_linux_finder_result.txt")
        if not p: return
        try:
            if p.endswith(".json"):
                data={"created":datetime.now().isoformat(),"result":text,"answers":{k:v.get() for k,v in self.vars.items()}}
                with open(p,"w",encoding="utf-8") as f: json.dump(data,f,ensure_ascii=False,indent=2)
            else:
                with open(p,"w",encoding="utf-8") as f: f.write(text)
            messagebox.showinfo("Saved", "Result has been saved.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def about_me(self):
        win = tk.Toplevel(self)
        win.title("About BlackRabbitZ")
        win.geometry("700x420")
        win.configure(bg=COLORS["bg"])

        container = tk.Frame(
            win,
            bg=COLORS["panel"],
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            container,
            text="BlackRabbitZ",
            bg=COLORS["panel"],
            fg=COLORS["red"],
            font=("Segoe UI Semibold", 28)
        ).pack(pady=(25, 20))

        info_text = """# Copyright © 2026 BlackRabbitZ
# Author: BlackRabbitZ
# This script may not be modified,
# resold or claimed as your own work without permission."""

        tk.Label(
            container,
            text=info_text,
            justify="left",
            bg=COLORS["panel"],
            fg=COLORS["text"],
            font=("Consolas", 12)
        ).pack(pady=10)

        tk.Label(
            container,
            text="Discord",
            bg=COLORS["panel"],
            fg=COLORS["red"],
            font=("Segoe UI Semibold", 16)
        ).pack(pady=(30, 8))

        link = tk.Label(
            container,
            text="https://discord.gg/XX4E7FtXWk",
            bg=COLORS["panel"],
            fg="#6aa9ff",
            cursor="hand2",
            font=("Consolas", 12, "underline")
        )
        link.pack()

        def open_dc(event=None):
            import webbrowser
            webbrowser.open("https://discord.gg/XX4E7FtXWk")

        link.bind("<Button-1>", open_dc)


    def reset(self):
        for key,title,opts in RADIO_QUESTIONS: self.vars[key].set(opts[0][0])
        for group in self.check_vars.values():
            for v in group.values(): v.set(False)
        self.out.delete("1.0","end"); self.out.insert("1.0", "No evaluation yet.\n\nAnswer the questions on the left and click EVALUATE.")

if __name__ == "__main__":
    App().mainloop()
