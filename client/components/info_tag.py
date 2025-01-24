import customtkinter as ctk


class Info_tag(ctk.CTkLabel):
    def __init__(
        self,
        master,
        text,
        font=("Arial", 20),
        fg_color=("#CBCBCB", "#353535"),
        text_color=("black", "white"),
    ):
        super().__init__(
            master=master,
            text=text,
            font=font,
            fg_color=fg_color,
            text_color=text_color,
            corner_radius=100,
        )
