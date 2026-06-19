import customtkinter as ctk
import requests
import uuid

from cards import (
    HotelCard,
    TransportCard,
    CarbonCard,
    HumanAdvisorCard,
    TripDashboard,
    HOTELS_BY_LEVEL,
    TRANSPORT_META,
)


# ── Palette ──────────────────────────────────────────────
BG          = "#0A0E1A"
SURFACE     = "#0D1B2A"
SURFACE2    = "#111E30"
ACCENT      = "#00D4AA"
ACCENT_DIM  = "#00A882"
TEXT_MAIN   = "#E8F4F1"
TEXT_SUB    = "#7A99A8"
BORDER      = "#1A2744"
USER_BUBBLE = "#1A2744"
BOT_BUBBLE  = "#0D1B2A"
AMBER       = "#F5A623"


class ChatPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.sender_id = str(uuid.uuid4())

        # ── conversation state ────────────────────────────
        self._sustainability = "medium"
        self._transport      = None
        self._distance_km    = None
        self._trip_fields    = {}   # accumulates dashboard data

        self.pack(fill="both", expand=True)

        self._build_topbar()
        self._build_quick_replies()
        self._build_body()          # chat + dashboard side-by-side
        self._build_input_bar()

        self._post_bot_message(
            "Hello! I'm your Sustainable Travel Advisor. 🌍\n"
            "Tell me where you'd like to go and I'll help you plan\n"
            "an eco-friendly journey."
        )

    # ════════════════════════════════════════════════════
    # Layout builders
    # ════════════════════════════════════════════════════

    def _build_topbar(self):

        bar = ctk.CTkFrame(
            self, fg_color=SURFACE, corner_radius=0, height=62
        )
        bar.pack(fill="x")
        bar.pack_propagate(False)

        left = ctk.CTkFrame(bar, fg_color="transparent")
        left.pack(side="left", padx=20, fill="y")

        dot = ctk.CTkFrame(
            left, fg_color=ACCENT, width=10, height=10, corner_radius=5
        )
        dot.pack(side="left")
        dot.pack_propagate(False)

        ctk.CTkLabel(
            left,
            text="  EcoTravel Advisor",
            font=("Arial", 17, "bold"),
            text_color=TEXT_MAIN
        ).pack(side="left")

        ctk.CTkLabel(
            left,
            text="  ·  Online",
            font=("Arial", 12),
            text_color=ACCENT
        ).pack(side="left")

        right = ctk.CTkFrame(bar, fg_color="transparent")
        right.pack(side="right", padx=20, fill="y")

        for chip_text in ["🌿 Eco Mode", "🔒 GDPR Safe"]:
            chip = ctk.CTkFrame(
                right, fg_color=BORDER, corner_radius=6, height=28
            )
            chip.pack(side="right", padx=5)
            chip.pack_propagate(False)

            ctk.CTkLabel(
                chip,
                text=f"  {chip_text}  ",
                font=("Arial", 11),
                text_color=TEXT_SUB
            ).pack(pady=4)

    def _build_quick_replies(self):

        bar = ctk.CTkFrame(
            self, fg_color=SURFACE2, corner_radius=0, height=48
        )
        bar.pack(fill="x")
        bar.pack_propagate(False)

        ctk.CTkLabel(
            bar,
            text="Quick:",
            font=("Arial", 11),
            text_color=TEXT_SUB
        ).pack(side="left", padx=(14, 6))

        quick_replies = [
            ("🌱 Low",       "low"),
            ("🌿 Medium",    "medium"),
            ("🍃 High",      "high"),
            ("🏨 Hotels",    "show me eco friendly hotels"),
            ("🚆 Transport", "show sustainable transport"),
            ("📊 Carbon",    "calculate my carbon footprint"),
            ("🤝 Advisor",   "connect me to a human advisor"),
        ]

        for label, msg in quick_replies:
            ctk.CTkButton(
                bar,
                text=label,
                font=("Arial", 11),
                fg_color=BORDER,
                hover_color=ACCENT_DIM,
                text_color=TEXT_MAIN,
                height=28,
                corner_radius=6,
                command=lambda m=msg: self.quick_message(m)
            ).pack(side="left", padx=3, pady=10)

    def _build_body(self):
        """
        Horizontal split: scrollable chat on left, trip dashboard on right.
        """

        body = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        body.pack(fill="both", expand=True)

        # ── Scrollable chat column ────────────────────────
        self.scroll_frame = ctk.CTkScrollableFrame(
            body,
            fg_color=BG,
            corner_radius=0,
            scrollbar_fg_color=SURFACE,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=ACCENT_DIM
        )
        self.scroll_frame.pack(
            side="left", fill="both", expand=True
        )

        # ── Right dashboard column ────────────────────────
        sidebar = ctk.CTkFrame(
            body,
            fg_color=BG,
            corner_radius=0,
            width=244
        )
        sidebar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        sidebar.pack_propagate(False)

        self.dashboard = TripDashboard(sidebar)
        self.dashboard.pack(fill="x")

    def _build_input_bar(self):

        bar = ctk.CTkFrame(
            self, fg_color=SURFACE, corner_radius=0, height=70
        )
        bar.pack(fill="x")
        bar.pack_propagate(False)

        self.user_input = ctk.CTkEntry(
            bar,
            placeholder_text="Type your message...",
            font=("Arial", 14),
            fg_color=SURFACE2,
            text_color=TEXT_MAIN,
            placeholder_text_color=TEXT_SUB,
            border_color=BORDER,
            border_width=1,
            corner_radius=10,
            height=42
        )
        self.user_input.pack(
            side="left", fill="x", expand=True, padx=(16, 10), pady=14
        )
        self.user_input.bind("<Return>", lambda e: self.send_message())

        ctk.CTkButton(
            bar,
            text="Send  ↵",
            font=("Arial", 13, "bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_DIM,
            text_color="#0A0E1A",
            height=42,
            width=100,
            corner_radius=10,
            command=self.send_message
        ).pack(side="right", padx=(0, 16), pady=14)

    # ════════════════════════════════════════════════════
    # Message bubble helpers
    # ════════════════════════════════════════════════════

    def _post_user_message(self, text: str):

        outer = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        outer.pack(fill="x", pady=4, padx=10)

        bubble = ctk.CTkFrame(outer, fg_color=USER_BUBBLE, corner_radius=12)
        bubble.pack(side="right", padx=(60, 0))

        ctk.CTkLabel(
            bubble,
            text=text,
            font=("Arial", 13),
            text_color=TEXT_MAIN,
            wraplength=480,
            justify="left",
            anchor="w"
        ).pack(padx=14, pady=10)

    def _post_bot_message(self, text: str):

        outer = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        outer.pack(fill="x", pady=4, padx=10)

        avatar = ctk.CTkFrame(
            outer, fg_color=ACCENT, width=28, height=28, corner_radius=14
        )
        avatar.pack(side="left", anchor="n", pady=2)
        avatar.pack_propagate(False)

        ctk.CTkLabel(
            avatar,
            text="E",
            font=("Arial", 12, "bold"),
            text_color="#0A0E1A"
        ).pack(expand=True)

        bubble = ctk.CTkFrame(
            outer,
            fg_color=BOT_BUBBLE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )
        bubble.pack(side="left", padx=(6, 60))

        ctk.CTkLabel(
            bubble,
            text=text,
            font=("Arial", 13),
            text_color=TEXT_MAIN,
            wraplength=520,
            justify="left",
            anchor="w"
        ).pack(padx=14, pady=10)

        self._scroll_to_bottom()

    def _scroll_to_bottom(self):
        self.scroll_frame.after(
            50,
            lambda: self.scroll_frame._parent_canvas.yview_moveto(1.0)
        )

    # ════════════════════════════════════════════════════
    # Rich-card renderers
    # ════════════════════════════════════════════════════

    def _render_hotel_cards(self):
        """
        Render hotel cards for the CURRENT sustainability level.
        Hotels are determined by level, not by parsing bot text.
        """
        hotels = HOTELS_BY_LEVEL.get(self._sustainability, HOTELS_BY_LEVEL["medium"])

        self._post_bot_message(
            f"Here are eco-friendly hotels for your {self._sustainability.capitalize()} "
            f"sustainability preference:"
        )

        for hotel in hotels:
            HotelCard(
                self.scroll_frame,
                hotel_name=hotel,
                sustainability=self._sustainability
            )

        self._scroll_to_bottom()

    def _render_transport_card(self, mode: str):

        TransportCard(self.scroll_frame, transport=mode)
        self._scroll_to_bottom()

    def _render_carbon_card(self, mode: str, emissions_kg: int):

        CarbonCard(
            self.scroll_frame,
            mode=mode,
            emissions_kg=emissions_kg,
            distance_km=self._distance_km
        )
        self._scroll_to_bottom()

    def _render_handover_card(self):

        HumanAdvisorCard(self.scroll_frame)
        self._scroll_to_bottom()

    def _update_dashboard_from_summary(self, text: str):
        """
        Parse Trip Summary text and push all fields to the dashboard.
        Also extracts distance and transport for card use.
        """
        for line in text.split("\n"):
            if ": " not in line:
                continue

            parts = line.split(": ", 1)
            if len(parts) != 2:
                continue

            key, val = parts[0].strip(), parts[1].strip()

            # map actions.py field names → dashboard labels
            mapping = {
                "Origin":                   "Origin",
                "Destination":              "Destination",
                "Distance":                 "Distance",
                "Travel Dates":             "Dates",
                "Budget":                   "Budget",
                "Transport Mode":           "Transport",
                "Sustainability Preference":"Sustainability",
            }

            if key in mapping:
                self._trip_fields[mapping[key]] = val

            # capture distance for CarbonCard
            if key == "Distance":
                try:
                    self._distance_km = float(
                        val.replace(" km", "").replace(",", ".")
                    )
                except ValueError:
                    pass

            # capture transport mode
            if key == "Transport Mode":
                self._transport = val.lower()

        self.dashboard.update_fields(self._trip_fields)

    # ════════════════════════════════════════════════════
    # Core send / receive
    # ════════════════════════════════════════════════════

    def quick_message(self, text: str):
        self.user_input.delete(0, "end")
        self.user_input.insert(0, text)
        self.send_message()

    def send_message(self):

        user_message = self.user_input.get().strip()
        if not user_message:
            return

        self._post_user_message(user_message)
        self.user_input.delete(0, "end")

        # track sustainability from direct user input
        lower = user_message.lower()
        if lower in ("high", "medium", "low"):
            self._sustainability = lower
            self._trip_fields["Sustainability"] = lower.capitalize()
            self.dashboard.update_fields(self._trip_fields)

        try:
            response = requests.post(
                "http://localhost:5005/webhooks/rest/webhook",
                json={"sender": self.sender_id, "message": user_message},
                timeout=10
            )
            bot_messages = response.json()

        except requests.exceptions.ConnectionError:
            self._post_bot_message(
                "⚠️  Cannot reach the Rasa server.\n"
                "Make sure it's running on localhost:5005."
            )
            return

        except Exception as e:
            self._post_bot_message(f"⚠️  Error: {str(e)}")
            return

        for message in bot_messages:

            if "text" not in message:
                continue

            text = message["text"]

            # ── Trip Summary → dashboard + skip chat bubble ──
            if "Trip Summary" in text:
                self._update_dashboard_from_summary(text)
                self._post_bot_message(
                    "✅  Your trip profile is set! Dashboard updated →\n"
                    "You can now ask for hotels, transport, or carbon estimates."
                )
                continue

            # ── Hotels → rich cards (level-driven) ──────────
            if "Recommended Hotels" in text:
                self._render_hotel_cards()
                continue

            # ── Transport → rich card ────────────────────────
            if "Recommended transport:" in text:
                self._post_bot_message(text)
                for mode in ["train", "bus", "car", "flight"]:
                    if mode in text.lower():
                        self._render_transport_card(mode)
                        # update dashboard transport field
                        self._trip_fields["Transport"] = mode.capitalize()
                        self.dashboard.update_fields(self._trip_fields)
                        break
                continue

            # ── Carbon footprint → dedicated card ───────────
            if "Carbon Footprint" in text:
                mode = self._transport or "train"
                for m in ["train", "bus", "car", "flight"]:
                    if m in text.lower():
                        mode = m
                        self._transport = m
                        break

                # extract emissions from bot text e.g. "40 kg CO₂"
                emissions = 0
                for part in text.split():
                    if part.isdigit():
                        emissions = int(part)
                        break

                self._post_bot_message(text)
                self._render_carbon_card(mode, emissions)
                continue

            # ── Human handover → advisor card ───────────────
            if "human travel advisor" in text.lower():
                self._post_bot_message(text)
                self._render_handover_card()
                continue

            # ── Default plain bubble ─────────────────────────
            self._post_bot_message(text)