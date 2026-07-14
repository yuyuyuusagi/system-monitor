import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar,
)
from PySide6.QtCore import Qt


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("System Monitor")
window.resize(360, 500)

window.setStyleSheet("""
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
        margin-top: 10px;
    }

    QProgressBar {
        border: 1px solid #3a3f4b;
        border-radius: 6px;
        background-color: #20242c;
        height: 18px;
        text-align: center;
    }

    QProgressBar::chunk {
        background-color: #4c8bf5;
        border-radius: 5px;
    }
""")

layout = QVBoxLayout()
layout.setContentsMargins(24, 24, 24, 24)
layout.setSpacing(10)

title = QLabel("System Monitor")
title.setObjectName("title")
title.setAlignment(Qt.AlignmentFlag.AlignCenter)

cpu_label = QLabel("CPU")
cpu_label.setObjectName("itemLabel")
cpu_bar = QProgressBar()
cpu_bar.setRange(0, 100)
cpu_bar.setValue(25)

memory_label = QLabel("Memory")
memory_label.setObjectName("itemLabel")
memory_bar = QProgressBar()
memory_bar.setRange(0, 100)
memory_bar.setValue(48)

disk_label = QLabel("Disk")
disk_label.setObjectName("itemLabel")
disk_bar = QProgressBar()
disk_bar.setRange(0, 100)
disk_bar.setValue(34)

network_label = QLabel("Network")
network_label.setObjectName("itemLabel")

network_value = QLabel("↑ 0 MB/s    ↓ 0 MB/s")
network_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

layout.addWidget(title)
layout.addWidget(cpu_label)
layout.addWidget(cpu_bar)
layout.addWidget(memory_label)
layout.addWidget(memory_bar)
layout.addWidget(disk_label)
layout.addWidget(disk_bar)
layout.addWidget(network_label)
layout.addWidget(network_value)
layout.addStretch()

window.setLayout(layout)
window.show()

sys.exit(app.exec())