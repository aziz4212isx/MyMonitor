import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

# Backend imports
from config_manager import ConfigManager
from cpu_temp_utils import CPUTempFetcher
from gpu_utils import GPUFetcher

# Data structures
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class SystemData:
    uptime: str = "--"
    cpu_use: float = 0.0
    cpu_temp: str = "--"
    cpu_freq: str = "--"
    cpu_cores: List[float] = field(default_factory=list)
    
    gpu_name: str = "--"
    gpu_use: str = "--"
    gpu_temp: str = "--"
    gpu_mem: str = "--"
    gpu_pow: str = "--"
    gpu_pow_limit: str = "--"
    top5_cpu: List[str] = field(default_factory=list)
    top5_ram: List[str] = field(default_factory=list)
    gpu_c_clock: str = "--"
    gpu_m_clock: str = "--"
    gpu_fan: str = "--"
    
    ram_pct: float = 0.0
    ram_used: float = 0.0
    ram_total: float = 0.0
    swap_pct: float = 0.0
    
    disk_data: Dict[str, dict] = field(default_factory=dict)
    
    dl_speed: float = 0.0
    ul_speed: float = 0.0
    net_tot_dl: float = 0.0
    net_tot_ul: float = 0.0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LightMonitor Pro V2 (Qt)")
        self.resize(600, 750)
        
        # Load stylesheet
        try:
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading QSS: {e}")

        # Central Widget & Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title_lbl = QLabel("System Monitor")
        title_lbl.setObjectName("TitleLabel")
        layout.addWidget(title_lbl)

        # Tab Widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # 5 Tabs
        self.tab_overview = QWidget()
        self.tab_cpu = QWidget()
        self.tab_gpu = QWidget()
        self.tab_storage = QWidget()
        self.tab_settings = QWidget()
        
        self.tabs.addTab(self.tab_overview, "Overview")
        self.tabs.addTab(self.tab_cpu, "CPU")
        self.tabs.addTab(self.tab_gpu, "GPU")
        self.tabs.addTab(self.tab_storage, "Storage & Network")
        self.tabs.addTab(self.tab_settings, "Settings")

        # Placeholders
        for tab in [self.tab_overview, self.tab_cpu, self.tab_gpu, self.tab_storage, self.tab_settings]:
            l = QVBoxLayout(tab)
            lbl = QLabel("Placeholder for " + self.tabs.tabText(self.tabs.indexOf(tab)))
            lbl.setAlignment(Qt.AlignCenter)
            l.addWidget(lbl)

        # Test backend imports
        self.config_mgr = ConfigManager()
        self.cpu_fetcher = CPUTempFetcher()
        self.gpu_fetcher = GPUFetcher()
        print("Backend initialized successfully")

if __name__ == "__main__":
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
