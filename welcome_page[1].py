import customtkinter as ctk


# ── Palette ──────────────────────────────────────────────
BG          = "#0A0E1A"
SURFACE     = "#0D1B2A"
ACCENT      = "#00D4AA"
ACCENT_DIM  = "#00A882"
TEXT_MAIN   = "#E8F4F1"
TEXT_SUB    = "#7A99A8"
BORDER      = "#1A2744"


class WelcomePage(ctk.CTkFrame):

    def __init__(self, parent, start_callback):

        super().__init__(
            parent,
            fg_color=BG,
            corner_radius=0
        )

        self.pack(fill="both", expand=True)

        self._build_left_panel(start_callback)
        self._build_right_panel()

    # ── Left panel ───────────────────────────────────────
    def _build_left_panel(self, start_callback):

        left = ctk.CTkFrame(
            self,
            fg_color=SURFACE,
            corner_radius=0,
            width=480
        )

        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        # top badge
        badge_frame = ctk.CTkFrame(
            left,
            fg_color=BORDER,
            corner_radius=6,
            height=32
        )

        badge_frame.pack(anchor="nw", padx=36, pady=(48, 0))
        badge_frame.pack_propagate(False)

        ctk.CTkLabel(
            badge_frame,
            text="  🌿  ECO TRAVEL ADVISOR  ",
            font=("Arial", 11, "bold"),
            text_color=ACCENT,
            fg_color="transparent"
        ).pack(side="left", padx=8, pady=6)

        # big headline
        ctk.CTkLabel(
            left,
            text="Travel\nResponsibly.",
            font=("Arial", 52, "bold"),
            text_color=TEXT_MAIN,
            justify="left",
            anchor="w"
        ).pack(anchor="w", padx=36, pady=(28, 0))

        # accent underline bar
        accent_bar = ctk.CTkFrame(
            left,
            fg_color=ACCENT,
            height=4,
            width=90,
            corner_radius=2
        )

        accent_bar.pack(anchor="w", padx=36, pady=(10, 0))

        # sub-headline
        ctk.CTkLabel(
            left,
            text=(
                "Your AI-powered companion for\n"
                "low-carbon, sustainable journeys."
            ),
            font=("Arial", 16),
            text_color=TEXT_SUB,
            justify="left",
            anchor="w"
        ).pack(anchor="w", padx=36, pady=(20, 0))

        # feature pills
        features = [
            ("🏨", "Eco-certified hotel recommendations"),
            ("🚆", "Low-carbon transport options"),
            ("📊", "Live carbon footprint estimates"),
            ("🤝", "Human advisor escalation"),
        ]

        feature_frame = ctk.CTkFrame(
            left,
            fg_color="transparent"
        )

        feature_frame.pack(anchor="w", padx=36, pady=(36, 0))

        for icon, label in features:
            row = ctk.CTkFrame(
                feature_frame,
                fg_color=BORDER,
                corner_radius=8,
                height=40
            )

            row.pack(fill="x", pady=5)
            row.pack_propagate(False)

            ctk.CTkLabel(
                row,
                text=f" {icon}  {label}",
                font=("Arial", 13),
                text_color=TEXT_MAIN,
                anchor="w"
            ).pack(side="left", padx=14, pady=0)

        # CTA button
        start_btn = ctk.CTkButton(
            left,
            text="Start Planning  →",
            font=("Arial", 15, "bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_DIM,
            text_color="#0A0E1A",
            height=52,
            width=240,
            corner_radius=10,
            command=start_callback
        )

        start_btn.pack(anchor="w", padx=36, pady=(44, 0))

        # footer note
        ctk.CTkLabel(
            left,
            text="Powered by Rasa · OpenCage · OpenRouteService",
            font=("Arial", 10),
            text_color=TEXT_SUB
        ).pack(anchor="w", padx=36, pady=(16, 48))

    # ── Right panel ──────────────────────────────────────
    def _build_right_panel(self):

        right = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )

        right.pack(side="right", fill="both", expand=True)

        # decorative stat cards
        stats = [
            ("2.4t",  "avg CO₂ saved per trip"),
            ("340+",  "eco-certified hotels"),
            ("1,200", "routes analysed"),
        ]

        ctk.CTkLabel(
            right,
            text="Why eco-travel matters",
            font=("Arial", 13, "bold"),
            text_color=TEXT_SUB
        ).pack(anchor="w", padx=48, pady=(60, 12))

        for value, desc in stats:
            card = ctk.CTkFrame(
                right,
                fg_color=SURFACE,
                corner_radius=12,
                border_width=1,
                border_color=BORDER,
                height=78
            )

            card.pack(fill="x", padx=48, pady=6)
            card.pack_propagate(False)

            ctk.CTkLabel(
                card,
                text=value,
                font=("Arial", 26, "bold"),
                text_color=ACCENT
            ).pack(anchor="w", padx=22, pady=(14, 0))

            ctk.CTkLabel(
                card,
                text=desc,
                font=("Arial", 12),
                text_color=TEXT_SUB
            ).pack(anchor="w", padx=22)

        # decorative glow label
        ctk.CTkLabel(
            right,
            text=(
                "🌍  Every journey is a choice.\n"
                "Make yours count."
            ),
            font=("Arial", 20, "bold"),
            text_color=TEXT_MAIN,
            justify="center"
        ).pack(expand=True)