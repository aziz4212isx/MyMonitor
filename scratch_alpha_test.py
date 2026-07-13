import customtkinter as ctk

app = ctk.CTk()
app.geometry("400x300")
app.title("Main Window")

# Background Window
bg_win = ctk.CTkToplevel(app)
bg_win.overrideredirect(True)
bg_win.attributes("-topmost", True)
bg_win.attributes("-alpha", 0.3)
bg_frame = ctk.CTkFrame(bg_win, fg_color="#333333", corner_radius=15)
bg_frame.pack(fill="both", expand=True)

# Foreground (Text) Window
fg_win = ctk.CTkToplevel(app)
fg_win.overrideredirect(True)
fg_win.attributes("-topmost", True)
# Windows-specific transparent color key
TRANSPARENT_COLOR = "#000001"
fg_win.attributes("-transparentcolor", TRANSPARENT_COLOR)
fg_win.configure(fg_color=TRANSPARENT_COLOR)
fg_frame = ctk.CTkFrame(fg_win, fg_color=TRANSPARENT_COLOR, corner_radius=15)
fg_frame.pack(fill="both", expand=True)

lbl = ctk.CTkLabel(fg_frame, text="OPAQUE TEXT on SEMI-TRANSPARENT BG", font=("Arial", 16, "bold"), text_color="#00FF00")
lbl.pack(padx=20, pady=20)

# Sync geometries
def sync_geometry(*args):
    bg_win.geometry(f"{fg_win.winfo_width()}x{fg_win.winfo_height()}+{fg_win.winfo_x()}+{fg_win.winfo_y()}")

fg_win.bind("<Configure>", sync_geometry)

# Dragging logic on fg_win
drag_x = 0
drag_y = 0
def start_drag(e):
    global drag_x, drag_y
    drag_x = e.x
    drag_y = e.y
def do_drag(e):
    x = fg_win.winfo_x() + e.x - drag_x
    y = fg_win.winfo_y() + e.y - drag_y
    fg_win.geometry(f"+{x}+{y}")
    sync_geometry()

lbl.bind("<Button-1>", start_drag)
lbl.bind("<B1-Motion>", do_drag)
fg_frame.bind("<Button-1>", start_drag)
fg_frame.bind("<B1-Motion>", do_drag)

fg_win.geometry("350x100+200+200")

app.mainloop()
