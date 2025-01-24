import customtkinter as ctk


class form_input_field(ctk.CTkFrame):
    def __init__(
        self, master, field_name, entry_width, censor_input=False, error_message=""
    ):
        super().__init__(master=master, fg_color="transparent")

        # Create label + entry
        self.field_label = ctk.CTkLabel(
            master=self,
            text=f"{field_name}:",
            font=("Arial", 20),
            width=entry_width,
            anchor="w",  # align text to the left
        )

        if censor_input == True:
            self.field_entry = ctk.CTkEntry(
                master=self,
                width=entry_width,
                font=("Arial", 24),
                show="*",
            )
        else:
            self.field_entry = ctk.CTkEntry(
                master=self,
                width=entry_width,
                font=("Arial", 24),
            )

        self.error_label = ctk.CTkLabel(
            master=self,
            textvariable=error_message,
            font=("Arial", 20, "bold"),
            text_color="red",
            width=entry_width,
            anchor="w",
        )

        # Put widgets on screen
        self.field_label.pack()
        self.field_entry.pack()
        self.error_label.pack()

    # Setters + getters
    def get(self):
        return self.field_entry.get()

    def set(self, new_text):
        self.field_entry.delete(0, ctk.END)
        self.field_entry.insert(0, new_text)
