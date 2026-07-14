from pathlib import Path
from time import monotonic

import psutil


class SystemInfo:
    """PCのシステム情報を取得するクラス。"""

    BYTES_PER_MEGABYTE = 1024 * 1024

    def __init__(self) -> None:
        network = psutil.net_io_counters()

        self._previous_bytes_sent = network.bytes_sent
        self._previous_bytes_received = network.bytes_recv
        self._previous_network_time = monotonic()

    @staticmethod
    def get_cpu_usage() -> float:
        """CPU使用率を取得する。"""
        return psutil.cpu_percent(interval=None)

    @staticmethod
    def get_memory_usage() -> float:
        """メモリ使用率を取得する。"""
        return psutil.virtual_memory().percent

    @staticmethod
    def get_disk_usage() -> float:
        """Windowsが入っているドライブの使用率を取得する。"""
        drive = Path.home().anchor
        return psutil.disk_usage(drive).percent

    def get_network_speed(self) -> tuple[float, float]:
        """
        前回取得時からのネットワーク速度をMB/sで取得する。

        Returns:
            tuple[float, float]:
                アップロード速度とダウンロード速度。
        """
        network = psutil.net_io_counters()
        current_time = monotonic()

        elapsed_seconds = current_time - self._previous_network_time

        if elapsed_seconds <= 0:
            return 0.0, 0.0

        sent_difference = network.bytes_sent - self._previous_bytes_sent
        received_difference = (
            network.bytes_recv - self._previous_bytes_received
        )

        upload_speed = (
            sent_difference
            / self.BYTES_PER_MEGABYTE
            / elapsed_seconds
        )
        download_speed = (
            received_difference
            / self.BYTES_PER_MEGABYTE
            / elapsed_seconds
        )

        self._previous_bytes_sent = network.bytes_sent
        self._previous_bytes_received = network.bytes_recv
        self._previous_network_time = current_time

        return max(upload_speed, 0.0), max(download_speed, 0.0)