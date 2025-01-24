from datetime import datetime
import customtkinter as ctk
from geopy.geocoders import Nominatim
import requests, hashlib, json

from client.components.navbar import Navbar

from ..components.form_input_field import form_input_field


class CreateEventScreen(ctk.CTkFrame):
    def __init__(self, master, screen_width, screen_height, API_URL):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.screen_width = screen_width
        self.screen_height = screen_height
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

            self.title_issue = ctk.StringVar(master=self, value="")
            self.description_issue = ctk.StringVar(master=self, value="")
            self.sport_issue = ctk.StringVar(master=self, value="")
            self.location_issue = ctk.StringVar(master=self, value="")
            self.max_participants_issue = ctk.StringVar(master=self, value="")
            self.date_time_issue = ctk.StringVar(master=self, value="")

            self.location = ctk.StringVar(value="Click to input")
            self.location_coords = (999, 999)

            proactive_label = ctk.CTkLabel(
                master=self,
                text="ProActive",
                font=("Arial", 32, "bold"),
                text_color=("black", "white"),
            )

            proactive_label.place(relx=0.03, rely=0.04)
            Navbar(master=self, screen_width=screen_width)

            header_label = ctk.CTkLabel(
                master=self,
                text="Create an event",
                font=("Arial", 48, "bold"),
                text_color=("black", "white"),
            )
            caption_label = ctk.CTkLabel(
                master=self,
                text="Share your love of sports with the world",
                font=("Arial", 24),
                text_color=("black", "white"),
            )

            form_width = 0.33 * self.screen_width

            form = ctk.CTkFrame(
                master=self,
                width=form_width,
                height=0.7 * self.screen_height,
                fg_color="transparent",
            )

            # Title
            self.title_input = form_input_field(
                master=form,
                field_name="Event title",
                entry_width=form_width,
                error_message=self.title_issue,
            )

            # Description
            self.description_input = form_input_field(
                master=form,
                field_name="Description",
                entry_width=form_width,
                error_message=self.description_issue,
            )

            # Sport + location
            details_input_frame = ctk.CTkFrame(
                master=form, width=form_width, fg_color="transparent"
            )
            self.sport_input = form_input_field(
                master=details_input_frame,
                field_name="Sport",
                entry_width=190,
                error_message=self.sport_issue,
            )

            location_frame = ctk.CTkFrame(
                master=details_input_frame, fg_color="transparent"
            )
            # Create label + entry
            location_label = ctk.CTkLabel(
                master=location_frame,
                text="Location:",
                font=("Arial", 20),
                width=310,
                anchor="w",  # align text to the left
            )

            self.location_btn = ctk.CTkButton(
                master=location_frame,
                width=310,
                font=("Arial", 20),
                text="Click to input",
                command=self.show_location_popup,
            )

            location_error_label = ctk.CTkLabel(
                master=location_frame,
                textvariable=self.location_issue,
                font=("Arial", 20, "bold"),
                text_color="red",
                width=310,
                anchor="w",
            )

            location_label.pack()
            self.location_btn.pack()
            location_error_label.pack()

            self.sport_input.grid(row=0, column=0, padx=(0, 15))
            location_frame.grid(row=0, column=1, padx=(15, 0))

            event_attributes_input_frame = ctk.CTkFrame(
                master=form, width=form_width, fg_color="transparent"
            )

            def change_intensity(value):
                self.intensity_input = value

            self.intensity_input = "-- select --"

            intensity_section = ctk.CTkFrame(
                master=event_attributes_input_frame, width=150, fg_color="transparent"
            )
            intensity_label = ctk.CTkLabel(
                master=intensity_section, text="Intensity:", font=("Arial", 20)
            )
            intensity_dropdown = ctk.CTkOptionMenu(
                master=intensity_section,
                values=[
                    "-- select --",
                    "Low",
                    "Medium",
                    "Intense",
                ],
                fg_color="lightgrey",
                button_color="lightgrey",
                button_hover_color="grey",
                font=("Arial", 20),
                text_color="black",
                corner_radius=20,
                command=lambda new_val: change_intensity(new_val),
            )
            intensity_label.pack()
            intensity_dropdown.pack()

            skill_level_section = ctk.CTkFrame(
                master=event_attributes_input_frame, width=150, fg_color="transparent"
            )
            skill_level_label = ctk.CTkLabel(
                master=skill_level_section, text="Skill level:", font=("Arial", 20)
            )

            def change_skill_level(value):
                self.skill_level_input = value

            self.skill_level_input = "-- select --"

            skill_level_dropdown = ctk.CTkOptionMenu(
                master=skill_level_section,
                values=[
                    "-- select --",
                    "Beginner",
                    "Intermediate",
                    "Advanced",
                ],
                fg_color="lightgrey",
                button_color="lightgrey",
                button_hover_color="grey",
                font=("Arial", 20),
                text_color="black",
                corner_radius=20,
                command=lambda new_val: change_skill_level(new_val),
            )
            skill_level_label.pack()
            skill_level_dropdown.pack()

            intensity_section.pack(side="left", padx=(0, 100))
            skill_level_section.pack(side="left", padx=(100, 0))

            # Participant details

            participant_details_frame = ctk.CTkFrame(
                master=form, width=form_width, fg_color="transparent"
            )

            self.max_participants_input = form_input_field(
                master=participant_details_frame,
                field_name="Max participants",
                entry_width=190,
                error_message=self.max_participants_issue,
            )
            self.date_time_input = form_input_field(
                master=participant_details_frame,
                field_name="Time + date (HH:MM DD/MM/YYYY)",
                entry_width=310,
                error_message=self.date_time_issue,
            )

            self.max_participants_input.pack(side="left")
            self.date_time_input.pack(side="left")

            # Submit button
            submit_btn = ctk.CTkButton(
                master=form,
                width=form_width,
                height=50,
                text="Submit",
                font=("Arial", 24),
                command=self.verify_form,
            )

            back_btn = ctk.CTkButton(
                master=form,
                width=form_width,
                height=50,
                text="Back",
                font=("Arial", 24),
                command=lambda: self.master.showScreen("myEventsScreen"),
                fg_color="darkgrey",
                hover_color="grey",
                text_color="black",
            )

            self.title_input.pack()
            self.description_input.pack()
            details_input_frame.pack()
            event_attributes_input_frame.pack()
            participant_details_frame.pack(anchor="w")
            submit_btn.pack(pady=10)
            back_btn.pack()

            header_label.pack(pady=(100, 10))
            caption_label.pack()
            form.pack(pady=35)

    def show_location_popup(self):
        self.location.set("Your address will appear here")
        popup = ctk.CTkToplevel(self.master)
        popup.geometry("600x400")
        popup.resizable(False, False)

        proactive_label = ctk.CTkLabel(
            master=popup,
            text="ProActive",
            font=("Arial", 24, "bold"),
            text_color=("black", "white"),
        )

        submit_btn = ctk.CTkButton(
            master=popup,
            text="Submit",
            font=("Arial", 20),
            fg_color="lime",
            hover_color="green",
        )

        address_label = ctk.CTkLabel(
            master=popup,
            textvariable=self.location,
            font=("Arial", 20),
            text_color=("black", "white"),
            wraplength=400,
        )

        find_automatically_btn = ctk.CTkButton(
            master=popup,
            text="Find address automatically",
            width=300,
            height=30,
            font=("Arial", 20),
            state="disabled",
        )

        option2_label = ctk.CTkLabel(
            master=popup,
            text="Or type manually:",
            font=("Arial", 20),
            text_color=("black", "white"),
        )

        manual_frame = ctk.CTkFrame(master=popup, width=300, fg_color="transparent")
        self.manual_address_entry = ctk.CTkEntry(
            master=manual_frame, width=240, font=("Arial", 20)
        )
        manual_address_submit = ctk.CTkButton(
            master=manual_frame,
            width=40,
            text="Go",
            font=("Arial", 20),
            fg_color="lime",
            hover_color="green",
            command=self.find_address_manually,
        )

        self.manual_address_entry.grid(row=0, column=0, padx=(0, 10))
        manual_address_submit.grid(row=0, column=1, padx=(10, 0))

        proactive_label.place(relx=0.03, rely=0.04)
        submit_btn.place(relx=0.7, rely=0.04)
        address_label.pack(pady=(70, 10))
        find_automatically_btn.pack(pady=20)
        option2_label.pack()
        manual_frame.pack()

        popup.grab_set()
        popup.mainloop()

    def find_address_manually(self):
        entry = self.manual_address_entry.get()
        geolocator = Nominatim(user_agent="location_tkinter")
        location = geolocator.geocode(entry)

        try:
            address = location.raw["display_name"]
            self.location_coords = (location.longitude, location.latitude)
        except:
            address = "No address found."
            self.location_coords = (999, 999)

        self.location.set(address)
        self.location_btn.configure(text=address[0:30])

    def verify_form(self):

        title = self.title_input.get()
        description = self.description_input.get()
        sport = self.sport_input.get()
        location_coords = self.location_coords
        intensity = self.intensity_input
        skill_level = self.skill_level_input
        max_participants = self.max_participants_input.get()
        date_time = self.date_time_input.get()

        self.title_issue.set("")
        self.description_issue.set("")
        self.sport_issue.set("")
        self.location_issue.set("")
        self.max_participants_issue.set("")
        self.date_time_issue.set("")

        # Title checks:
        if len(title) == 0:
            self.title_issue.set("Event title is required")

        # Description checks: >100
        if len(description) < 100:
            self.description_issue.set("Description must be atleast 100 characters")

        # Sport checks
        if len(sport) < 2:
            self.sport_issue.set("Invalid sport")

        # Location checks
        if abs(location_coords[0]) > 90:
            self.location_issue.set("Invalid latitude!")
        if abs(location_coords[1]) > 180:
            self.location_issue.set("Invalid longitude!")

        # Max participant check 0 < x < 50
        # try cast string to integer
        try:
            max_participants = int(max_participants)
            if max_participants < 0:
                self.max_participants_issue.set("Must be greater than 0")
            if max_participants > 50:
                self.max_participants_issue.set("Must be less than 51")
        except ValueError:  # if casting to integer fails
            self.max_participants_issue.set("Max participants must be an integer")

        # Date time interpretation
        self.date_time = None
        try:
            print(date_time)
            time, date = date_time.split(" ")
            print(time, date)
            hours, minutes = time.split(":")

            day, month, year = date.split("/")
            if (
                len(hours) != 2
                and len(minutes) != 2
                and len(day) != 2
                and len(month) != 2
                and len(year) != 4
            ):
                self.date_time_issue.set("Invalid format")

            # Although unnecessary in the string, the integer casting ensures the values are all numbers
            # If they are not, an error will be thrown
            date_time_formatted = f"{year}-{month}-{day} {hours}:{minutes}"

            # If the formatted string can be convered into a datetime object successfully, then the formatted string is a valid date
            datetime.strptime(date_time_formatted, "%Y-%m-%d %H:%M")
            self.date_time = date_time_formatted

        except Exception as error:
            self.date_time_issue.set("Invalid format")

        # Only valid if no issues + intensity/skill level chosen
        valid = False
        if (
            self.title_issue.get() == ""
            and self.description_issue.get() == ""
            and self.sport_issue.get() == ""
            and self.location_issue.get() == ""
            and self.max_participants_issue.get() == ""
            and intensity != "-- select --"
            and skill_level != "-- select --"
            and self.date_time != None
        ):
            valid = True
            # valid = False

        if valid == True:
            self.send_API_request()

    def send_API_request(self):
        data_to_send_dict = {
            "title": self.title_input.get(),
            "description": self.description_input.get(),
            "sport": self.sport_input.get(),
            "intensity": self.intensity_input,
            "skill_level": self.skill_level_input,
            "max_participants": int(self.max_participants_input.get()),
            "location": self.location_coords,
            "event_creator": self.active_user["username"],
            "date_time": self.date_time,
        }

        # Convert to JSON format
        data_to_send_json = json.dumps(data_to_send_dict)

        response = requests.post(url=f"{self.API_URL}/events", json=data_to_send_dict)

        if response.status_code == 201:
            self.master.showScreen("myEventsScreen")
