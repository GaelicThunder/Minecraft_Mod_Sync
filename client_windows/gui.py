import PySimpleGUI as sg
import requests
import hashlib
import os

def sync_process(url, window):
    try:
        window["-STATUS-"].update("Downloading manifest from server...")
        manifest = requests.get(f"{url}/manifest").json()
        
        local_mods = {}
        if os.path.exists("mods"):
            for file in os.listdir("mods"):
                if file.endswith(".jar"):
                    with open(os.path.join("mods", file), 'rb') as f:
                        local_mods[file] = hashlib.sha256(f.read()).hexdigest()

        for local_file in list(local_mods.keys()):
            if local_file not in manifest:
                window["-STATUS-"].update(f"Deleting {local_file}...")
                os.remove(os.path.join("mods", local_file))
                del local_mods[local_file]

        total = len(manifest)
        count = 0
        for mod, server_hash in manifest.items():
            if mod not in local_mods or local_mods[mod] != server_hash:
                window["-STATUS-"].update(f"Downloading {mod}...")
                response = requests.get(f"{url}/mods/{mod}")
                os.makedirs("mods", exist_ok=True)
                with open(os.path.join("mods", mod), 'wb') as f:
                    f.write(response.content)
            count += 1
            window["-PROG-"].update_bar(int(count / total * 100))

        window["-STATUS-"].update("Sync Completed!")
    except Exception as e:
        window["-STATUS-"].update(f"Error: {str(e)}")

layout = [
    [sg.Text("Server URL:"), sg.Input(key="-URL-", default_text="http://example_URL:8080")],
    [sg.Button("Sync"), sg.Exit()],
    [sg.ProgressBar(100, size=(20,20), key="-PROG-")],
    [sg.Text("", key="-STATUS-", size=(40,1))]
]

window = sg.Window("Minecraft Mod Sync", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == "Sync":
        sync_process(values["-URL-"], window)

window.close()
