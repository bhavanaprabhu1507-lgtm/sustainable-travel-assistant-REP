import customtkinter as ctk


# ── Palette ──────────────────────────────────────────────
BG          = "#0A0E1A"
SURFACE     = "#0D1B2A"
SURFACE2    = "#111E30"
ACCENT      = "#00D4AA"
TEXT_MAIN   = "#E8F4F1"
TEXT_SUB    = "#7A99A8"
BORDER      = "#1A2744"
GREEN       = "#00D4AA"
AMBER       = "#F5A623"
RED         = "#E74C4C"


# ── Hotel metadata keyed by name ─────────────────────────
HOTEL_META = {
    "Eco Green Resort":    {"price": "€120/night", "carbon": "Low",    "cert": "Green Key"},
    "Sustainable Suites":  {"price": "€145/night", "carbon": "Low",    "cert": "EU Ecolabel"},
    "Nature Stay Hotel":   {"price": "€98/night",  "carbon": "Low",    "cert": "Green Globe"},
    "Green Comfort Hotel": {"price": "€85/night",  "carbon": "Medium", "cert": "EarthCheck"},
    "Eco Lodge":           {"price": "€70/night",  "carbon": "Medium", "cert": "Green Key"},
    "City Green Inn":      {"price": "€95/night",  "carbon": "Medium", "cert": "ISO 14001"},
    "Budget Stay":         {"price": "€45/night",  "carbon": "High",   "cert": "None"},
    "Travel Inn":          {"price": "€55/night",  "carbon": "High",   "cert": "None"},
    "City Hotel":          {"price": "€65/night",  "carbon": "High",   "cert": "None"},
}

# ── Transport metadata ───────────────────────────────────
TRANSPORT_META = {
    "train":  {"price": "€50",  "green_score": "95/100", "emissions": 40,  "sustainability": "high"},
    "bus":    {"price": "€25",  "green_score": "78/100", "emissions": 60,  "sustainability": "medium"},
    "car":    {"price": "€110", "green_score": "42/100", "emissions": 120, "sustainability": "low"},
    "flight": {"price": "€180", "green_score": "18/100", "emissions": 250, "sustainability": "low"},
}

# ── Hotels per sustainability level ──────────────────────
HOTELS_BY_LEVEL = {
    "high":   ["Eco Green Resort",    "Sustainable Suites",  "Nature Stay Hotel"],
    "medium": ["Green Comfort Hotel", "Eco Lodge",           "City Green Inn"],
    "low":    ["Budget Stay",         "Travel Inn",          "City Hotel"],
}

# ── Transport icons ──────────────────────────────────────
TRANSPORT_ICONS = {
    "train":  "🚆",
    "bus":    "🚌",
    "car":    "🚗",
    "flight": "✈️",
}


def _carbon_color(level: str) -> str:
    """Green = low carbon / high sustainability, Red = high carbon / low sustainability."""
    mapping = {
        "high":   GREEN,   # high sustainability → green
        "medium": AMBER,
        "low":    RED,     # low sustainability → red
    }
    return mapping.get(level.lower(), AMBER)


def _carbon_label_color(carbon_label: str) -> str:
    """Colour based on carbon score label (Low / Medium / High)."""
    mapping = {
        "low":    GREEN,
        "medium": AMBER,
        "high":   RED,
    }
    return mapping.get(carbon_label.lower(), AMBER)


# ════════════════════════════════════════════════════════
class HotelCard(ctk.CTkFrame):
    """
    Rich hotel card with price, carbon score, and certification.

    Parameters
    ----------
    parent        : parent widget
    hotel_name    : name string (looked up in HOTEL_META)
    sustainability: 'high' | 'medium' | 'low'  — drives left bar colour
    """

    def __init__(
        self,
        parent,
        hotel_name: str,
        sustainability: str = "medium"
    ):

        super().__init__(
            parent,
            fg_color=SURFACE2,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        self.pack(fill="x", padx=12, pady=5)

        glow = _carbon_color(sustainability)
        meta = HOTEL_META.get(hotel_name, {
            "price": "N/A",
            "carbon": sustainability.capitalize(),
            "cert":  "N/A"
        })
        carbon_glow = _carbon_label_color(meta["carbon"])

        # ── Left colour bar ──────────────────────────────
        ctk.CTkFrame(
            self,
            fg_color=glow,
            width=5,
            corner_radius=4
        ).pack(side="left", fill="y", pady=8)

        # ── Content ──────────────────────────────────────
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=14, pady=10)

        # Row 1: icon + name + sustainability badge
        top = ctk.CTkFrame(content, fg_color="transparent")
        top.pack(fill="x")

        ctk.CTkLabel(
            top,
            text="🏨",
            font=("Arial", 18),
            text_color=glow
        ).pack(side="left")

        ctk.CTkLabel(
            top,
            text=f"  {hotel_name}",
            font=("Arial", 15, "bold"),
            text_color=TEXT_MAIN
        ).pack(side="left")

        badge = ctk.CTkFrame(top, fg_color=glow, corner_radius=5, height=22)
        badge.pack(side="right")
        badge.pack_propagate(False)

        ctk.CTkLabel(
            badge,
            text=f"  {sustainability.upper()}  ",
            font=("Arial", 10, "bold"),
            text_color="#0A0E1A"
        ).pack(pady=3)

        # Row 2: detail chips
        detail_row = ctk.CTkFrame(content, fg_color="transparent")
        detail_row.pack(fill="x", pady=(8, 0))

        chips = [
            ("💰", meta["price"],           TEXT_SUB),
            ("🌍", f"Carbon: {meta['carbon']}", carbon_glow),
            ("🏅", f"Cert: {meta['cert']}",  TEXT_SUB),
        ]

        for icon, label, colour in chips:
            chip = ctk.CTkFrame(
                detail_row,
                fg_color=BORDER,
                corner_radius=6,
                height=26
            )

            chip.pack(side="left", padx=(0, 6))
            chip.pack_propagate(False)

            ctk.CTkLabel(
                chip,
                text=f"  {icon} {label}  ",
                font=("Arial", 11),
                text_color=colour
            ).pack(pady=4)


