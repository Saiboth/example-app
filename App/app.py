import customtkinter as ctk
import tkinter as tk
from Utils import titlebar as tb

class BaseFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Some text", anchor="center")
        label.pack(expand=True, fill="both", side="top", padx=5, pady=5)

        self.pack(expand=True, fill="both")

class SubFrame(ctk.CTkFrame):
    def __init__(self, parent, labelText, buttonText):
        super().__init__(parent)
        
        self.svar = tk.StringVar(master=self, value="test")
        label = ctk.CTkLabel(self, text=labelText, anchor="center")
        entry = ctk.CTkEntry(self, textvariable=self.svar)
        button = ctk.CTkButton(self, text=buttonText, command=lambda: label.configure(text=self.svar.get()))

        label.pack(expand=True, fill="both", side="left", padx=5, pady=5)
        entry.pack(expand=True, fill="both", side="left", padx=5, pady=15)
        button.pack(expand=True, fill="both", side="left", padx=5, pady=5)

        self.pack(expand=True, fill="both")

class App(tb.App):
    def __init__(self, title="", titlebarcolor="#333333", width=200, height=200) -> None:
        super().__init__(title=title, titlebarcolor=titlebarcolor, width=width, height=height)
        # utils.SetTitleBarColor(self, 0x00FF0000)
        # self.title(title)
        # self.minsize(width=width, height=height)
        # self.maxsize(width=width*2, height=height*2)
        self.makeUI()

    def makeUI(self):
        baseFrame = BaseFrame(self.window)
        for i in range(3):
            SubFrame(baseFrame, f"Label{i}", f"Button{i}")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("./style/theme.json")  # Themes: blue (default), dark-blue, green
    app = App("Example app", width=300, height=300)
    app.mainloop()
