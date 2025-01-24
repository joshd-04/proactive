import customtkinter as ctk
import requests, hashlib, json

from ..components.form_input_field import form_input_field


class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, screen_width, screen_height, API_URL):
        super().__init__(master=master, fg_color="transparent")
        self.master = master
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.API_URL = API_URL

        self.username_issue = ctk.StringVar(master=self, value="")
        self.password_issue = ctk.StringVar(master=self, value="")

        proactive_label = ctk.CTkLabel(
            master=self,
            text="ProActive",
            font=("Arial", 32, "bold"),
            text_color=("black", "white"),
        )

        proactive_label.place(relx=0.03, rely=0.04)

        header_label = ctk.CTkLabel(
            master=self,
            text="Welcome back!",
            font=("Arial", 48, "bold"),
            text_color=("black", "white"),
        )
        caption_label = ctk.CTkLabel(
            master=self,
            text="Log in to your account here",
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

        self.username_input = form_input_field(
            master=form,
            field_name="Username",
            entry_width=form_width,
            error_message=self.username_issue,
        )
        self.password_input = form_input_field(
            master=form,
            field_name="Password",
            entry_width=form_width,
            error_message=self.password_issue,
            censor_input=True,
        )
        self.username_input.pack(pady=10)
        self.password_input.pack(pady=10)

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

        header_label.pack(pady=(60, 10))
        caption_label.pack()
        form.pack(pady=35)
        submit_btn.pack(pady=10)
        back_btn.pack()

    def verify_form(self):
        username = self.username_input.get()
        password = self.password_input.get()

        self.username_issue.set("")
        self.password_issue.set("")

        if len(username) == 0:
            self.username_issue.set("Username is required")
        elif len(password) == 0:
            self.password_issue.set("Password is required")
        else:
            self.send_api_request()

    def send_api_request(self):
        username = self.username_input.get()

        # Convert password to SHA-256 hash. encode() turns string into bytes
        # sha256 is the algorithm, hexdigest converts binary output to hexadecimal
        password_hash = hashlib.sha256(self.password_input.get().encode()).hexdigest()

        data_to_send_dict = {"username": username, "password_hash": password_hash}
        data_to_send_json = json.dumps(data_to_send_dict)

        # Send API request
        response = requests.post(url=f"{self.API_URL}/login", json=data_to_send_json)

        # Handle response
        if response.status_code == 200:
            user = response.json()
            self.master.active_user = user
            self.master.showScreen("homeScreen")
        elif response.status_code == 401:
            reasons = response.json()
            reasons_keys = list(reasons.keys())

            if "username" in reasons_keys:
                self.username_issue.set(reasons["username"])
            if "password" in reasons_keys:
                self.password_issue.set(reasons["password"])
        else:
            print("There was an error!")
