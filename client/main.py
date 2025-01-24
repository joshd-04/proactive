# imports
import customtkinter as ctk

from client.screens.create_event import CreateEventScreen
from client.screens.event_page import EventScreen
from client.screens.my_events import MyEventsScreen

from .screens.login import LoginScreen
from .screens.register import RegisterScreen
from .screens.landing import LandingScreen
from .screens.home import HomeScreen
from .screens.search import SearchScreen

# define the global variables
global textFont
global screen_width
global screen_height
global active_user
global API_URL

# assign values to the defines global constants
screen_width = 1600
screen_height = 900
API_URL = "http://127.0.0.1:5000"

ctk.set_appearance_mode("light")


# app class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{screen_width}x{screen_height}")
        self.resizable(False, False)
        self.rowconfigure(index=0, minsize=screen_height)
        self.columnconfigure(index=0, minsize=screen_width)

        # Global app variables
        self.active_user = None

        self.app_screens = {
            "landingScreen": lambda: LandingScreen(
                master=self,
                screen_width=screen_width,
            ),
            "registerScreen": lambda: RegisterScreen(
                master=self,
                screen_height=screen_height,
                screen_width=screen_width,
                API_URL=API_URL,
            ),
            "loginScreen": lambda: LoginScreen(
                master=self,
                screen_height=screen_height,
                screen_width=screen_width,
                API_URL=API_URL,
            ),
            "homeScreen": lambda: HomeScreen(
                master=self,
                screen_width=screen_width,
                screen_height=screen_height,
                API_URL=API_URL,
            ),
            "searchScreen": lambda: SearchScreen(
                master=self,
                screen_width=screen_width,
                screen_height=screen_height,
                API_URL=API_URL,
            ),
            "myEventsScreen": lambda: MyEventsScreen(
                master=self,
                screen_width=screen_width,
                screen_height=screen_height,
                API_URL=API_URL,
            ),
            "eventScreen": lambda event_id: EventScreen(
                master=self,
                screen_width=screen_width,
                screen_height=screen_height,
                API_URL=API_URL,
                event_id=event_id,
            ),
            "createEventScreen": lambda: CreateEventScreen(
                master=self,
                screen_width=screen_width,
                screen_height=screen_height,
                API_URL=API_URL,
            ),
        }

        # self.showScreen("landingScreen")
        self.showScreen("myEventsScreen")

        self.mainloop()

    def showScreen(self, screenName, **kwargs):
        display_screen_fn = self.app_screens[screenName]
        if screenName == "eventScreen":
            screen = display_screen_fn(event_id=kwargs["event_id"])
        else:
            screen = display_screen_fn()

        screen.grid(row=0, column=0, sticky="nsew")
        screen.tkraise()


# Create an instance of the application that allows the program to run
app = App()
