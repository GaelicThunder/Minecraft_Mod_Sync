import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QProgressBar, QLabel, QFileDialog
)
from PySide6.QtCore import Qt, QThread, Signal
import requests
import hashlib
import os

class SyncThread(QThread):
    progress = Signal(int)
    status = Signal(str)
    done = Signal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            self.status.emit("Downloading manifest...")
            manifest = requests.get(f"{self.url}/manifest").json()
            local_mods = {}
            if os.path.exists("mods"):
                for file in os.listdir("mods"):
                    if file.endswith(".jar"):
                        with open(os.path.join("mods", file), 'rb') as f:
                            local_mods[file] = hashlib.sha256(f.read()).hexdigest()
            # Delete local mods not on server
            for local_file in list(local_mods.keys()):
                if local_file not in manifest:
                    self.status.emit(f"Deleting {local_file}...")
                    os.remove(os.path.join("mods", local_file))
                    del local_mods[local_file]
            # Download new/updated mods
            total = len(manifest)
            count = 0
            for mod, server_hash in manifest.items():
                if mod not in local_mods or local_mods[mod] != server_hash:
                    self.status.emit(f"Downloading {mod}...")
                    response = requests.get(f"{self.url}/mods/{mod}")
                    os.makedirs("mods", exist_ok=True)
                    with open(os.path.join("mods", mod), 'wb') as f:
                        f.write(response.content)
                count += 1
                self.progress.emit(int(count / total * 100) if total else 100)
            self.status.emit("Sync complete!")
            self.done.emit("Sync complete!")
        except Exception as e:
            self.status.emit(f"Error: {str(e)}")
            self.done.emit(f"Error: {str(e)}")

class ModSyncApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minecraft Mod Sync")
        self.setFixedSize(400, 200)
        layout = QVBoxLayout(self)
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("http://localhost:8080")
        layout.addWidget(self.url_input)
        self.status_label = QLabel("Ready.", self)
        layout.addWidget(self.status_label)
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        self.sync_btn = QPushButton("Sync Mods", self)
        layout.addWidget(self.sync_btn)
        self.sync_btn.clicked.connect(self.start_sync)
        self.setLayout(layout)

    def start_sync(self):
        url = self.url_input.text()
        if not url:
            self.status_label.setText("Please enter the server URL.")
            return
        self.sync_btn.setEnabled(False)
        self.thread = SyncThread(url)
        self.thread.progress.connect(self.progress.setValue)
        self.thread.status.connect(self.status_label.setText)
        self.thread.done.connect(self.on_done)
        self.thread.start()

    def on_done(self, message):
        self.sync_btn.setEnabled(True)
        self.status_label.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModSyncApp()
    window.show()
    sys.exit(app.exec())

