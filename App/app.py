import customtkinter as tk

class BaseFrame(tk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.CTkLabel(self, text="Some text", bg_color="grey", anchor="center")
        label.pack(expand=True, fill="both", side="top", padx=5, pady=5)

        self.pack(expand=True, fill="both")

class SubFrame(tk.CTkFrame):
    def __init__(self, parent, labelText, buttonText):
        super().__init__(parent)
        self.svar = tk.StringVar(master=self, value="test")
        label = tk.CTkLabel(self, text=labelText, anchor="center")
        entry = tk.CTkEntry(self, textvariable=self.svar)
        button = tk.CTkButton(self, text=buttonText, command=lambda: label.configure(text=self.svar.get()))

        label.pack(expand=True, fill="both", side="left", padx=5, pady=5)
        entry.pack(expand=True, fill="both", side="left", padx=5, pady=15)
        button.pack(expand=True, fill="both", side="left", padx=5, pady=5)

        self.pack(expand=True, fill="both")

class App(tk.CTk):
    def __init__(self, title, width, height) -> None:
        super().__init__()
        self.title(title)
        self.minsize(width=width, height=height)
        self.maxsize(width=width*2, height=height*2)
        self.makeUI()

    def makeUI(self):
        baseFrame = BaseFrame(self)
        for i in range(3):
            SubFrame(baseFrame, f"Label{i}", f"Button{i}")


if __name__ == "__main__":
    app = App("Example app", width=300, height=220)
    app.mainloop()
