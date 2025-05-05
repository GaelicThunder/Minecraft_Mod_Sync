@echo off
pip install pyinstaller requests
pyinstaller --onefile --noconsole --add-data "icon.ico;." --icon=icon.ico gui.py
