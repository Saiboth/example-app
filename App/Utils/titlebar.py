import tkinter as tk
from ctypes import windll

class Colors:
    LGRAY = '#3e4042' # button color effects in the title bar (Hex color)
    LGRAY2 = '#3a3a3a' #3a3a3a
    DGRAY = '#0d1117' # window background color               (Hex color)
    RGRAY = '#0e0e0e' # title bar color                       (Hex color)
    RED = '#ae0d1a'

class Titlebar(tk.Frame):
    def __init__(self, parent=None, title="") -> None:
        super().__init__()
        self.config(bg=Colors.RGRAY, relief='raised', bd=0, highlightthickness=0)
        self.parent = parent

        # put a close button on the title bar
        self.close_button = tk.Button(self, text='  ×  ', command=parent.destroy,bg=Colors.RGRAY,padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
        self.expand_button = tk.Button(self, text=' 🗖 ', command=self.maximize_me,bg=Colors.RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
        self.minimize_button = tk.Button(self, text=' ⎯ ',command=self.minimize_me,bg=Colors.RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
        self.title = tk.Label(self, text=title, bg=Colors.RGRAY,bd=0,fg='white',font=("helvetica", 10),highlightthickness=0, padx=5)

        # pack the widgets
        self.pack(fill="x")
        self.close_button.pack(side="right", ipadx=7, ipady=1)
        self.expand_button.pack(side="right", ipadx=7, ipady=1)
        self.minimize_button.pack(side="right", ipadx=7, ipady=1)
        self.title.pack(side="left", padx=10)

        # bind title bar motion to the move window function
        # self.bind('<Button-1>', self.get_pos) # so you can drag the window from the title bar
        # self.title.bind('<Button-1>', self.get_pos) # so you can drag the window from the title 
        self.bind('<Double-Button-1>', self.maximize_me)

        # button effects in the title bar when hovering over buttons
        self.close_button.bind('<Enter>', self.changex_on_hovering)
        self.close_button.bind('<Button-1>', self.changex_on_click)
        self.close_button.bind('<Leave>',self.returnx_to_normalstate)
        self.expand_button.bind('<Enter>', self.change_size_on_hovering)
        self.expand_button.bind('<Leave>', self.return_size_on_hovering)
        self.minimize_button.bind('<Enter>', self.changem_size_on_hovering)
        self.minimize_button.bind('<Leave>', self.returnm_size_on_hovering)

        self.bindMove(self)
        self.bindMove(self.title)

    def bindMove(self, widget):
        w = self
        if widget:
            w = widget
        w.bind("<Button-1>", lambda event, arg=w: self.startMove(event, arg))
        w.bind("<ButtonRelease-1>", lambda event, arg=w: self.stopMove(event, arg))
        w.bind("<B1-Motion>", lambda event, arg=w: self.moving(event, arg))

        # self.bind("<Map>",self.frame_mapped)

    def startMove(self, event, w):
        if self.parent.maximized == True:
            locx = int(event.x/self.get_geometry_xy(self.parent.geometry())[0] * self.get_geometry_xy(self.normal_size)[0])
            locy = int(event.y/self.get_geometry_xy(self.parent.geometry())[1] * self.get_geometry_xy(self.normal_size)[1])
            w.x = locx
            w.y = locy
            self.maximize_me()
            self.expand_button.config(text=" 🗖 ")
        else:
            w.x = event.x
            w.y = event.y

    def stopMove(self, event, w):
        w.x = None
        w.y = None

    def moving(self, event, w):
        x = (event.x_root - w.x - w.winfo_rootx() + self.winfo_rootx())
        y = (event.y_root - w.y - w.winfo_rooty() + self.winfo_rooty())
        self.parent.geometry("+%s+%s" % (x, y))

    def get_geometry_xy(self, geom):
        xy = geom.split("+")[0]
        return [int(val) for val in xy.split("x")]

    def minimize_me(self, event=None):
        if self.parent.minimized == False:
            self.parent.update_idletasks()
            self.parent.overrideredirect(False)
            self.parent.unbind("<FocusOut>")
            self.parent.update_idletasks()
            self.parent.after_idle(self.iconify)

            # self.set_appwindow()
            self.parent.minimized = True       

    def iconify(self):
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
            self.parent.attributes("-alpha",1) # so you can see the window when is not minimized
            self.parent.after_idle(lambda: self.bind("<FocusOut>", self.minimize_me))
            self.parent.minimized = False                              

    def maximize_me(self, *args):
        if self.parent.maximized == False: # if the window was not maximized
            self.normal_size = self.parent.geometry()
            self.expand_button.config(text=" 🗗 ")
            self.parent.geometry(f"{self.parent.winfo_screenwidth()}x{self.parent.winfo_screenheight()}+0+0")
            self.parent.maximized = not self.parent.maximized 
            # now it's maximized
            
        else: # if the window was maximized
            self.expand_button.config(text=" 🗖 ")
            self.parent.geometry(self.normal_size)
            self.parent.maximized = not self.parent.maximized
            # now it is not maximized

    def changex_on_hovering(self, event):
        self.close_button['bg']=Colors.RED
        
    def changex_on_click(self, event):
        self.close_button['bg']='#f16f7a'
        
    def returnx_to_normalstate(self, event):
        self.close_button['bg']=Colors.RGRAY
        
    def change_size_on_hovering(self, event):
        self.expand_button['bg']=Colors.LGRAY
        
    def return_size_on_hovering(self, event):
        self.expand_button['bg']=Colors.RGRAY
        
    def changem_size_on_hovering(self, event):
        self.minimize_button['bg']=Colors.LGRAY
        
    def returnm_size_on_hovering(self, event):
        self.minimize_button['bg']=Colors.RGRAY

class App(tk.Tk):
    def __init__(self, title="") -> None:
        super().__init__()
        self.title(title) 
        self.title = title
        self.overrideredirect(True) # turns off title bar, geometry
        self.geometry('200x200+1200+300')
        self.minsize(width=200, height=200)
        # self.iconbitmap("your_icon.ico") # to show your own icon 
        self.minimized = False
        self.maximized = False

        self.config(bg=Colors.LGRAY2, borderwidth=1)
        self.titlebar = Titlebar(self, self.title)
        self.resizeSetup()

        # some settings
        self.bind("<FocusOut>", self.titlebar.minimize_me)
        self.bind("<FocusIn>", self.titlebar.deminimize) # to view the window by clicking on the window icon on the taskbar
        self.after_idle(self.set_appwindow) # to see the icon on the task bar

        self.mainloop()

    def resizeSetup(self):
        # a frame for the main area of the window, this is where the actual app will go
        self.window = tk.Frame(self, bg=Colors.DGRAY, highlightthickness=0)
        
        # resize widgets
        self.resizex_widget = tk.Frame(self.window, bg="white", cursor="sb_h_double_arrow")
        self.resizex_widget.pack(side="right", ipadx=2, fill="y")
        # self.resizex_widget2 = tk.Frame(self.window, bg="white", cursor="sb_h_double_arrow")
        # self.resizex_widget2.pack(side="left", ipadx=2, fill="y")

        self.resizey_widget = tk.Frame(self.window,bg="white", cursor='sb_v_double_arrow')
        self.resizey_widget.place(relx=0, rely=1, anchor="sw", relwidth=1, height=5)
        # self.resizey_widget2 = tk.Frame(self, bg="white", cursor='sb_v_double_arrow')
        # self.resizey_widget2.place(relx=0, rely=0, anchor="nw", relwidth=1, height=5)

        self.resizexy_widget = tk.Frame(self.window,bg="white", cursor='size_nw_se')
        self.resizexy_widget.place(relx=1, rely=1, anchor="se", width=10, height=10)


        self.window.pack(expand=1, fill="both") # replace this with your main Canvas/Frame/etc.
        #xwin=None
        #ywin=None



        self.resizex_widget.bind("<B1-Motion>",self.resizex)
        # self.resizex_widget2.bind("<B1-Motion>",self.resizex)
        self.resizey_widget.bind("<B1-Motion>",self.resizey)
        # self.resizey_widget2.bind("<B1-Motion>",self.resizey)
        self.resizexy_widget.bind("<B1-Motion>",self.resizexy)

    def set_appwindow(self): # to display the window icon on the taskbar, 
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

    def resizex(self, event):
        xwin = self.winfo_x()
        difference = (event.x_root - xwin) - self.winfo_width()
        
        if self.winfo_width() > 150 : # 150 is the minimum width for the window
            try:
                self.geometry(f"{ self.winfo_width() + difference }x{ self.winfo_height() }")
            except:
                pass
        else:
            if difference > 0: # so the window can't be too small (150x150)
                try:
                    self.geometry(f"{ self.winfo_width() + difference }x{ self.winfo_height() }")
                except:
                    pass
                
        # resizex_widget.config(bg=DGRAY)

    def resizey(self, event):
        ywin = self.winfo_y()
        difference = (event.y_root - ywin) - self.winfo_height()

        if self.winfo_height() > 150: # 150 is the minimum height for the window
            try:
                self.geometry(f"{ self.winfo_width()  }x{ self.winfo_height() + difference}")
            except:
                pass
        else:
            if difference > 0: # so the window can't be too small (150x150)
                try:
                    self.geometry(f"{ self.winfo_width()  }x{ self.winfo_height() + difference}")
                except:
                    pass

        # resizey_widget.config(bg=DGRAY)

    def resizexy(self, event):
        xwin = self.winfo_x()
        xdifference = (event.x_root - xwin) - self.winfo_width()
        ywin = self.winfo_y()
        ydifference = (event.y_root - ywin) - self.winfo_height()

        if self.winfo_width() > 150 : # 150 is the minimum width for the window
            try:
                self.geometry(f"{ self.winfo_width() + xdifference }x{ self.winfo_height() + ydifference}")
            except:
                pass
        else:
            if xdifference > 0: # so the window can't be too small (150x150)
                try:
                    self.geometry(f"{ self.winfo_width() + xdifference }x{ self.winfo_height() + ydifference}")
                except:
                    pass
        if self.winfo_height() > 150: # 150 is the minimum height for the window
            try:
                self.geometry(f"{ self.winfo_width()  + xdifference}x{ self.winfo_height() + ydifference}")
            except:
                pass
        else:
            if ydifference > 0: # so the window can't be too small (150x150)
                try:
                    self.geometry(f"{ self.winfo_width()  + xdifference}x{ self.winfo_height() + ydifference}")
                except:
                    pass

        # resizexy_widget.config(bg=DGRAY)

if __name__ == "__main__":
    App(title="MyApp")