# ════════════════════════════════════════════════════════
class TransportCard(ctk.CTkFrame):
    """
    Rich transport card with emissions, price, and green score.

    Parameters
    ----------
    parent   : parent widget
    transport: mode string e.g. 'Train'
    """

    def __init__(self, parent, transport: str):

        super().__init__(
            parent,
            fg_color=SURFACE2,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        self.pack(fill="x", padx=12, pady=5)

        key  = transport.lower()
        meta = TRANSPORT_META.get(key, {
            "price": "N/A", "green_score": "N/A",
            "emissions": 0, "sustainability": "medium"
        })

        glow = _carbon_color(meta["sustainability"])
        icon = TRANSPORT_ICONS.get(key, "🚀")

        # ── Left colour bar ──────────────────────────────
        ctk.CTkFrame(
            self,
            fg_color=glow,
            width=5,
            corner_radius=4
        ).pack(side="left", fill="y", pady=8)

        # ── Content ──────────────────────────────────────
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=14, pady=10)

        # Row 1: icon + name + sustainability badge
        top = ctk.CTkFrame(content, fg_color="transparent")
        top.pack(fill="x")

        ctk.CTkLabel(
            top,
            text=icon,
            font=("Arial", 18),
            text_color=glow
        ).pack(side="left")

        ctk.CTkLabel(
            top,
            text=f"  {transport.capitalize()}",
            font=("Arial", 15, "bold"),
            text_color=TEXT_MAIN
        ).pack(side="left")

        badge = ctk.CTkFrame(top, fg_color=glow, corner_radius=5, height=22)
        badge.pack(side="right")
        badge.pack_propagate(False)

        ctk.CTkLabel(
            badge,
            text=f"  {meta['sustainability'].upper()}  ",
            font=("Arial", 10, "bold"),
            text_color="#0A0E1A"
        ).pack(pady=3)

        # Row 2: detail chips
        detail_row = ctk.CTkFrame(content, fg_color="transparent")
        detail_row.pack(fill="x", pady=(8, 0))

        chips = [
            ("🌍", f"Carbon: {meta['emissions']} kg CO₂", glow),
            ("💰", f"Price: {meta['price']}",             TEXT_SUB),
            ("🌿", f"Green Score: {meta['green_score']}", GREEN),
        ]

        for icon_c, label, colour in chips:
            chip = ctk.CTkFrame(
                detail_row,
                fg_color=BORDER,
                corner_radius=6,
                height=26
            )

            chip.pack(side="left", padx=(0, 6))
            chip.pack_propagate(False)

            ctk.CTkLabel(
                chip,
                text=f"  {icon_c} {label}  ",
                font=("Arial", 11),
                text_color=colour
            ).pack(pady=4)


