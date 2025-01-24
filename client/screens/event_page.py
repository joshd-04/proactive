import customtkinter as ctk
import requests, json

from geopy.geocoders import Nominatim
from datetime import datetime
from ..components.navbar import Navbar

from ..components.info_tag import Info_tag
from ..components.event_preview import Event_preview


class EventScreen(ctk.CTkFrame):
    def __init__(self, master, event_id, screen_width, screen_height, API_URL):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.screen_width = screen_width
        self.API_URL = API_URL
        self.active_user = master.active_user
        self.event_id = event_id

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
            self.event_data = self.load_event_data(self.event_id)
            self.pack_event_details()
            self.pack_reviews()
            self.pack_similar_events()

    def load_event_data(self, event_id):
        response = requests.get(f"{self.API_URL}/events/{event_id}")
        return response.json()

    def pack_event_details(self):
        details = ctk.CTkFrame(
            master=self,
            width=0.75 * self.screen_width,
            height=300,
            fg_color=("white", "black"),
        )
        details.propagate(False)

        left_container = ctk.CTkFrame(
            master=details,
            width=0.5 * self.screen_width,
            height=300,
            fg_color="transparent",
        )
        right_container = ctk.CTkFrame(
            master=details,
            width=0.35 * self.screen_width,
            height=300,
            fg_color="transparent",
        )

        # Title
        title_label = ctk.CTkLabel(
            master=left_container,
            text=self.event_data["title"],
            font=("Arial", 32, "bold"),
        )
        title_label.pack(anchor="nw")

        # Info tags
        tags_frame = ctk.CTkFrame(
            master=left_container,
            fg_color="transparent",
            width=0.75 * self.screen_width,
        )
        sport_tag = Info_tag(master=tags_frame, text=self.event_data["sport"])

        date_str = self.event_data["date_time"]
        date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
        formatted_date = f"{date.day}/{date.month}/{date.year}"

        date_tag = Info_tag(master=tags_frame, text=formatted_date)
        spaces_left_tag = Info_tag(
            master=tags_frame,
            text=f"{self.event_data["spaces_left"]}/{self.event_data["max_participants"]} spaces left",
        )

        sport_tag.pack(side="left")
        date_tag.pack(side="left", padx=20)
        spaces_left_tag.pack(side="left")

        tags_frame.pack(anchor="nw", pady=20)

        # Description
        description_label = ctk.CTkLabel(
            master=left_container, text="Description", font=("Arial", 24, "bold")
        )
        description_body = ctk.CTkLabel(
            master=left_container,
            text=self.event_data["description"],
            font=("Arial", 20),
            wraplength=0.4 * self.screen_width,
        )

        description_label.pack(pady=(5, 5), anchor="nw")
        description_body.pack(anchor="nw")

        # Address
        # Find address via reverse geocoding
        geolocator = Nominatim(user_agent="location_tkinter")
        location = geolocator.reverse(self.event_data["location"])

        address_label = ctk.CTkLabel(
            master=right_container,
            text=f"Location: {location}",
            font=("Arial", 20, "bold"),
        )
        address_label.pack(anchor="nw")

        # Event creator
        event_creator_label = ctk.CTkLabel(
            master=right_container,
            text=f"Event creator: {self.event_data["event_creator"]}",
            font=("Arial", 20, "bold"),
        )

        event_creator_label.pack(anchor="nw")

        # If event is upcoming, give a participate button
        epoch = date.timestamp()
        current_epoch = datetime.now().timestamp()

        if current_epoch < epoch:
            participate_btn = ctk.CTkButton(
                master=right_container,
                text="Participate",
                font=("Arial", 24, "bold"),
                text_color=("white", "black"),
            )
            participate_btn.pack(pady=10, anchor="nw")

        else:
            pass
            # This will be filled at a later sprint when review endpoints are made
            # Otherwise give option to write a review

            # if they have written a review, show the review

        # Pack containers
        left_container.pack(side="left", anchor="n")
        right_container.pack(side="left", anchor="n", pady=(50, 0))
        details.pack(pady=(100, 20))

    def pack_reviews(self):
        # Will be filled at a later sprint when review endpoints are made
        pass

    def pack_similar_events(self):
        response = requests.get(
            f"{self.API_URL}/events/{self.event_id}/similar-events?quantity=5"
        )

        similar_events_frame = ctk.CTkFrame(
            master=self,
            width=0.75 * self.screen_width,
            fg_color="transparent",
        )

        similar_events_label = ctk.CTkLabel(
            master=similar_events_frame, text="Similar events:", font=("Arial", 24)
        )
        events_container = ctk.CTkFrame(
            master=similar_events_frame, width=0.75 * self.screen_width, height=300
        )
        events_container.propagate(False)

        data = response.json()
        for event in data:
            date_str = event["date_time"]
            date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
            formatted_date = f"{date.day}/{date.month}/{date.year}"

            Event_preview(
                app_master=self.master,
                master=events_container,
                event_id=event["event_id"],
                event_title=event["title"],
                sport=event["sport"],
                date_string=formatted_date,
                max_participants=event["max_participants"],
            ).pack(side="left")

        if len(data) == 0:
            no_data_label = ctk.CTkLabel(
                master=events_container,
                text="No nearby similar events found!",
                font=("Arial", 20, "italic"),
            )
            no_data_label.pack(side="left")

        similar_events_label.pack(anchor="nw")
        events_container.pack()
        similar_events_frame.pack()
