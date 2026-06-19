import customtkinter as ctk
from welcome_page import WelcomePage
from chat_page import ChatPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class SustainableTravelApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Sustainable Travel Assistant")
        self.geometry("1200x800")
        self.minsize(900, 650)
        self.configure(fg_color="#0A0E1A")

        self.show_welcome()

    def clear_window(self):

        for widget in self.winfo_children():
            widget.destroy()

    def show_welcome(self):

        self.clear_window()
        WelcomePage(self, self.show_chat)

    def show_chat(self):

        self.clear_window()
        ChatPage(self)


app = SustainableTravelApp()
app.mainloop()