import customtkinter as ctk
from tkinter import TclError
from ctypes import windll


class Colors:
    LGRAY = "#3e4042"  # button color effects in the title bar (Hex color)
    LGRAY2 = "#3a3a3a"  # 3a3a3a
    DGRAY = "#0d1117"  # window background color               (Hex color)
    RGRAY = "#0e0e0e"  # title bar color                       (Hex color)
    RED = "#ae0d1a"


class Titlebar(ctk.CTkFrame):
    def __init__(
        self, parent, title="", titlebarcolor="#333333", foreground="#ffffff"
    ) -> None:
        super().__init__(master=parent)
        self.configure(
            bg_color=titlebarcolor
        )  # , relief='raised', bd=0, highlightthickness=0)
        self.parent = parent
        self.titlebarcolor: str = titlebarcolor
        self.fg: str = foreground

        # add buttons to the title bar
        self.title = ctk.CTkLabel(
            master=self, text=title, font=("helvetica", 10), padx=5
        )
        self.close_button = ctk.CTkButton(
            master=self, text="  ×  ", command=parent.destroy, font=("calibri", 13)
        )
        self.expand_button = ctk.CTkButton(
            master=self, text=" 🗖 ", command=self.maximize_me, font=("calibri", 13)
        )
        self.minimize_button = ctk.CTkButton(
            master=self, text=" ⎯ ", command=self.minimize_me, font=("calibri", 13)
        )

        # pack the widgets
        self.title.pack(side="left", padx=10)
        self.close_button.pack(side="right", ipadx=7, ipady=1)
        self.expand_button.pack(side="right", ipadx=7, ipady=1)
        self.minimize_button.pack(side="right", ipadx=7, ipady=1)
        self.pack(fill="x")

        # bind double click to maximize method
        self.bind(sequence="<Double-Button-1>", command=self.maximize_me)

        # hover effects for buttons
        self.close_button.bind(sequence="<Enter>", command=self.changex_on_hovering)
        self.close_button.bind(sequence="<Leave>", command=self.returnx_to_normalstate)
        self.expand_button.bind(
            sequence="<Enter>", command=self.change_size_on_hovering
        )
        self.expand_button.bind(
            sequence="<Leave>", command=self.return_size_on_hovering
        )
        self.minimize_button.bind(
            sequence="<Enter>", command=self.changem_size_on_hovering
        )
        self.minimize_button.bind(
            sequence="<Leave>", command=self.returnm_size_on_hovering
        )

        # bind move to frame and label
        self.bindMove(widget=self)
        self.bindMove(widget=self.title)

    def bindMove(self, widget) -> None:
        w = self
        if widget:
            w = widget
        w.bind("<Button-1>", lambda event, arg=w: self.startMove(event=event, w=arg))
        w.bind("<B1-Motion>", lambda event, arg=w: self.moving(event=event, w=arg))

        # self.bind("<Map>",self.frame_mapped)

    def startMove(self, event, w) -> None:
        # get relative click position when maximized and return to old size on drag
        if self.parent.maximized == True:
            normalx: int
            normaly: int
            maxx: int
            maxy: int

            normalx, normaly = self.get_geometry_xy(geom=self.normal_size)
            maxx, maxy = self.get_geometry_xy(geom=self.parent.geometry())
            locx = int(event.x / maxx * normalx)
            locy = int(event.y / maxy * normaly)
            w.x = locx
            w.y = locy
            self.maximize_me()
            self.expand_button.configure(text=" 🗖 ")
        else:
            w.x = event.x
            w.y = event.y

    def moving(self, event, w) -> None:
        x: int = event.x_root - w.x - w.winfo_rootx() + self.winfo_rootx()
        y: int = event.y_root - w.y - w.winfo_rooty() + self.winfo_rooty()
        self.parent.geometry(f"+{x}+{y}")

    def get_geometry_xy(self, geom) -> list[int]:
        xy = geom.split("+")[0]
        return [int(val) for val in xy.split("x")]

    def minimize_me(self, event=None) -> None:
        if self.parent.minimized == False:
            self.parent.update_idletasks()
            self.parent.overrideredirect(False)
            self.parent.unbind("<FocusOut>")
            self.parent.update_idletasks()
            self.parent.after_idle(self.safe_iconify)
            self.parent.minimized = True

    def safe_iconify(self) -> None:
        try:
            self.parent.iconify()
        except TclError:
            pass

    def deminimize(self, event) -> None:
        if self.parent.minimized == True:
            self.parent.iconify()
            self.parent.overrideredirect(True)
            self.parent.set_appwindow()
            self.parent.deiconify()
            self.parent.focus()
            self.parent.after_idle(
                lambda: self.bind(sequence="<FocusOut>", command=self.minimize_me)
            )
            self.parent.minimized = False

    def maximize_me(self, *args) -> None:
        if self.parent.maximized == False:
            self.normal_size: str = self.parent.geometry()
            self.expand_button.configure(text=" 🗗 ")
            w: int = self.parent.winfo_screenwidth()
            h: int = self.parent.winfo_screenheight()
            self.parent.geometry(f"{w}x{h}+0+0")
            self.parent.maximized = not self.parent.maximized

        else:
            self.expand_button.configure(text=" 🗖 ")
            self.parent.geometry(self.normal_size)
            self.parent.maximized = not self.parent.maximized

    def changex_on_hovering(self, event) -> None:
        self.close_button["bg"] = Colors.RED

    def returnx_to_normalstate(self, event) -> None:
        self.close_button["bg"] = self.titlebarcolor

    def change_size_on_hovering(self, event) -> None:
        self.expand_button["bg"] = Colors.LGRAY

    def return_size_on_hovering(self, event) -> None:
        self.expand_button["bg"] = self.titlebarcolor

    def changem_size_on_hovering(self, event) -> None:
        self.minimize_button["bg"] = Colors.LGRAY

    def returnm_size_on_hovering(self, event) -> None:
        self.minimize_button["bg"] = self.titlebarcolor