# ════════════════════════════════════════════════════════
class CarbonCard(ctk.CTkFrame):
    """
    Dedicated carbon footprint estimate card.

    Parameters
    ----------
    parent      : parent widget
    mode        : transport mode string
    distance_km : distance in km (optional)
    emissions_kg: CO₂ in kg
    """

    def __init__(
        self,
        parent,
        mode: str,
        emissions_kg: int,
        distance_km: float = None
    ):

        super().__init__(
            parent,
            fg_color=SURFACE2,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        self.pack(fill="x", padx=12, pady=6)

        meta = TRANSPORT_META.get(mode.lower(), {"sustainability": "medium"})
        glow = _carbon_color(meta["sustainability"])

        # left bar
        ctk.CTkFrame(
            self,
            fg_color=glow,
            width=5,
            corner_radius=4
        ).pack(side="left", fill="y", pady=8)

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=14, pady=12)

        # header
        ctk.CTkLabel(
            content,
            text="🌍  Carbon Estimate",
            font=("Arial", 14, "bold"),
            text_color=ACCENT,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkFrame(
            content,
            fg_color=BORDER,
            height=1
        ).pack(fill="x", pady=(6, 8))

        # fields
        fields = {"Mode": mode.capitalize()}

        if distance_km:
            fields["Distance"] = f"{distance_km} km"

        fields["Estimated CO₂"] = f"{emissions_kg} kg"

        grid = ctk.CTkFrame(content, fg_color="transparent")
        grid.pack(anchor="w")

        for i, (label, value) in enumerate(fields.items()):

            ctk.CTkLabel(
                grid,
                text=label,
                font=("Arial", 11),
                text_color=TEXT_SUB,
                width=110,
                anchor="w"
            ).grid(row=i, column=0, sticky="w", pady=2)

            ctk.CTkLabel(
                grid,
                text=value,
                font=("Arial", 11, "bold"),
                text_color=glow,
                anchor="w"
            ).grid(row=i, column=1, sticky="w", padx=(8, 0), pady=2)


# ════════════════════════════════════════════════════════
class HumanAdvisorCard(ctk.CTkFrame):
    """
    Human handover card with action button.
    """

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#1A1000",
            corner_radius=12,
            border_width=1,
            border_color=AMBER
        )

        self.pack(fill="x", padx=12, pady=6)

        # left amber bar
        ctk.CTkFrame(
            self,
            fg_color=AMBER,
            width=5,
            corner_radius=4
        ).pack(side="left", fill="y", pady=8)

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=14, pady=12)

        # header row
        top = ctk.CTkFrame(content, fg_color="transparent")
        top.pack(fill="x")

        ctk.CTkLabel(
            top,
            text="⚠  Human Advisor Required",
            font=("Arial", 14, "bold"),
            text_color=AMBER
        ).pack(side="left")

        # status chips
        chips_row = ctk.CTkFrame(content, fg_color="transparent")
        chips_row.pack(fill="x", pady=(8, 0))

        for chip_text in ["✅ Trip details prepared", "📋 Conversation exported"]:
            chip = ctk.CTkFrame(
                chips_row,
                fg_color=BORDER,
                corner_radius=6,
                height=26
            )

            chip.pack(side="left", padx=(0, 8))
            chip.pack_propagate(False)

            ctk.CTkLabel(
                chip,
                text=f"  {chip_text}  ",
                font=("Arial", 11),
                text_color=TEXT_SUB
            ).pack(pady=4)

        # contact button
        ctk.CTkButton(
            content,
            text="📞  Contact Advisor",
            font=("Arial", 12, "bold"),
            fg_color=AMBER,
            hover_color="#C0820F",
            text_color="#0A0E1A",
            height=34,
            width=160,
            corner_radius=8,
            command=lambda: None  # wired to handover action if needed
        ).pack(anchor="w", pady=(10, 0))


# ════════════════════════════════════════════════════════
class TripDashboard(ctk.CTkFrame):
    """
    Persistent side dashboard showing trip summary fields.
    Updated via update_fields(dict).
    """

    _FIELD_ORDER = [
        "Origin",
        "Destination",
        "Distance",
        "Dates",
        "Budget",
        "Transport",
        "Sustainability",
    ]

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color=SURFACE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER,
            width=220
        )

        self.pack_propagate(False)

        # header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=14, pady=(14, 8))

        ctk.CTkLabel(
            hdr,
            text="🗺  Trip Summary",
            font=("Arial", 13, "bold"),
            text_color=ACCENT
        ).pack(anchor="w")

        ctk.CTkFrame(
            self,
            fg_color=BORDER,
            height=1
        ).pack(fill="x", padx=14)

        # field rows
        self._labels = {}
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="x", padx=14, pady=10)

        for i, field in enumerate(self._FIELD_ORDER):

            ctk.CTkLabel(
                grid,
                text=field,
                font=("Arial", 10),
                text_color=TEXT_SUB,
                anchor="w",
                width=90
            ).grid(row=i, column=0, sticky="w", pady=4)

            val_label = ctk.CTkLabel(
                grid,
                text="—",
                font=("Arial", 10, "bold"),
                text_color=TEXT_MAIN,
                anchor="w",
                wraplength=110
            )

            val_label.grid(row=i, column=1, sticky="w", padx=(6, 0), pady=4)
            self._labels[field] = val_label

    def update_fields(self, data: dict):
        """
        Pass a dict like {"Origin": "Madrid", "Destination": "Turin", ...}
        to update visible values.
        """
        for key, val in data.items():
            if key in self._labels:
                colour = ACCENT if key == "Distance" else TEXT_MAIN
                self._labels[key].configure(
                    text=str(val),
                    text_color=colour
                )