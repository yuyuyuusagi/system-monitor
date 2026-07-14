from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from monitor.system_info import SystemInfo


class MainWindow(QMainWindow):
    """System Monitorのメイン画面。"""

    UPDATE_INTERVAL_MS = 1000

    def __init__(self) -> None:
        super().__init__()

        self.system_info = SystemInfo()

        self.setWindowTitle("System Monitor")
        self.resize(360, 500)
        self.setMinimumSize(320, 420)

        self._apply_style()
        self._build_ui()
        self._start_monitoring()

    def _build_ui(self) -> None:
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        title = QLabel("System Monitor")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cpu_label, self.cpu_bar = self._create_monitor_item("CPU")
        self.memory_label, self.memory_bar = self._create_monitor_item("Memory")
        self.disk_label, self.disk_bar = self._create_monitor_item("Disk")

        self.network_title = QLabel("Network")
        self.network_title.setObjectName("itemLabel")

        self.network_value = QLabel("↑ 0.00 MB/s    ↓ 0.00 MB/s")
        self.network_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)

        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)

        layout.addWidget(self.memory_label)
        layout.addWidget(self.memory_bar)

        layout.addWidget(self.disk_label)
        layout.addWidget(self.disk_bar)

        layout.addWidget(self.network_title)
        layout.addWidget(self.network_value)

        layout.addStretch()

        self.setCentralWidget(central_widget)

    def _create_monitor_item(
        self,
        name: str,
    ) -> tuple[QLabel, QProgressBar]:
        label = QLabel(f"{name}  0%")
        label.setObjectName("itemLabel")

        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        progress_bar.setTextVisible(False)

        return label, progress_bar

    def _start_monitoring(self) -> None:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_system_info)
        self.timer.start(self.UPDATE_INTERVAL_MS)

        self._update_system_info()

    def _update_system_info(self) -> None:
        cpu_usage = round(self.system_info.get_cpu_usage())
        memory_usage = round(self.system_info.get_memory_usage())
        disk_usage = round(self.system_info.get_disk_usage())

        self.cpu_label.setText(f"CPU  {cpu_usage}%")
        self.cpu_bar.setValue(cpu_usage)

        self.memory_label.setText(f"Memory  {memory_usage}%")
        self.memory_bar.setValue(memory_usage)

        self.disk_label.setText(f"Disk  {disk_usage}%")
        self.disk_bar.setValue(disk_usage)

    def _apply_style(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow,
            QWidget {
                background-color: #111318;
                color: white;
                font-family: "Segoe UI";
            }

            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 12px;
            }

            QLabel#itemLabel {
                font-size: 15px;
                font-weight: 600;
                margin-top: 10px;
            }

            QProgressBar {
                border: 1px solid #3a3f4b;
                border-radius: 6px;
                background-color: #20242c;
                min-height: 18px;
                max-height: 18px;
            }

            QProgressBar::chunk {
                background-color: #4c8bf5;
                border-radius: 5px;
            }
            """
        )