import customtkinter as ctk


class LandingScreen(ctk.CTkFrame):
    def __init__(self, master, screen_width):
        super().__init__(master, fg_color="transparent")
        self.master = master

        proactive_label = ctk.CTkLabel(
            master=self,
            text="ProActive",
            font=("Arial", 32, "bold"),
            text_color=("black", "white"),
        )

        proactive_label.place(relx=0.03, rely=0.04)

        slogan_label = ctk.CTkLabel(
            master=self,
            text="Be Active Like A Pro",
            font=("Arial", 48, "bold"),
            text_color=("black", "white"),
        )
        description_label = ctk.CTkLabel(
            master=self,
            text="Find sports events you can actually play in at a time and place that suits you",
            wraplength=screen_width / 2.5,
            font=("Arial", 24),
            text_color=("black", "white"),
        )

        # Container to hold the buttons, container will be used to place the buttons side by side
        buttons_container = ctk.CTkFrame(
            master=self, width=screen_width / 2, height=50, fg_color="transparent"
        )

        log_in_btn = ctk.CTkButton(
            master=buttons_container,
            width=200,
            height=50,
            text="Log in",
            text_color="black",
            font=("Arial", 20, "bold"),
            fg_color="#2DC0E9",
            border_color="#2DC0E9",
            border_width=3,
            hover_color=("#64ffff", "#009e9e"),
            corner_radius=50,
            command=lambda: master.showScreen("loginScreen"),
        )
        register_btn = ctk.CTkButton(
            master=buttons_container,
            width=200,
            height=50,
            text="Register",
            text_color=("black", "white"),
            font=("Arial", 20, "bold"),
            fg_color=("white", "#303030"),
            border_color="#2DC0E9",
            border_width=3,
            hover_color=("#64ffff", "#003232"),
            corner_radius=50,
            command=lambda: master.showScreen("registerScreen"),
        )

        # Place the buttons in a grid on the frame container
        log_in_btn.grid(row=0, column=0, padx=20)
        register_btn.grid(row=0, column=1, padx=20)

        # Place the labels on screen

        slogan_label.pack(pady=(200, 20))
        description_label.pack(pady=(0, 40))
        buttons_container.pack()

        ### Bottom half of the screen

        why_us_title = ctk.CTkLabel(
            master=self,
            text="Why ProActive?",
            font=("Arial", 32, "bold"),
            text_color=("black", "white"),
        )

        why_us_reasons = [
            "Browse events, refine search results to your liking",
            "Read reviews written by others just like you",
            "See all of your upcoming and previous events all in one place!",
            "Create events to show to other users!",
            "Write constructive reviews to help other event hosts",
            "State of the art recommendation system, delivering events you didn't know you liked!",
            "Modern profile with graphical statistics page to see your progress over time",
        ]

        reasons_frame = ctk.CTkFrame(master=self, fg_color="transparent")

        for index, reason in enumerate(why_us_reasons):
            reasonLabel = ctk.CTkLabel(
                master=reasons_frame,
                text=f"- {reason}",
                font=("Arial", 20),
                text_color=("black", "white"),
                width=screen_width / 2,
                anchor="w",
            )
            reasonLabel.grid(row=index, column=0, sticky="w")

        why_us_title.pack(pady=(100, 40))
        reasons_frame.pack(padx=(100, 0))
