import tkinter as tk
from ctypes import windll

class Colors:
    LGRAY = '#3e4042' # button color effects in the title bar (Hex color)
    LGRAY2 = '#3a3a3a' #3a3a3a
    DGRAY = '#0d1117' # window background color               (Hex color)
    RGRAY = '#0e0e0e' # title bar color                       (Hex color)
    RED = '#ae0d1a'

class Titlebar(tk.Frame):
    def __init__(self, parent=None, title="", titlebarcolor=Colors.DGRAY) -> None:
        super().__init__()
        self.config(bg=titlebarcolor, relief='raised', bd=0, highlightthickness=0)
        self.parent = parent
        self.titlebarcolor = titlebarcolor

        # add buttons to the title bar
        self.title = tk.Label(self, text=title, bg=self.titlebarcolor,bd=0,fg='white',font=("helvetica", 10),highlightthickness=0, padx=5)
        self.close_button = tk.Button(self, text='  ×  ', command=parent.destroy,bg=self.titlebarcolor,padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
        self.expand_button = tk.Button(self, text=' 🗖 ', command=self.maximize_me,bg=self.titlebarcolor,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
        self.minimize_button = tk.Button(self, text=' ⎯ ',command=self.minimize_me,bg=self.titlebarcolor,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)

        # pack the widgets
        self.title.pack(side="left", padx=10)
        self.close_button.pack(side="right", ipadx=7, ipady=1)
        self.expand_button.pack(side="right", ipadx=7, ipady=1)
        self.minimize_button.pack(side="right", ipadx=7, ipady=1)
        self.pack(fill="x")

        # bind double click to maximize method
        self.bind('<Double-Button-1>', self.maximize_me)

        # hover effects for buttons
        self.close_button.bind('<Enter>', self.changex_on_hovering)
        self.close_button.bind('<Leave>',self.returnx_to_normalstate)
        self.expand_button.bind('<Enter>', self.change_size_on_hovering)
        self.expand_button.bind('<Leave>', self.return_size_on_hovering)
        self.minimize_button.bind('<Enter>', self.changem_size_on_hovering)
        self.minimize_button.bind('<Leave>', self.returnm_size_on_hovering)

        # bind move to frame and label
        self.bindMove(self)
        self.bindMove(self.title)

    def bindMove(self, widget):
        w = self
        if widget:
            w = widget
        w.bind("<Button-1>", lambda event, arg=w: self.startMove(event, arg))
        w.bind("<B1-Motion>", lambda event, arg=w: self.moving(event, arg))

        # self.bind("<Map>",self.frame_mapped)

    def startMove(self, event, w):
        # get relative click position when maximized and return to old size on drag
        if self.parent.maximized == True:
            normalx, normaly = self.get_geometry_xy(self.normal_size)
            maxx, maxy = self.get_geometry_xy(self.parent.geometry())
            locx = int(event.x/ maxx * normalx)
            locy = int(event.y/ maxy * normaly)
            w.x = locx
            w.y = locy
            self.maximize_me()
            self.expand_button.config(text=" 🗖 ")
        else:
            w.x = event.x
            w.y = event.y

    def moving(self, event, w):
        x = (event.x_root - w.x - w.winfo_rootx() + self.winfo_rootx())
        y = (event.y_root - w.y - w.winfo_rooty() + self.winfo_rooty())
        self.parent.geometry(f"+{x}+{y}")

    def get_geometry_xy(self, geom):
        xy = geom.split("+")[0]
        return [int(val) for val in xy.split("x")]

    def minimize_me(self, event=None):
        if self.parent.minimized == False:
            self.parent.update_idletasks()
            self.parent.overrideredirect(False)
            self.parent.unbind("<FocusOut>")
            self.parent.update_idletasks()
            self.parent.after_idle(self.safe_iconify)
            self.parent.minimized = True       

    def safe_iconify(self):
        try:
            self.parent.iconify()
        except tk.TclError: 
            pass

    def deminimize(self, event):
        if self.parent.minimized == True:
            self.parent.iconify()
            self.parent.overrideredirect(True)
            self.parent.set_appwindow()
            self.parent.deiconify()
            self.parent.focus()
            self.parent.after_idle(lambda: self.bind("<FocusOut>", self.minimize_me))
            self.parent.minimized = False                              

    def maximize_me(self, *args):
        if self.parent.maximized == False:
            self.normal_size = self.parent.geometry()
            self.expand_button.config(text=" 🗗 ")
            self.parent.geometry(f"{self.parent.winfo_screenwidth()}x{self.parent.winfo_screenheight()}+0+0")
            self.parent.maximized = not self.parent.maximized 
            
        else:
            self.expand_button.config(text=" 🗖 ")
            self.parent.geometry(self.normal_size)
            self.parent.maximized = not self.parent.maximized

    def changex_on_hovering(self, event):
        self.close_button['bg']=Colors.RED
        
    def returnx_to_normalstate(self, event):
        self.close_button['bg']=self.titlebarcolor
        
    def change_size_on_hovering(self, event):
        self.expand_button['bg']=Colors.LGRAY
        
    def return_size_on_hovering(self, event):
        self.expand_button['bg']=self.titlebarcolor
        
    def changem_size_on_hovering(self, event):
        self.minimize_button['bg']=Colors.LGRAY
        
    def returnm_size_on_hovering(self, event):
        self.minimize_button['bg']=self.titlebarcolor

class App(tk.Tk):
    def __init__(self, title="", width=400, height=200, titlebarcolor=Colors.DGRAY) -> None:
        super().__init__()
        self.title(title) 
        self.title = title
        self.titlebarcolor = titlebarcolor
        self.overrideredirect(True) # turns off title bar, geometry
        self.geom = f'{width}x{height}+1200+300'
        self.geometry(self.geom)
        self.minsize(width=width, height=height)
        # self.iconbitmap("your_icon.ico") # to show your own icon 
        self.minimized = False
        self.maximized = False

        self.config(bg=Colors.LGRAY2, borderwidth=1)
        self.titlebar = Titlebar(self, self.title, titlebarcolor)
        self.resizeSetup()

        # some settings
        self.bind("<FocusOut>", self.titlebar.minimize_me)
        self.bind("<FocusIn>", self.titlebar.deminimize) # to view the window by clicking on the window icon on the taskbar

        self.update_idletasks()
        self.after_idle(self.set_appwindow) # to see the icon on the task bar
        self.update_idletasks()
        self.deiconify()

        self.mainloop()

    def resizeSetup(self):
        # a frame for the main area of the window, this is where the actual app will go
        self.window = tk.Frame(self, bg=Colors.DGRAY, highlightthickness=0)
        self.window.pack(expand=1, fill="both") # replace this with your main Canvas/Frame/etc.

        frame_size = 3
        # resize widgets
        self.resizex_widget = tk.Frame(self, bg=self.titlebarcolor, cursor="sb_h_double_arrow")
        self.resizex_widget.place(relx=1, relheight=1, anchor="ne", width=5)#, ipadx=2, fill="y")
        self.resizex_widget2 = tk.Frame(self, bg=self.titlebarcolor, cursor="sb_h_double_arrow")
        self.resizex_widget2.place(relx=0, relheight=1, anchor="nw", width=5)#, ipadx=2, fill="y")

        self.resizey_widget = tk.Frame(self,bg=self.titlebarcolor, cursor='sb_v_double_arrow')
        self.resizey_widget.place(relx=0, rely=1, anchor="sw", relwidth=1, height=5)
        self.resizey_widget2 = tk.Frame(self, bg=self.titlebarcolor, cursor='sb_v_double_arrow')
        self.resizey_widget2.place(relx=0, rely=0, anchor="nw", relwidth=1, height=5)

        corner_size = 3
        self.resizexy_widget_se = tk.Frame(self, bg=self.titlebarcolor, cursor='size_nw_se')
        self.resizexy_widget_se.place(relx=1, rely=1, anchor="se", width=corner_size, height=corner_size)
        self.resizexy_widget_sw = tk.Frame(self, bg=self.titlebarcolor, cursor='size_ne_sw')
        self.resizexy_widget_sw.place(relx=0, rely=1, anchor="sw", width=corner_size, height=corner_size)
        self.resizexy_widget_nw = tk.Frame(self, bg=self.titlebarcolor, cursor='size_nw_se')
        self.resizexy_widget_nw.place(relx=0, rely=0, anchor="nw", width=corner_size, height=corner_size)
        self.resizexy_widget_ne = tk.Frame(self, bg=self.titlebarcolor, cursor='size_ne_sw')
        self.resizexy_widget_ne.place(relx=1, rely=0, anchor="ne", width=corner_size, height=corner_size)

        self.resizex_widget.bind("<B1-Motion>", lambda event, arg=("x","e"): self.resizexy(event, arg))
        self.resizex_widget2.bind("<B1-Motion>", lambda event, arg=("x","w"): self.resizexy(event, arg))
        self.resizey_widget.bind("<B1-Motion>", lambda event, arg=("y","s"): self.resizexy(event, arg))
        self.resizey_widget2.bind("<B1-Motion>", lambda event, arg=("y","n"): self.resizexy(event, arg))
        self.resizexy_widget_se.bind("<B1-Motion>", lambda event, arg=("x","y","s","e"): self.resizexy(event, arg))
        self.resizexy_widget_sw.bind("<B1-Motion>", lambda event, arg=("x","y","s","w"): self.resizexy(event, arg))
        self.resizexy_widget_nw.bind("<B1-Motion>", lambda event, arg=("x","y","n","w"): self.resizexy(event, arg))
        self.resizexy_widget_ne.bind("<B1-Motion>", lambda event, arg=("x","y","n","e"): self.resizexy(event, arg))

    def set_appwindow(self): 
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
        self.after_idle(self.wm_deiconify)
        self.geometry(self.geom)

    def resizexy(self, event, direction):
        newx = self.winfo_x()
        newy = self.winfo_y()

        if "x" in direction:
            xwin = self.winfo_x()
            xdifference = event.x_root - xwin
            if "e" in direction:
                xdifference = xdifference - self.winfo_width()
                if self.winfo_width() + xdifference < self.minsize()[0]:
                    xdifference = self.minsize()[0] - self.winfo_width()
            else:
                xdifference = -xdifference
                if self.winfo_width() + xdifference < self.minsize()[0]:
                    xdifference = 0
                newx = self.winfo_x() - xdifference
        else:
            xdifference = 0

        if "y" in direction:
            ywin = self.winfo_y()
            ydifference = event.y_root - ywin
            if "s" in direction:
                ydifference = ydifference - self.winfo_height()
                if self.winfo_height() + ydifference < self.minsize()[1]:
                    ydifference =  self.minsize()[1] - self.winfo_height()
            else:
                ydifference = -ydifference
                if self.winfo_height() + ydifference < self.minsize()[1]:
                    ydifference = 0
                newy = self.winfo_y() - ydifference
        else:
            ydifference = 0

        self.geometry(f"{ self.winfo_width() + xdifference}x{ self.winfo_height() + ydifference}+{newx}+{newy}")


if __name__ == "__main__":
    App(title="MyApp", titlebarcolor="#333333")