import pathlib
import customtkinter as ctk
import tkinter as tk
import exampleApp.Utils.titlebar as tb
from pathlib import Path
import sys
import os


def resolve_path(path) -> str:
    if getattr(sys, "frozen", False):
        # If the 'frozen' flag is set, we are in bundled-app mode!
        resolved_path: str = os.path.abspath(path=os.path.join(sys._MEIPASS, path))
    else:
        # Normal development mode. Use os.getcwd() or __file__ as appropriate in your case...
        parent: Path = Path(__file__).parent.parent
        resolved_path: str = os.path.abspath(path=os.path.join(parent, path))

    return resolved_path


class BaseFrame(ctk.CTkFrame):
    def __init__(self, parent) -> None:
        super().__init__(master=parent)
        label = ctk.CTkLabel(master=self, text="Some text", anchor="center")
        label.pack(expand=True, fill="both", side="top", padx=5, pady=5)

        self.pack(expand=True, fill="both")


class SubFrame(ctk.CTkFrame):
    def __init__(self, parent, labelText, buttonText) -> None:
        super().__init__(master=parent)

        self.svar = tk.StringVar(master=self, value="test")
        label = ctk.CTkLabel(master=self, text=labelText, anchor="center")
        entry = ctk.CTkEntry(master=self, textvariable=self.svar)
        button = ctk.CTkButton(
            master=self,
            text=buttonText,
            command=lambda: label.configure(text=self.svar.get()),
        )

        label.pack(expand=True, fill="both", side="left", padx=5, pady=5)
        entry.pack(expand=True, fill="both", side="left", padx=5, pady=15)
        button.pack(expand=True, fill="both", side="left", padx=5, pady=5)

        self.pack(expand=True, fill="both")


class App(tb.App):
    def __init__(
        self, title="", titlebarcolor="#333333", width=200, height=200
    ) -> None:
        super().__init__(
            title=title, titlebarcolor=titlebarcolor, width=width, height=height
        )
        # utils.SetTitleBarColor(self, 0x00FF0000)
        # self.title(title)
        # self.minsize(width=width, height=height)
        # self.maxsize(width=width*2, height=height*2)
        self.makeUI()

    def makeUI(self) -> None:
        baseFrame = BaseFrame(parent=self.window)
        for i in range(3):
            SubFrame(parent=baseFrame, labelText=f"Label{i}", buttonText=f"Button{i}")


def main():
    ctk.set_appearance_mode(mode_string="dark")  # Modes: system (default), light, dark
    ctk.set_default_color_theme(
        color_string=resolve_path(path="./style/theme.json")
    )  # Themes: blue (default), dark-blue, green
    app = App(title="Example app", width=300, height=300)
    app.mainloop()


if __name__ == "__main__":
    main()
