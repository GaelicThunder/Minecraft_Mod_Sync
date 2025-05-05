# Minecraft Mod Sync

A lightweight, cross-platform client-server app to keep your Minecraft mods folder in sync between a Debian-based server and multiple clients (Windows & Linux).  
The server exposes a manifest and mod files via HTTP, while clients download new or updated mods and remove obsolete ones automatically.

---

## Features

- **Automatic mod synchronization**: Download new/updated mods, delete obsolete mods.
- **Super lightweight server**: Suitable for low-power boards (Radxa, Raspberry Pi, etc.).
- **Easy to use**: GUI for Windows, CLI for Linux.
- **No SSH required**: Uses a simple HTTP API.

---

## Project Structure

```
mc_mod_sync/
├── server/
│   ├── server_mod_updater.py
│   ├── mods/                # Place your server .jar mods here
│   └── requirements.txt
├── client_windows/
│   ├── gui.py
│   └── (optional: icon.ico, build.bat)
└── client_linux/
    ├── cli.py
    └── setup.py
```

---

## Server Setup (Debian/Linux)

1. **Install dependencies**
   ```bash
   cd server
   pip install -r requirements.txt
   ```
2. **Place your mod .jar files in the `mods/` directory**
3. **Run the server**
   ```bash
   python server_mod_updater.py
   ```
   The server will listen on port 8080 by default.

4. **(Optional) Run as a service**
   - See the [systemd section below](#run-server-as-a-systemd-service).

---

## Windows Client

1. **Install Python and dependencies**
   - Download and install [Python 3.x](https://www.python.org/downloads/)
   - Install dependencies:
     ```bash
     pip install PySimpleGUI requests
     ```
2. **Run the client**
   - Double click `gui.py` or run:
     ```bash
     python gui.py
     ```
   - Enter your server URL (e.g. `http://google.com:8080`)
   - Click "Sync" to synchronize your mods folder.

3. **Build a standalone exe (optional)**
   - Install PyInstaller:
     ```bash
     pip install pyinstaller
     ```
   - Build:
     ```bash
     pyinstaller --onefile --noconsole gui.py
     ```
   - The executable will be in the `dist/` folder.

---

## Linux Client (Arch, Debian, etc.)

1. **Install Python and dependencies**
   ```bash
   pip install requests
   ```
2. **Run the client**
   ```bash
   python cli.py --server http://google.com:8080
   ```
   - Your local `mods/` folder will be synchronized with the server.

3. **(Optional) Install as a command**
   ```bash
   cd client_linux
   pip install --user .
   mcmodsync --server http://google.com:8080
   ```

---

## How It Works

- The server exposes:
  - `/manifest` - a JSON listing of all mods and their SHA-256 hashes
  - `/mods/` - direct download of mod files
- The client:
  - Compares local mods with the manifest
  - Downloads new/updated mods
  - Deletes local mods not present on the server

---

## Run Server as a systemd Service

1. Create a service file:
   ```ini
   [Unit]
   Description=Minecraft Mod Sync Server
   After=network.target

   [Service]
   User=youruser
   WorkingDirectory=/path/to/server
   ExecStart=/usr/bin/python3 /path/to/server/server_mod_updater.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
2. Reload systemd and enable:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable mcmodsync.service
   sudo systemctl start mcmodsync.service
   ```

---

## Notes

- The server expects the `mods/` folder to be in the same directory as `server_mod_updater.py`.
- The Windows and Linux clients will create or update their own `mods/` folder in the current directory.
- Make sure your firewall allows incoming connections on the chosen port (default: 8080).

---

## License

MIT
