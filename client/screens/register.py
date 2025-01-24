import customtkinter as ctk
from geopy.geocoders import Nominatim
import requests, hashlib, json

from ..components.form_input_field import form_input_field


class RegisterScreen(ctk.CTkFrame):
    def __init__(self, master, screen_width, screen_height, API_URL):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.API_URL = API_URL

        self.username_issue = ctk.StringVar(master=self, value="")
        self.first_name_issue = ctk.StringVar(master=self, value="")
        self.last_name_issue = ctk.StringVar(master=self, value="")
        self.age_issue = ctk.StringVar(master=self, value="")
        self.home_location_issue = ctk.StringVar(master=self, value="")
        self.password_issue = ctk.StringVar(master=self, value="")
        self.password_confirm_issue = ctk.StringVar(master=self, value="")

        self.home_location = ctk.StringVar(value="Click to input")
        self.home_location_coords = (999, 999)

        proactive_label = ctk.CTkLabel(
            master=self,
            text="ProActive",
            font=("Arial", 32, "bold"),
            text_color=("black", "white"),
        )

        proactive_label.place(relx=0.03, rely=0.04)

        header_label = ctk.CTkLabel(
            master=self,
            text="Hi there! Welcome",
            font=("Arial", 48, "bold"),
            text_color=("black", "white"),
        )
        caption_label = ctk.CTkLabel(
            master=self,
            text="Create an account today",
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

        # Username

        self.username_input = form_input_field(
            master=form,
            field_name="Username",
            entry_width=form_width,
            error_message=self.username_issue,
        )

        # First name + last name
        ## New frame required as they are positioned next to each other

        name_input_frame = ctk.CTkFrame(
            master=form, width=form_width, fg_color="transparent"
        )
        self.first_name_input = form_input_field(
            master=name_input_frame,
            field_name="First name",
            entry_width=250,
            error_message=self.first_name_issue,
        )
        self.last_name_input = form_input_field(
            master=name_input_frame,
            field_name="Last name",
            entry_width=250,
            error_message=self.last_name_issue,
        )
        self.first_name_input.grid(row=0, column=0, padx=(0, 15))
        self.last_name_input.grid(row=0, column=1, padx=(15, 0))

        # Age + home location

        details_input_frame = ctk.CTkFrame(
            master=form, width=form_width, fg_color="transparent"
        )
        self.age_input = form_input_field(
            master=details_input_frame,
            field_name="Age",
            entry_width=170,
            error_message=self.age_issue,
        )

        home_location_frame = ctk.CTkFrame(
            master=details_input_frame, fg_color="transparent"
        )
        # Create label + entry
        home_location_label = ctk.CTkLabel(
            master=home_location_frame,
            text="Home location:",
            font=("Arial", 20),
            width=330,
            anchor="w",  # align text to the left
        )

        self.home_location_btn = ctk.CTkButton(
            master=home_location_frame,
            width=330,
            font=("Arial", 20),
            text="Click to input",
            command=self.show_location_popup,
        )

        home_location_error_label = ctk.CTkLabel(
            master=home_location_frame,
            textvariable=self.home_location_issue,
            font=("Arial", 20, "bold"),
            text_color="red",
            width=330,
            anchor="w",
        )

        home_location_label.pack()
        self.home_location_btn.pack()
        home_location_error_label.pack()

        self.age_input.grid(row=0, column=0, padx=(0, 15))
        home_location_frame.grid(row=0, column=1, padx=(15, 0))

        # Password

        self.password_input = form_input_field(
            master=form,
            field_name="Password",
            entry_width=form_width,
            censor_input=True,
            error_message=self.password_issue,
        )

        # Password confirm
        self.password_confirm_input = form_input_field(
            master=form,
            field_name="Password confirm",
            entry_width=form_width,
            censor_input=True,
            error_message=self.password_confirm_issue,
        )

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
            command=lambda: self.master.showScreen("landingScreen"),
            fg_color="darkgrey",
            hover_color="grey",
            text_color="black",
        )

        self.username_input.pack(pady=10)
        name_input_frame.pack(pady=10)
        details_input_frame.pack(pady=10)
        self.password_input.pack(pady=10)
        self.password_confirm_input.pack(pady=10)
        submit_btn.pack(pady=10)
        back_btn.pack()

        header_label.pack(pady=(60, 10))
        caption_label.pack()
        form.pack(pady=35)

    def show_location_popup(self):
        self.home_location.set("Your address will appear here")
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
            textvariable=self.home_location,
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
            self.home_location_coords = (location.longitude, location.latitude)
        except:
            address = "No address found."
            self.home_location_coords = (999, 999)

        self.home_location.set(address)
        self.home_location_btn.configure(text=address[0:30])

    def verify_form(self):
        username = self.username_input.get()
        first_name = self.first_name_input.get()
        last_name = self.last_name_input.get()
        age = self.age_input.get()
        home_location_coords = self.home_location_coords
        password = self.password_input.get()
        password_confirm = self.password_confirm_input.get()

        self.username_issue.set("")
        self.first_name_issue.set("")
        self.last_name_issue.set("")
        self.age_issue.set("")
        self.home_location_issue.set("")
        self.password_issue.set("")
        self.password_confirm_issue.set("")

        # Username checks: 3-15 chars
        if " " in username:
            self.username_issue.set("Username cannot contain spaces")
        if len(username) < 3:
            self.username_issue.set("Username too short. Min 3 chars")
        if len(username) > 15:
            self.username_issue.set("Username too long. Max 15 chars")

        for character in username:
            if character.isupper():
                self.username_issue.set("Username must not contain capital letters.")
                break

        # First name checks: 2-25 chars
        if len(first_name) < 2:
            self.first_name_issue.set("First name too short. Min 2 chars")
        if len(first_name) > 25:
            self.first_name_issue.set("First name too long. Max 25 chars")

        # Last name checks: 2-25
        if len(last_name) < 2:
            self.last_name_issue.set("Last name too short. Min 2 chars")
        if len(last_name) > 25:
            self.last_name_issue.set("Last name too long. Max 25 chars")

        # Age: Integer and age >= 16
        # try cast string to integer
        try:
            age = int(age)
            if age < 16:
                self.age_issue.set("You must be 16 or over to use this app")
        except ValueError:  # if casting to integer fails
            self.age_issue.set("Age must be an integer")

        # Home location check
        if home_location_coords[0] > 180 or home_location_coords[0] < -180:
            self.home_location_issue.set("Invalid longitude")
        if home_location_coords[1] > 90 or home_location_coords[1] < -90:
            self.home_location_issue.set("Invalid latitude")

        # Password checks: 8 chars+, 1 upper, 1 lower, 1
        if len(password) < 8:
            self.password_issue.set("Password is too short. Min 8 chars")

        else:
            upper_count = 0
            lower_count = 0
            number_count = 0
            # isalnum() returns true if string contains only letters or numbers
            contains_symbol = not password.isalnum()
            for character in password:
                if character.isupper():
                    upper_count += 1
                if character.islower():
                    lower_count += 1
                if character.isdigit():
                    number_count += 1

            if upper_count == 0:
                self.password_issue.set("Password needs one uppercase letter")
            if lower_count == 0:
                self.password_issue.set("Password needs one lowercase letter")
            if number_count == 0:
                self.password_issue.set("Password needs one number")
            if contains_symbol == False:
                self.password_issue.set("Password needs one symbol")

        # Password confirmation check: passwordconfirm must match password
        if password != password_confirm:
            self.password_confirm_issue.set("Passwords do not match")

        # Check if issue stringvars are empty. if they are, all inputs are valid (true). otherwise false
        valid = False
        if (
            self.username_issue.get() == ""
            and self.first_name_issue.get() == ""
            and self.last_name_issue.get() == ""
            and self.age_issue.get() == ""
            and self.home_location_issue.get() == ""
            and self.password_issue.get() == ""
            and self.password_confirm_issue.get() == ""
        ):
            valid = True

        if valid == True:
            self.send_API_request()

    def send_API_request(self):
        # Convert password to SHA-256 hash. encode() turns string into bytes
        # sha256 is the algorithm, hexdigest converts binary output to hexadecimal
        password_hash = hashlib.sha256(self.password_input.get().encode()).hexdigest()

        data_to_send_dict = {
            "first_name": self.first_name_input.get(),
            "last_name": self.last_name_input.get(),
            "age": self.age_input.get(),
            "home_location": [
                self.home_location_coords[0],
                self.home_location_coords[1],
            ],
            "username": self.username_input.get(),
            "password_hash": password_hash,
        }

        # Convert to JSON format
        data_to_send_json = json.dumps(data_to_send_dict)

        response = requests.post(url=f"{self.API_URL}/register", json=data_to_send_json)
        if response.status_code == 400:
            response_data = response.json()
            if "username" in list(response_data.keys()):
                self.username_issue.set(response_data["username"])
            if "first_name" in list(response_data.keys()):
                self.first_name_issue.set(response_data["first_name"])
            if "last_name" in list(response_data.keys()):
                self.last_name_issue.set(response_data["last_name"])
            if "age" in list(response_data.keys()):
                self.age_issue.set(response_data["age"])
            if "home_location" in list(response_data.keys()):
                self.home_location_issue.set(response_data["home_location"])
        elif response.status_code == 201:
            self.master.showScreen("landingScreen")
