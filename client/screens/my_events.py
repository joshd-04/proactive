from datetime import datetime
import customtkinter as ctk
import requests

from client.components.event_preview import Event_preview

from ..components.navbar import Navbar


class MyEventsScreen(ctk.CTkFrame):
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

        # user_1   | MyRandomPasswordhash! | normal       | Jessica    | Rodriguez |  58 | (70,-90)
        # master.active_user = {
        #     "username": "user_1",
        #     "password_hash": "MyRandomPasswordhash",
        #     "access_level": "normal",
        #     "first_name": "Jessica",
        #     "last_name": "Rodriguez",
        #     "age": 58,
        #     "home_location": "(70,-90)",
        # }

        # user_23  | MyRandomPasswordhash! | normal       | Richard    | Garcia    |  38 | (-13,-4)
        master.active_user = {
            "username": "user_23",
            "password_hash": "MyRandomPasswordhash",
            "access_level": "normal",
            "first_name": "Richard",
            "last_name": "Garcia",
            "age": 38,
            "home_location": "(-13,-4)",
        }

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
            navbar.activate_button(2)

            # Event type selection
            top_bar = ctk.CTkFrame(
                master=self, fg_color="transparent", width=self.screen_width
            )
            title_frame = ctk.CTkFrame(master=top_bar, fg_color="transparent")

            title_label = ctk.CTkLabel(
                master=title_frame, text="Your events:", font=("Arial", 20)
            )

            dropdown = ctk.CTkOptionMenu(
                master=title_frame,
                values=[
                    "-- select --",
                    "Created by me (past)",
                    "Created by me (upcoming)",
                    "Participated (past)",
                    "Participating (future)",
                ],
                fg_color="lightgrey",
                button_color="lightgrey",
                button_hover_color="grey",
                font=("Arial", 20),
                text_color="black",
                corner_radius=20,
                command=self.handle_filter_change,
            )
            title_label.pack(side="left")
            dropdown.pack(side="left", padx=20)

            create_event_btn = ctk.CTkButton(
                master=top_bar,
                text=" Create event ",
                height=40,
                corner_radius=10,
                fg_color="lime",
                hover_color="lightgreen",
                font=("Arial", 20, "bold"),
                command=lambda: self.master.showScreen("createEventScreen"),
            )

            title_frame.pack(anchor="nw")
            create_event_btn.pack(anchor="ne")

            top_bar.pack(pady=(150, 50), padx=100, anchor="w", fill="both")

            ## Event handling:
            self.fetch_event_data()

    def pack_events(self, option_menu_filter):
        if self.focused_events == None:
            return

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

        for event in self.focused_events:
            date_str = event["date_time"]
            date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
            formatted_date = f"{date.day}/{date.month}/{date.year}"

            if option_menu_filter == "Created by me (past)":
                # To calculate the event's average rating
                ## 1. Get all reviews from API
                ## 2. Calculate mean of ratings

                response = requests.get(
                    f"{self.API_URL}/reviews?event_id={event["event_id"]}"
                )
                reviews = response.json()

                if len(reviews) == 0:
                    avg_rating = -1
                else:
                    total_rating = 0
                    for review in reviews:
                        total_rating += float(review["rating"])

                avg_rating = round(total_rating / len(reviews), 1)

                eventUI = Event_preview(
                    master=self.events_frame,
                    app_master=self.master,
                    event_id=event["event_id"],
                    event_title=event["title"],
                    sport=event["sport"],
                    date_string=formatted_date,
                    participant_count=event["participant_count"],
                    distance_km=event["distance_from_home_km"],
                    avg_rating=avg_rating,
                )
            elif option_menu_filter == "Created by me (upcoming)":

                def delete_event_command(event_id, username):
                    requests.delete(
                        f"{self.API_URL}/events/{event_id}?username={username}"
                    )
                    self.master.showScreen("myEventsScreen")

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
                    show_delete_btn=True,
                    delete_command=lambda: delete_event_command(
                        event["event_id"], self.active_user["username"]
                    ),
                )
            elif option_menu_filter == "Participated (past)":
                # Fetch the user's review
                response = requests.get(
                    f"{self.API_URL}/reviews?username={self.active_user["username"]}&event_id={event["event_id"]}"
                )
                review_data = response.json()
                if len(review_data) == 0:
                    # If the user hasn't written a review
                    # Negative rating indicates "write review" button should be shown
                    rating = -1
                else:
                    rating = review_data[0]["rating"]
                eventUI = Event_preview(
                    master=self.events_frame,
                    app_master=self.master,
                    event_id=event["event_id"],
                    event_title=event["title"],
                    sport=event["sport"],
                    date_string=formatted_date,
                    distance_km=event["distance_from_home_km"],
                    participant_count=event["participant_count"],
                    users_rating=rating,
                )

            elif option_menu_filter == "Participating (future)":
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

        if len(self.focused_events) == 0:
            no_data_label = ctk.CTkLabel(
                master=self.events_frame,
                text="No data found",
                font=("Arial", 20, "italic"),
            )
            no_data_label.pack(side="left")

        self.events_frame.pack()
        self.section_frame.pack()

    def unpack_events(self):
        self.events_frame.destroy()
        self.section_frame.destroy()

    def fetch_event_data(self):
        # To be run once, when the myevents page first loads
        request = f"{self.API_URL}/user/{self.active_user["username"]}/events"
        response = requests.get(request)
        data = response.json()
        self.events_data = data

    def filter_data(self, option_menu_filter):
        # Only run if the data has been fetched
        if self.events_data == None:
            return None

        # These two variables will store the flags that represent the data we want
        created_by_me_wanted = None
        upcoming_wanted = None

        if option_menu_filter == "-- select --":
            return None

        if option_menu_filter == "Created by me (past)":
            created_by_me_wanted = True
            upcoming_wanted = False

        if option_menu_filter == "Created by me (upcoming)":
            created_by_me_wanted = True
            upcoming_wanted = True

        if option_menu_filter == "Participated (past)":
            created_by_me_wanted = False
            upcoming_wanted = False

        if option_menu_filter == "Participating (future)":
            created_by_me_wanted = False
            upcoming_wanted = True

        # Loop over the data we have, and extract the data denoted by the wanted flags
        requested_data = None
        for data_set in self.events_data:
            if (
                data_set["upcoming"] == upcoming_wanted
                and data_set["created_by_me"] == created_by_me_wanted
            ):
                requested_data = data_set["events"]

        return requested_data

    def handle_filter_change(self, new_option_menu_filter):
        try:
            self.unpack_events()
        except:
            pass
        finally:
            data = self.filter_data(option_menu_filter=new_option_menu_filter)
            # Focused_events will store the events we are currently interested in
            self.focused_events = data
            self.pack_events(option_menu_filter=new_option_menu_filter)
