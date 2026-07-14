from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from monitor.system_info import SystemInfo
from ui.history_graph import HistoryGraphCard


class MainWindow(QMainWindow):
    """PulseDeskのメイン画面。"""

    UPDATE_INTERVAL_MS = 1000

    def __init__(self) -> None:
        super().__init__()

        self.system_info = SystemInfo()

        self.setWindowTitle("PulseDesk")
        self.resize(440, 820)
        self.setMinimumSize(400, 700)

        self._apply_style()
        self._build_ui()
        self._start_monitoring()

    def _build_ui(self) -> None:
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        title = QLabel("PulseDesk")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Your PC, at a glance")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cpu_label, self.cpu_bar, cpu_card = self._create_usage_card(
            "CPU",
            "Processor usage",
        )

        self.memory_label, self.memory_bar, memory_card = (
            self._create_usage_card(
                "Memory",
                "System memory usage",
            )
        )

        self.disk_label, self.disk_bar, disk_card = self._create_usage_card(
            "Disk",
            "System drive usage",
        )

        self.network_value, network_card = self._create_network_card()

        self.history_graph = HistoryGraphCard()

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(8)
        main_layout.addWidget(cpu_card)
        main_layout.addWidget(memory_card)
        main_layout.addWidget(disk_card)
        main_layout.addWidget(network_card)
        main_layout.addWidget(self.history_graph)
        main_layout.addStretch()

        self.setCentralWidget(central_widget)

    def _create_usage_card(
        self,
        title_text: str,
        description_text: str,
    ) -> tuple[QLabel, QProgressBar, QFrame]:
        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(10)

        header_layout = QHBoxLayout()

        title = QLabel(title_text)
        title.setObjectName("cardTitle")

        value_label = QLabel("0%")
        value_label.setObjectName("cardValue")
        value_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        description = QLabel(description_text)
        description.setObjectName("cardDescription")

        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        progress_bar.setTextVisible(False)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(value_label)

        card_layout.addLayout(header_layout)
        card_layout.addWidget(description)
        card_layout.addWidget(progress_bar)

        return value_label, progress_bar, card

    def _create_network_card(self) -> tuple[QLabel, QFrame]:
        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(10)

        title = QLabel("Network")
        title.setObjectName("cardTitle")

        description = QLabel("Realtime upload and download speed")
        description.setObjectName("cardDescription")

        network_value = QLabel(
            "↑ 0.00 MB/s    ↓ 0.00 MB/s"
        )
        network_value.setObjectName("networkValue")
        network_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_layout.addWidget(title)
        card_layout.addWidget(description)
        card_layout.addWidget(network_value)

        return network_value, card

    def _start_monitoring(self) -> None:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_system_info)
        self.timer.start(self.UPDATE_INTERVAL_MS)

        self._update_system_info()

    def _update_system_info(self) -> None:
        cpu_usage = round(self.system_info.get_cpu_usage())
        memory_usage = round(self.system_info.get_memory_usage())
        disk_usage = round(self.system_info.get_disk_usage())

        upload_speed, download_speed = (
            self.system_info.get_network_speed()
        )

        self.cpu_label.setText(f"{cpu_usage}%")
        self.cpu_bar.setValue(cpu_usage)

        self.memory_label.setText(f"{memory_usage}%")
        self.memory_bar.setValue(memory_usage)

        self.disk_label.setText(f"{disk_usage}%")
        self.disk_bar.setValue(disk_usage)

        self.network_value.setText(
            f"↑ {upload_speed:.2f} MB/s    "
            f"↓ {download_speed:.2f} MB/s"
        )

        self.history_graph.update_values(
            cpu_usage,
            memory_usage,
        )

    def _apply_style(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow,
            QWidget {
                background-color: #0f1117;
                color: #f5f7fa;
                font-family: "Segoe UI";
            }

            QLabel#title {
                font-size: 28px;
                font-weight: 700;
            }

            QLabel#subtitle {
                color: #8f98a8;
                font-size: 13px;
                margin-bottom: 4px;
            }

            QFrame#card {
                background-color: #191d26;
                border: 1px solid #2a303d;
                border-radius: 14px;
            }

            QLabel#cardTitle {
                font-size: 17px;
                font-weight: 700;
            }

            QLabel#cardValue {
                font-size: 22px;
                font-weight: 700;
                color: #72a7ff;
            }

            QLabel#cardDescription {
                color: #8f98a8;
                font-size: 12px;
            }

            QLabel#networkValue {
                background-color: #11151c;
                border: 1px solid #2a303d;
                border-radius: 9px;
                padding: 12px;
                font-size: 15px;
                font-weight: 600;
            }

            QProgressBar {
                background-color: #11151c;
                border: none;
                border-radius: 7px;
                min-height: 14px;
                max-height: 14px;
            }

            QProgressBar::chunk {
                background-color: #4c8bf5;
                border-radius: 7px;
            }
            """
        )