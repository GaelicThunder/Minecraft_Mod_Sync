import requests
import hashlib
import os
import argparse

def sync_mods(server_url):
    try:
        print("Connecting...")
        response = requests.get(f"{server_url}/manifest")
        response.raise_for_status()
        print("Connection established")
        manifest = response.json()

        os.makedirs("mods", exist_ok=True)

        local_mods = {}
        for file in os.listdir("mods"):
            if file.endswith(".jar"):
                with open(os.path.join("mods", file), 'rb') as f:
                    local_mods[file] = hashlib.sha256(f.read()).hexdigest()

        for local_file in list(local_mods.keys()):
            if local_file not in manifest:
                os.remove(os.path.join("mods", local_file))
                del local_mods[local_file]

        for mod, server_hash in manifest.items():
            mod_path = os.path.join("mods", mod)
            if mod not in local_mods or local_mods[mod] != server_hash:
                print(f"Downloading {mod}...")
                mod_data = requests.get(f"{server_url}/mods/{mod}").content
                with open(mod_path, 'wb') as f:
                    f.write(mod_data)

        print("Sync complete!")
    except Exception as e:
        print(f"Error: {str(e)}")


def hash_file(filepath):
    sha = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            sha.update(chunk)
    return sha.hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Minecraft Mod Sync')
    parser.add_argument('--server', required=True, help='server URL')
    args = parser.parse_args()
    sync_mods(args)
