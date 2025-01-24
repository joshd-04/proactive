import customtkinter as ctk
from .info_tag import Info_tag


class Event_preview(ctk.CTkFrame):
    def __init__(
        self,
        app_master,
        master,
        event_id,
        event_title,
        sport,
        date_string,
        max_participants=None,
        spaces_left=None,
        participant_count=None,
        distance_km=None,
        show_delete_btn=False,
        delete_command=lambda: None,
        users_rating=None,
        avg_rating=None,
    ):
        super().__init__(
            master=master, width=260, height=320, fg_color=("white", "black")
        )
        self.app_master = app_master
        self.event_id = event_id
        # Make sure the frame keeps its dimensions
        self.propagate(False)

        # Create labels + buttons
        title_label = ctk.CTkLabel(
            master=self,
            text=event_title,
            font=("Arial", 20, "bold"),
            wraplength=260,
        )
        sport_label = Info_tag(self, sport)
        date_label = Info_tag(self, date_string)
        title_label.pack(anchor="w", padx=10, pady=10)

        participants_label = None
        if spaces_left and max_participants:
            participants_label = Info_tag(
                self, f"{spaces_left}/{max_participants} spaces left"
            )
        elif participant_count:
            participants_label = Info_tag(self, f"{participant_count} attendees")
        distance_label = Info_tag(self, f"{distance_km} km away")

        details_btn = ctk.CTkButton(
            master=self,
            text=" View details ",
            text_color="white",
            font=("Arial", 20),
            fg_color="#00AAFF",
            height=40,
            corner_radius=10,
            command=self.view_details,
        )

        rating_widget = None
        if users_rating == -1:
            # Show "write review" button
            rating_widget = ctk.CTkButton(
                master=self,
                text=" Write a review ",
                text_color="white",
                font=("Arial", 20),
                fg_color="#00AAFF",
                height=40,
                corner_radius=10,
                # command=self.view_details, # Will be implemented later
            )
        elif users_rating:
            # otherwise if users_rating is still provided,
            # create a text label
            rating_widget = ctk.CTkLabel(
                master=self,
                text=f"You rated this {users_rating} stars",
                font=("Arial", 20),
            )

        # Pack components onto event preview frame
        sport_label.pack(anchor="w", padx=10, pady=5)
        date_label.pack(anchor="w", padx=10, pady=5)
        if participants_label:
            participants_label.pack(anchor="w", padx=10, pady=5)
        if distance_km:
            distance_label.pack(anchor="w", padx=10, pady=5)
        details_btn.pack(anchor="w", padx=10, pady=15)

        # If the event is deletable, then add the delete button
        if show_delete_btn == True:
            delete_btn = ctk.CTkButton(
                master=self,
                text=" Delete ",
                text_color="white",
                font=("Arial", 20, "bold"),
                fg_color="red",
                height=40,
                corner_radius=10,
                command=delete_command,
            )
            delete_btn.pack(anchor="w", padx=10, pady=0)

        if rating_widget:
            rating_widget.pack(anchor="w", padx=10, pady=10)

        avg_rating_label = None
        if avg_rating == -1:
            avg_rating_label = ctk.CTkLabel(
                master=self, text="Avg rating: pending", font=("Arial", 20)
            )
        elif avg_rating:
            avg_rating_label = ctk.CTkLabel(
                master=self, text=f"Avg rating: {avg_rating} stars", font=("Arial", 20)
            )

        if avg_rating_label:
            avg_rating_label.pack(anchor="w", padx=10, pady=10)

    def view_details(self):
        self.app_master.showScreen("eventScreen", event_id=self.event_id)
