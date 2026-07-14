from pathlib import Path

import psutil


class SystemInfo:
    """PCのシステム情報を取得するクラス。"""

    @staticmethod
    def get_cpu_usage() -> float:
        return psutil.cpu_percent(interval=None)

    @staticmethod
    def get_memory_usage() -> float:
        return psutil.virtual_memory().percent

    @staticmethod
    def get_disk_usage() -> float:
        drive = Path.home().anchor
        return psutil.disk_usage(drive).percent