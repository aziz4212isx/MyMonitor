# LightMonitor Pro 🚀

A modern, highly efficient, and sleek PC System Monitor built with Python and `customtkinter`. LightMonitor provides real-time tracking for your CPU, GPU, RAM, Disk, and Network usage. It is designed to be universally compatible with almost any hardware configuration and features a gaming-inspired **HUD Overlay**.

---

## 🌟 Key Features

*   **Universal Compatibility:** Automatically detects NVIDIA, AMD, or Intel GPUs. Safely hides GPU tabs if no dedicated hardware is detected. Fallback mechanisms ensure CPU temperature tracking works on most systems.
*   **Gaming HUD Overlay (Compact Mode):** A customizable, borderless, transparent, and always-on-top overlay. Keep an eye on your PC metrics while gaming!
*   **Global Hotkey:** Press `Ctrl+Alt+M` to instantly toggle the HUD Overlay from anywhere, even inside a fullscreen game.
*   **Click-Through Mode:** The HUD can be configured to ignore mouse clicks so it never interrupts your gameplay.
*   **Top 5 Resource Hogs:** Automatically tracks and displays the top 5 applications consuming the most CPU and RAM in real-time.
*   **Overheat Alerts:** Set custom temperature thresholds. If your CPU or GPU overheats, the app will trigger a Windows sound and a visual warning popup.
*   **Smart Stability (Anti-Spike & Watchdog):** Automatically handles Windows "Sleep" states to prevent network/disk speed spikes and includes a background watchdog to prevent the app from freezing.
*   **CSV Data Logging:** Silently log your PC's temperature and usage data into a CSV file for post-gaming performance analysis.
*   **Auto-Start:** Run silently in the background on Windows startup with a single click.

---

## 📥 How to Download & Run (For Users)

You don't need to install Python to use this app!

1. Go to the **[Releases](../../releases)** tab on the right side of this GitHub page.
2. Download the latest `LightMonitor.exe` file.
3. Move the `.exe` file to your preferred folder (e.g., Desktop) and double-click to run!
> *Note: If you want to use the Global Hotkey feature (`Ctrl+Alt+M`), you must right-click `LightMonitor.exe` and select **Run as Administrator**.*

---

## 🛠️ How to Build from Source (For Developers)

If you want to modify the code and compile it yourself, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aziz4212isx/MyMonitor.git
   cd MyMonitor
   ```
2. **Install Python dependencies:**
   Make sure Python is installed on your system.
   ```bash
   pip install customtkinter psutil keyboard pillow
   ```
3. **Compile to EXE:**
   Simply double-click the `build_exe.bat` file included in the repository. The script will automatically:
   - Clean old caches.
   - Bundle all python scripts and the application icon.
   - Generate a single `LightMonitor.exe` file inside the `dist/` folder.

---
*Built with ❤️ using Python.*