class App(ctk.CTk):
    def __init__(self, title="", width=400, height=200, titlebarcolor="") -> None:
        super().__init__()
        self.title(string=title)
        self.titlestring: str = title
        self.titlebarcolor: str = titlebarcolor
        self.overrideredirect(boolean=True)  # turns off title bar, geometry
        self.geom: str = f"{width}x{height}+1200+300"
        self.geometry(geometry_string=self.geom)
        self.minsize(width=width, height=height)
        # self.iconbitmap("your_icon.ico") # to show your own icon
        self.minimized = False
        self.maximized = False

        self.configure(bg=Colors.LGRAY2, borderwidth=1)
        self.titlebar = Titlebar(
            parent=self, title=self.titlestring, titlebarcolor=titlebarcolor
        )
        self.resizeSetup()

        # some settings
        self.bind(sequence="<FocusOut>", func=self.titlebar.minimize_me)
        self.bind(
            sequence="<FocusIn>", func=self.titlebar.deminimize
        )  # to view the window by clicking on the window icon on the taskbar

        self.update_idletasks()
        self.after_idle(func=self.set_appwindow)  # to see the icon on the task bar
        self.update_idletasks()
        self.deiconify()

        # self.mainloop()

    def resizeSetup(self) -> None:
        # a frame for the main area of the window, this is where the actual app will go
        self.window = ctk.CTkFrame(master=self)
        self.window.pack(
            expand=1, fill="both"
        )  # replace this with your main Canvas/Frame/etc.

        frame_size = 3
        # resize widgets
        self.resizex_widget = ctk.CTkFrame(
            master=self, cursor="sb_h_double_arrow", width=5
        )
        self.resizex_widget.place(
            relx=1, relheight=1, anchor="ne"
        )  # , ipadx=2, fill="y")
        self.resizex_widget2 = ctk.CTkFrame(
            master=self, cursor="sb_h_double_arrow", width=5
        )
        self.resizex_widget2.place(
            relx=0, relheight=1, anchor="nw"
        )  # , ipadx=2, fill="y")

        self.resizey_widget = ctk.CTkFrame(
            master=self, cursor="sb_v_double_arrow", height=5
        )
        self.resizey_widget.place(relx=0, rely=1, anchor="sw", relwidth=1)
        self.resizey_widget2 = ctk.CTkFrame(
            master=self, cursor="sb_v_double_arrow", height=5
        )
        self.resizey_widget2.place(relx=0, rely=0, anchor="nw", relwidth=1)

        corner_size = 3
        self.resizexy_widget_se = ctk.CTkFrame(
            master=self, cursor="size_nw_se", width=corner_size, height=corner_size
        )
        self.resizexy_widget_se.place(relx=1, rely=1, anchor="se")
        self.resizexy_widget_sw = ctk.CTkFrame(
            master=self, cursor="size_ne_sw", width=corner_size, height=corner_size
        )
        self.resizexy_widget_sw.place(relx=0, rely=1, anchor="sw")
        self.resizexy_widget_nw = ctk.CTkFrame(
            master=self, cursor="size_nw_se", width=corner_size, height=corner_size
        )
        self.resizexy_widget_nw.place(relx=0, rely=0, anchor="nw")
        self.resizexy_widget_ne = ctk.CTkFrame(
            master=self, cursor="size_ne_sw", width=corner_size, height=corner_size
        )
        self.resizexy_widget_ne.place(relx=1, rely=0, anchor="ne")

        self.resizex_widget.bind(
            sequence="<B1-Motion>",
            command=lambda event, arg=("x", "e"): self.resizexy(
                event=event, direction=arg
            ),
        )
        self.resizex_widget2.bind(
            sequence="<B1-Motion>",
            command=lambda event, arg=("x", "w"): self.resizexy(
                event=event, direction=arg
            ),
        )
        self.resizey_widget.bind(
            sequence="<B1-Motion>",
            command=lambda event, arg=("y", "s"): self.resizexy(
                event=event, direction=arg
            ),
        )
        self.resizey_widget2.bind(
            sequence="<B1-Motion>",
            command=lambda event, arg=("y", "n"): self.resizexy(
                event=event, direction=arg
            ),
        )
        self.resizexy_widget_se.bind(
            sequence="<B1-Motion>",
            command=lambda event, arg=("x", "y", "s", "e"): self.resizexy(
                event=event, direction=arg
            ),
        )
        self.resizexy_widget_sw.bind(
            sequence="<B1-Motion>",
            command=lambda event, arg=("x", "y", "s", "w"): self.resizexy(
                event=event, direction=arg
            ),
        )
        self.resizexy_widget_nw.bind(
            sequence="<B1-Motion>",
            command=lambda event, arg=("x", "y", "n", "w"): self.resizexy(
                event=event, direction=arg
            ),
        )
        self.resizexy_widget_ne.bind(
            sequence="<B1-Motion>",
            command=lambda event, arg=("x", "y", "n", "e"): self.resizexy(
                event=event, direction=arg
            ),
        )

    def set_appwindow(self) -> None:
        # to display the window icon on the taskbar,
        # even when using self.overrideredirect(True
        # Some WindowsOS styles, required for task bar integration
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        # Magic
        hwnd = windll.user32.GetParent(self.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

        self.wm_withdraw()
        self.after_idle(func=self.wm_deiconify)
        self.geometry(geometry_string=self.geom)

    def resizexy(self, event, direction) -> None:
        newx: int = self.winfo_x()
        newy: int = self.winfo_y()
        min_height: int = self.wm_minsize()[1]
        min_width: int = self.wm_minsize()[0]
        w: int = self.winfo_width()
        h: int = self.winfo_height()

        xdifference = 0
        ydifference = 0

        if "x" in direction:
            xwin: int = self.winfo_x()
            xdifference: int = event.x_root - xwin
            if "e" in direction:
                xdifference = xdifference - w
                if w + xdifference < min_width:
                    xdifference = min_width - w
            else:
                xdifference = -xdifference
                if w + xdifference < min_width:
                    xdifference = 0
                newx = xwin - xdifference

        if "y" in direction:
            ywin: int = self.winfo_y()
            ydifference: int = event.y_root - ywin
            if "s" in direction:
                ydifference = ydifference - h
                if h + ydifference < min_height:
                    ydifference = min_height - h
            else:
                ydifference = -ydifference
                if h + ydifference < min_height:
                    ydifference = 0
                newy = ywin - ydifference

        self.wm_geometry(
            newGeometry=f"{w + xdifference}x{h + ydifference}+{newx}+{newy}"
        )


if __name__ == "__main__":
    app = App(title="MyApp", titlebarcolor="#333333")
    app.mainloop()
