import customtkinter as ctk
import requests, json

from datetime import datetime
from ..components.navbar import Navbar

from ..components.info_tag import Info_tag
from ..components.event_preview import Event_preview


class HomeScreen(ctk.CTkFrame):
    def __init__(self, master, screen_width, screen_height, API_URL):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.screen_width = screen_width
        self.API_URL = API_URL
        self.active_user = master.active_user

        if not self.active_user:
            error_label = ctk.CTkLabel(
                master=self,
                text="You need to be signed in. This is a protected page.",
                font=("Arial", 48, "bold"),
                text_color="red",
            )
            error_label.pack(pady=100)
        else:

            # Important components
            proactive_label = ctk.CTkLabel(
                master=self,
                text="ProActive",
                font=("Arial", 32, "bold"),
                text_color=("black", "white"),
            )

            proactive_label.place(relx=0.03, rely=0.04)

            navbar = Navbar(master=self, screen_width=screen_width)
            navbar.activate_button(0)

            self.get_last_event()
            self.get_next_event()
            self.get_recommended_events()
            self.pack_top_frame()
            self.pack_recommended_events()

    def pack_top_frame(self):
        # Body components
        top_frame_width = self.screen_width - 200
        top_frame = ctk.CTkFrame(
            master=self, width=top_frame_width, height=370, fg_color="transparent"
        )

        last_event_frame = ctk.CTkFrame(
            master=top_frame,
            width=top_frame_width / 2 - 5,
            height=300,
            fg_color="transparent",
        )

        # Stop the frame from resizing to fit its children
        last_event_frame.pack_propagate(False)

        last_event_caption = ctk.CTkLabel(
            master=last_event_frame, text="Your last event:", font=("Arial", 24)
        )

        # Contains event info
        last_event_info_frame = ctk.CTkFrame(
            master=last_event_frame,
            width=top_frame_width / 4,
            height=250,
            fg_color="white",
        )
        last_event_info_frame.pack_propagate(False)

        # Contains action buttons
        last_event_actions_frame = ctk.CTkFrame(
            master=last_event_frame,
            width=top_frame_width / 4,
            height=250,
            fg_color="white",
        )
        last_event_actions_frame.pack_propagate(False)

        # Make the components
        if self.last_event:
            last_event_title = ctk.CTkLabel(
                master=last_event_info_frame,
                text=self.last_event["title"],
                font=("Arial", 20, "bold"),
            )

            date_str = self.last_event["date_time"]
            date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
            formatted_date = f"{date.day}/{date.month}/{date.year}"

            sport_label = Info_tag(last_event_info_frame, self.last_event["sport"])
            date_label = Info_tag(last_event_info_frame, formatted_date)
            participants_label = Info_tag(
                last_event_info_frame,
                f"{self.last_event["participant_count"]} people attended",
            )
            distance_label = Info_tag(
                last_event_info_frame,
                f"{self.last_event["distance_from_home_km"]} km away",
            )

            details_btn_last = ctk.CTkButton(
                master=last_event_actions_frame,
                text=" View details ",
                text_color="white",
                font=("Arial", 24),
                fg_color="#00AAFF",
                height=50,
                corner_radius=10,
                command=lambda: self.master.showScreen(
                    "eventScreen", event_id=self.last_event["event_id"]
                ),
            )

            review_btn = ctk.CTkButton(
                master=last_event_actions_frame,
                text=" Write a review ",
                text_color="white",
                font=("Arial", 24),
                fg_color="#00AAFF",
                height=50,
                corner_radius=10,
            )

            # Pack last event info
            last_event_title.pack(padx=10, pady=10, anchor="w")
            sport_label.pack(padx=10, pady=5, anchor="w")
            date_label.pack(padx=10, pady=5, anchor="w")
            participants_label.pack(padx=10, pady=5, anchor="w")
            distance_label.pack(padx=10, pady=5, anchor="w")

            # Pack last event buttons
            details_btn_last.pack(pady=10, anchor="w")
            review_btn.pack(pady=10, anchor="w")
        else:
            no_last_event_label = ctk.CTkLabel(
                master=last_event_info_frame,
                text="No previous event participation history found",
                wraplength=200,
                font=("Arial", 20, "italic"),
            )
            no_last_event_label.pack(anchor="w")

        # Pack last event components
        last_event_caption.pack(anchor="nw")
        last_event_info_frame.pack(side="left")
        last_event_actions_frame.pack(side="left")

        # Pack last event frame
        last_event_frame.pack(side="left", padx=(0, 5))

        next_event_frame = ctk.CTkFrame(
            master=top_frame,
            width=top_frame_width / 2 - 5,
            height=300,
            fg_color="transparent",
        )
        next_event_frame.pack(side="left", padx=(5, 0))
        # Stop the frame from resizing to fit its children
        next_event_frame.pack_propagate(False)

        next_event_caption = ctk.CTkLabel(
            master=next_event_frame, text="Your next event:", font=("Arial", 24)
        )

        # Contains event info
        next_event_info_frame = ctk.CTkFrame(
            master=next_event_frame,
            width=top_frame_width / 4,
            height=250,
            fg_color="white",
        )
        next_event_info_frame.pack_propagate(False)

        # Contains action buttons
        next_event_actions_frame = ctk.CTkFrame(
            master=next_event_frame,
            width=top_frame_width / 4,
            height=250,
            fg_color="white",
        )
        next_event_actions_frame.pack_propagate(False)

        # Make the components
        if self.next_event:
            next_event_title = ctk.CTkLabel(
                master=next_event_info_frame,
                text=self.next_event["title"],
                font=("Arial", 20, "bold"),
            )

            date_str = self.next_event["date_time"]
            date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
            formatted_date = f"{date.day}/{date.month}/{date.year}"

            sport_label = Info_tag(next_event_info_frame, self.next_event["sport"])
            date_label = Info_tag(next_event_info_frame, formatted_date)
            participants_label = Info_tag(
                next_event_info_frame,
                f"{self.next_event["spaces_left"]}/{self.next_event["max_participants"]} spaces left",
            )
            distance_label = Info_tag(
                next_event_info_frame,
                f"{self.next_event["distance_from_home_km"]} km away",
            )

            details_btn_next = ctk.CTkButton(
                master=next_event_actions_frame,
                text=" View details ",
                text_color="white",
                font=("Arial", 24),
                fg_color="#00AAFF",
                height=50,
                corner_radius=10,
                command=lambda: self.master.showScreen(
                    "eventScreen", event_id=self.next_event["event_id"]
                ),
            )

            # Pack next event info
            next_event_title.pack(padx=10, pady=10, anchor="w")
            sport_label.pack(padx=10, pady=5, anchor="w")
            date_label.pack(padx=10, pady=5, anchor="w")
            participants_label.pack(padx=10, pady=5, anchor="w")
            distance_label.pack(padx=10, pady=5, anchor="w")

            # Pack next event buttons
            details_btn_next.pack(pady=10, anchor="w")
        else:
            no_next_event_label = ctk.CTkLabel(
                master=next_event_info_frame,
                text="No upcoming event participation found",
                wraplength=200,
                font=("Arial", 20, "italic"),
            )
            no_next_event_label.pack(anchor="w")

        # Pack next event components
        next_event_caption.pack(anchor="nw")
        next_event_info_frame.pack(side="left")
        next_event_actions_frame.pack(side="left")

        # Pack next event frame
        next_event_frame.pack(side="left", padx=(0, 5))

        top_frame.pack(pady=(120, 30))

    def pack_recommended_events(self):
        section_width = self.screen_width - 200
        section_frame = ctk.CTkFrame(
            master=self, width=section_width, height=370, fg_color="transparent"
        )

        section_label = ctk.CTkLabel(
            master=section_frame, text="Recommended events:", font=("Arial", 24)
        )

        events_frame = ctk.CTkFrame(
            master=section_frame, width=section_width, height=320
        )
        events_frame.propagate(False)

        section_label.pack(anchor="w")

        for event in self.recommended_events:
            date_str = event["date_time"]
            date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
            formatted_date = f"{date.day}/{date.month}/{date.year}"

            eventUI = Event_preview(
                master=events_frame,
                app_master=self.master,
                event_id=event["event_id"],
                event_title=event["title"],
                sport=event["sport"],
                date_string=formatted_date,
                spaces_left=event["spaces_left"],
                max_participants=event["max_participants"],
                distance_km=event["distance_from_home_km"],
            )
            eventUI.pack(side="left", padx=10)

        events_frame.pack()
        section_frame.pack()

    def get_last_event(self):
        username = self.active_user["username"]
        response = requests.get(f"{self.API_URL}/user/{username}/last-event")

        # Convert the JSON response into a python dictionary
        data = response.json()
        self.last_event = data

    def get_next_event(self):
        username = self.active_user["username"]
        response = requests.get(f"{self.API_URL}/user/{username}/next-event")

        # Convert the JSON response into a python dictionary
        data = response.json()
        self.next_event = data

    def get_recommended_events(self):
        username = self.active_user["username"]
        # We want 5 events as we only display 5 events
        response = requests.get(
            f"{self.API_URL}/user/{username}/recommended-events?amount=5"
        )

        # Convert the JSON response into a python dictionary
        data = response.json()
        self.recommended_events = data
