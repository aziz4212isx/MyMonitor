import customtkinter as ctk
import ctypes
import platform

class CompactOverlay(ctk.CTkToplevel):
    def __init__(self, master, config_mgr):
        super().__init__(master)
        self.config_mgr = config_mgr
        self.conf = self.config_mgr.get_overlay_conf()
        
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", self.conf.get("transparency", 0.85))
        
        pos = self.conf.get("position", {"x": 100, "y": 100})
        self.geometry(f"+{pos['x']}+{pos['y']}")
        
        self.configure(fg_color="#121212")
        
        # Main Frame with rounded corners
        self.main_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1a1a1a")
        self.main_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        self._drag_start_x = 0
        self._drag_start_y = 0
        
        self.bind_drag(self.main_frame)
        
        # Dictionary to store metric value labels for quick updating
        self.metric_labels = {}
        
        # Apply Windows specific styles after window is mapped
        if platform.system() == "Windows":
            # Schedule the API call after window is drawn to ensure HWND is valid
            self.after(10, self.apply_window_styles)
        
        self.build_ui()

    def build_ui(self):
        # Clear existing
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.metric_labels.clear()

        metrics = self.conf.get("enabled_metrics", [])
        
        if not metrics:
            msg = ctk.CTkLabel(self.main_frame, text="No metrics selected", font=ctk.CTkFont(size=10, slant="italic"))
            msg.pack(padx=10, pady=10)
            self.geometry("160x50")
            return
            
        labels_map = {
            "cpu_usage": "CPU",
            "cpu_temp": "CPU Tmp",
            "cpu_freq": "CPU Clk",
            "gpu_usage": "GPU",
            "gpu_temp": "GPU Tmp",
            "vram_usage": "VRAM",
            "ram_usage": "RAM",
            "swap_usage": "Swap",
            "net_speed": "Net DL/UL",
            "disk_io": "Disk I/O"
        }
        
        for m in metrics:
            display_name = labels_map.get(m, m)
            if m.startswith("disk_usage_"):
                drive = m.split("_")[-1]
                display_name = f"Disk {drive}"
                
            self.metric_labels[m] = self._create_row(display_name, "--")
            
        # Auto-adjust height based on rows
        h = 10 + (len(metrics) * 26) # rough estimation
        self.geometry(f"160x{h}")

    def _create_row(self, label_text, val_text):
        row = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=6, height=22)
        row.pack(fill="x", padx=8, pady=2)
        row.pack_propagate(False)
        
        lbl = ctk.CTkLabel(row, text=label_text, font=ctk.CTkFont(family="Consolas", size=12, weight="bold"), text_color="#aaaaaa")
        lbl.pack(side="left", padx=5)
        
        val = ctk.CTkLabel(row, text=val_text, font=ctk.CTkFont(family="Consolas", size=12, weight="bold"), text_color="#00E5FF")
        val.pack(side="right", padx=5)
        
        def on_enter(e): row.configure(fg_color="#2a2a2a")
        def on_leave(e): row.configure(fg_color="transparent")
        row.bind("<Enter>", on_enter)
        row.bind("<Leave>", on_leave)
        
        self.bind_drag(row)
        self.bind_drag(lbl)
        self.bind_drag(val)
        
        return val

    def bind_drag(self, widget):
        widget.bind("<Button-1>", self.start_move)
        widget.bind("<B1-Motion>", self.do_move)
        widget.bind("<ButtonRelease-1>", self.stop_move)

    def start_move(self, event):
        if self.conf.get("click_through", False): return
        self._drag_start_x = event.x_root - self.winfo_x()
        self._drag_start_y = event.y_root - self.winfo_y()

    def do_move(self, event):
        if self.conf.get("click_through", False): return
        x = event.x_root - self._drag_start_x
        y = event.y_root - self._drag_start_y
        self.geometry(f"+{x}+{y}")

    def stop_move(self, event):
        if self.conf.get("click_through", False): return
        self.conf["position"] = {"x": self.winfo_x(), "y": self.winfo_y()}
        self.config_mgr.save_config()
        
    def apply_window_styles(self):
        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            # WS_EX_TOOLWINDOW = 0x00000080
            # WS_EX_LAYERED = 0x00080000
            # WS_EX_TRANSPARENT = 0x00000020
            
            ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20) # GWL_EXSTYLE
            
            # Always apply TOOLWINDOW to hide from Alt-Tab
            ex_style |= 0x00000080
            
            if self.conf.get("click_through", False):
                ex_style |= 0x00080000 | 0x00000020
            else:
                ex_style &= ~0x00000020 # Remove transparent if toggle off
                
            ctypes.windll.user32.SetWindowLongW(hwnd, -20, ex_style)
        except Exception as e:
            print(f"[Overlay] Failed to apply styles: {e}")

    def rebuild_if_needed(self):
        # Called from main app if config changes
        self.conf = self.config_mgr.get_overlay_conf()
        self.attributes("-alpha", self.conf.get("transparency", 0.85))
        self.apply_window_styles()
        self.build_ui()

    def update_data(self, d):
        def update_lbl(key, text):
            if key in self.metric_labels:
                # Update text directly without stealing focus or forcing geometry
                self.metric_labels[key].configure(text=text)

        update_lbl("cpu_usage", f"{d.cpu_use}%")
        update_lbl("cpu_temp", f"{d.cpu_temp}°C")
        update_lbl("cpu_freq", f"{d.cpu_freq} MHz")
        
        gpu_val = f"{d.gpu_use}%" if d.gpu_use != "--" else "N/A"
        update_lbl("gpu_usage", gpu_val)
        
        gpu_t = f"{d.gpu_temp}°C" if d.gpu_temp != "--" else "N/A"
        update_lbl("gpu_temp", gpu_t)
        
        vram_val = f"{d.gpu_mem} MB" if d.gpu_mem != "--" else "N/A"
        update_lbl("vram_usage", vram_val)
        
        update_lbl("ram_usage", f"{d.ram_pct}%")
        update_lbl("swap_usage", f"{d.swap_pct}%")
        
        net_speed = f"{d.dl_speed:.0f}/{d.ul_speed:.0f} KB"
        update_lbl("net_speed", net_speed)
        
        if "GLOBAL_IO" in d.disk_data:
            gio = d.disk_data["GLOBAL_IO"]
            update_lbl("disk_io", f"{gio['read']:.1f}/{gio['write']:.1f} MB")
            
        for key, val in d.disk_data.items():
            if key != "GLOBAL_IO":
                update_lbl(f"disk_usage_{key}", f"{val['pct']}%")
