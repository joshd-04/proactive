from datetime import datetime
import customtkinter as ctk
import requests

from client.components.event_preview import Event_preview
from client.components.navbar import Navbar


class SearchScreen(ctk.CTkFrame):
    def __init__(self, master, screen_width, screen_height, API_URL):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.screen_width = screen_width
        self.API_URL = API_URL
        # master.active_user = {
        #     "username": "test",
        #     "password_hash": "96f77deda882527d6f3142513324eafa47b71d845bef9c839082d738e49b59f9",
        #     "access_level": "normal",
        #     "first_name": "mo",
        #     "last_name": "salah",
        #     "age": 32,
        #     "home_location": "(-0.12770540128798905,51.5034927)",
        # }
        self.active_user = master.active_user

        self.search_results = []

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
            navbar.activate_button(1)

            searchFrame = ctk.CTkFrame(master=self, fg_color="transparent")

            self.searchEntry = ctk.CTkEntry(
                master=searchFrame,
                width=0.5 * screen_width,
                font=("Arial", 32),
                placeholder_text="Search",
                fg_color=("white", "black"),
            )

            searchSubmit = ctk.CTkButton(
                master=searchFrame,
                width=100,
                font=("Arial", 32),
                text="Go",
                command=self.fetch_search_results,
            )

            self.searchEntry.grid(row=0, column=0)
            searchSubmit.grid(row=0, column=1, padx=20)

            searchFrame.pack(pady=(100, 50))

    def pack_search_results(self):
        section_width = self.screen_width - 200
        self.section_frame = ctk.CTkFrame(
            master=self, width=section_width, height=370, fg_color="transparent"
        )

        section_label = ctk.CTkLabel(
            master=self.section_frame, text="Results:", font=("Arial", 24)
        )

        self.events_frame = ctk.CTkFrame(
            master=self.section_frame, width=section_width, height=320
        )
        self.events_frame.propagate(False)

        section_label.pack(anchor="w")

        for event in self.search_results:
            date_str = event["date_time"]
            date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
            formatted_date = f"{date.day}/{date.month}/{date.year}"

            eventUI = Event_preview(
                master=self.events_frame,
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

        self.events_frame.pack()
        self.section_frame.pack()

    def unpack_search_results(self):
        self.events_frame.destroy()
        self.section_frame.destroy()

    def fetch_search_results(self):
        query = self.searchEntry.get()
        if query == "":
            pass
        else:
            # Replace spaces with a plus symbol
            query.replace(" ", "+")
            response = requests.get(
                f"{self.API_URL}/events/search?username={self.active_user["username"]}&query={query}&quantity=5"
            )
            events = response.json()
            self.search_results = events
            try:
                self.unpack_search_results()
            except:
                pass
            finally:
                self.pack_search_results()
