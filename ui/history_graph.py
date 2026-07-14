from collections import deque

import pyqtgraph as pg
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class HistoryGraphCard(QFrame):
    """CPUとメモリの使用率履歴を表示するカード。"""

    HISTORY_LENGTH = 60

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("card")

        self.cpu_history = deque(
            [0] * self.HISTORY_LENGTH,
            maxlen=self.HISTORY_LENGTH,
        )
        self.memory_history = deque(
            [0] * self.HISTORY_LENGTH,
            maxlen=self.HISTORY_LENGTH,
        )

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        title = QLabel("Performance history")
        title.setObjectName("cardTitle")

        description = QLabel("CPU and memory usage over the last 60 seconds")
        description.setObjectName("cardDescription")

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground(None)
        self.plot_widget.setMinimumHeight(180)

        self.plot_widget.setYRange(0, 100)
        self.plot_widget.setXRange(
            -(self.HISTORY_LENGTH - 1),
            0,
            padding=0,
        )

        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.hideAxis("bottom")
        self.plot_widget.showGrid(x=False, y=True, alpha=0.15)

        left_axis = self.plot_widget.getAxis("left")
        left_axis.setLabel("%")
        left_axis.setTextPen("#8f98a8")
        left_axis.setPen("#2a303d")

        self.plot_widget.addLegend(offset=(10, 10))

        self.cpu_curve = self.plot_widget.plot(
            pen=pg.mkPen("#4c8bf5", width=2),
            name="CPU",
        )

        self.memory_curve = self.plot_widget.plot(
            pen=pg.mkPen("#9b7cff", width=2),
            name="Memory",
        )

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.plot_widget)

    def update_values(
        self,
        cpu_usage: int,
        memory_usage: int,
    ) -> None:
        """新しい使用率を履歴へ追加してグラフを更新する。"""

        self.cpu_history.append(cpu_usage)
        self.memory_history.append(memory_usage)

        x_values = list(
            range(
                -(len(self.cpu_history) - 1),
                1,
            )
        )

        self.cpu_curve.setData(
            x_values,
            list(self.cpu_history),
        )
        self.memory_curve.setData(
            x_values,
            list(self.memory_history),
        )