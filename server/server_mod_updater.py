from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import hashlib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODS_DIR = os.path.abspath(os.path.join(BASE_DIR, "mods"))

app = FastAPI()
app.mount("/mods", StaticFiles(directory=MODS_DIR), name="mods")

def generate_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            sha.update(chunk)
    return sha.hexdigest()

@app.get("/manifest")
def get_manifest():
    mods = {}
    try:
        for entry in os.scandir(MODS_DIR):
            if entry.is_file() and entry.name.endswith(".jar"):
                mods[entry.name] = generate_sha256(entry.path)
    except FileNotFoundError:
        print(f"Error: '{MODS_DIR}' doesn't exists!")
    return mods

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
