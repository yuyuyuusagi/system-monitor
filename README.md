# System Monitor

Windows向けのデスクトップシステム監視アプリです。

## 現在の機能

- CPU表示UI
- メモリ表示UI
- ディスク表示UI
- ネットワーク表示UI
- ダークテーマ

## 開発環境

- Python
- PySide6
- psutil

## 起動方法

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py