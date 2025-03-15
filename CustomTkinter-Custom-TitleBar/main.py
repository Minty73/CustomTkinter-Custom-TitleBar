from customtkinter import *
from PIL import Image
import ctypes
from ctypes import *
import cProfile

set_appearance_mode("dark")

maximized = False #Window maximaze mode for function
move_set_x = 0 #Cursor position in window X
move_set_y = 0 #Cursor position in window Y
bg = "gray15" #App background

minimized = False

def move(e): #Window moving function
    root.geometry(f"+{e.x_root-move_set_x}+{e.y_root-move_set_y}")

def setmove(e): #Cursor position in window function
    global move_set_x, move_set_y
    move_set_x = e.x_root - root.winfo_x()
    move_set_y = e.y_root - root.winfo_y()

def max_min(e=None):
    global maximized
    root.attributes("-alpha", 0)
    if maximized == False:
        maximize_btn.configure(image=minimize_icon)
        maximized = True
        root.wm_overrideredirect(0)
        root.attributes("-fullscreen", 1)
    else:
        maximize_btn.configure(image=maximize_icon)
        maximized = False
        root.attributes("-fullscreen", 0)
        root.wm_overrideredirect(1)
    root.attributes("-alpha", 1)
    set_appwindow(root)

def hide(e=None):
    global minimized
    minimized = True
    root.attributes("-alpha", 0)

def unhide(e):
    global minimized
    if minimized == True:
        minimized = False
    root.attributes("-alpha", 1)

#Main window
root = CTk()
root.iconbitmap("Images/icon.ico")
root.wm_overrideredirect(1)
root.geometry("600x400+100+100")
root.title("CustomTkinter Custom Title Bar")
root.configure(fg_color=bg)

def set_appwindow(mainWindow):
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())

#Programm images
close_icon = CTkImage(dark_image=Image.open("Images/close.png"), size=(17, 17))
hide_icon = CTkImage(dark_image=Image.open("Images/hide.png"), size=(17, 17))
maximize_icon = CTkImage(dark_image=Image.open("Images/maximize.png"), size=(17, 17))
minimize_icon = CTkImage(dark_image=Image.open("Images/minimize.png"), size=(17, 17))
icon_icon = CTkImage(dark_image=Image.open("Images/icon.png"), size=(19, 19))

#Title bar
titlebar = CTkFrame(root, corner_radius=0)
titlebar.pack(side=TOP, fill=X)

#Window icon label
icon = CTkLabel(titlebar, text="", image=icon_icon)
icon.pack(side=LEFT, padx=(8, 0), pady=5)

#Window title label
title = CTkLabel(titlebar, text=root.title(), font=("Century Gothic", 13, "bold"))
title.pack(side=LEFT, padx=(6, 0), pady=5)

#Buttons in titlebar
close_btn = CTkButton(titlebar, command=root.destroy, text=None, image=close_icon, fg_color="transparent", hover_color="red", corner_radius=0, width=40)
close_btn.pack(fill=Y, side=RIGHT)
maximize_btn = CTkButton(titlebar, command=max_min, text=None, image=maximize_icon, fg_color="transparent", hover_color="#515151", corner_radius=0, width=40)
maximize_btn.pack(fill=Y, side=RIGHT)
hide_btn = CTkButton(titlebar, command=hide, text=None, image=hide_icon, fg_color="transparent", hover_color="#515151", corner_radius=0, width=40)
hide_btn.pack(fill=Y, side=RIGHT)

#Move bind
titlebar.bind("<ButtonPress-1>", setmove)
titlebar.bind("<B1-Motion>", move)
title.bind("<ButtonPress-1>", setmove)
title.bind("<B1-Motion>", move)
icon.bind("<ButtonPress-1>", setmove)
icon.bind("<B1-Motion>", move)

root.bind("<FocusIn>", unhide)

#Add app to taskbar with overrideredirect
root.after(10, lambda: set_appwindow(root))

#App loop
cProfile.run("root.mainloop()")