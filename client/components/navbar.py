import customtkinter as ctk


class NavbarButton(ctk.CTkButton):
    def __init__(self, master, text, fnToExecute):
        super().__init__(
            master=master,
            text=text,
            font=("Arial", 32, "bold"),
            text_color="#00AAFF",
            fg_color="transparent",
            border_width=5,
            border_color="#00AAFF",
            corner_radius=10,
            hover_color=("#8ed9ff", "#004466"),
            command=fnToExecute,
        )

    def make_active(self):
        self.configure(
            text_color=("white", "black"),
            fg_color="#00AAFF",
            hover_color=("#30baff", "#007fbe"),
        )

    def make_inactive(self):
        self.configure(
            text_color="#00AAFF",
            fg_color="transparent",
            hover_color=("#8ed9ff", "#004466"),
        )


class Navbar(ctk.CTkFrame):
    def __init__(self, master, screen_width):
        super().__init__(
            master=master, width=0.5 * screen_width, height=80, fg_color="transparent"
        )

        self.master = master

        change_screen_fn = lambda screenTo: self.master.master.showScreen(screenTo)

        def logout_fn():
            # self = navbar
            # self.master = screen/page
            # self.master.master = app instance
            self.master.master.active_user = None
            change_screen_fn("landingScreen")

        home_btn = NavbarButton(self, "Home", lambda: change_screen_fn("homeScreen"))
        search_btn = NavbarButton(
            self, "Search", lambda: change_screen_fn("searchScreen")
        )
        my_events_btn = NavbarButton(
            self, "My events", lambda: change_screen_fn("myEventsScreen")
        )
        profile_btn = NavbarButton(
            self, "Profile", lambda: change_screen_fn("profileScreen")
        )

        logout_btn = NavbarButton(self, "Log out", logout_fn)

        self.buttons = [home_btn, search_btn, my_events_btn, profile_btn, logout_btn]

        for button in self.buttons:
            button.pack(padx=10, side="left")

        self.place(relx=0.48, rely=0.03)

    def activate_button(self, button_index):
        for i in range(len(self.buttons)):
            button = self.buttons[i]
            if i == button_index:
                button.make_active()
            else:
                button.make_inactive()
