import requests
import time
import subprocess
import os
import glob
import base64

SERVER = "http://localhost:5003"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEGMENTS_DIR = os.path.join(ROOT, "temp", "video_segments")


def find_app_path() -> str:
    pattern = os.path.expanduser(
        "~/Library/Developer/Xcode/DerivedData/meta_ai_app-*/Build/Products/Debug/meta_ai_app.app"
    )
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError("meta_ai_app.app not found. Build it in Xcode first.")
    return max(matches, key=os.path.getmtime)


def is_server_running() -> bool:
    try:
        r = requests.get(f"{SERVER}/status", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def ensure_app_running():
    if is_server_running():
        print("App already running.")
        return

    app_path = find_app_path()
    print(f"Starting app: {app_path}")
    subprocess.Popen(["open", app_path])

    for i in range(30):
        time.sleep(1)
        if is_server_running():
            print(f"App started and server ready ({i+1}s)")
            return

    raise RuntimeError("App launched but server did not respond on port 5003 after 30s")


def generate_video(prompt: str, timeout: int = 120) -> str:
    """
    Send prompt to Swift app, poll until video is ready,
    retrieve base64 data, save to temp/video_segments/, return path.
    """
    ensure_app_running()
    os.makedirs(SEGMENTS_DIR, exist_ok=True)

    resp = requests.post(f"{SERVER}/generate", json={"prompt": prompt}, timeout=10)
    resp.raise_for_status()
    print("Sent prompt:", resp.json())

    start = time.time()

    while True:
        elapsed = time.time() - start

        if elapsed > timeout:
            raise TimeoutError(f"Video not ready after {timeout}s")

        time.sleep(3)

        data = requests.get(f"{SERVER}/status", timeout=10).json()
        print(f"[{int(elapsed)}s] status:", data.get("status"))

        if data.get("status") == "completed":
            filename = data.get("filename", f"video_{int(time.time())}.mp4")
            b64 = data.get("data", "")

            # Decode and save to temp/video_segments/
            video_bytes = base64.b64decode(b64)
            out_path = os.path.join(SEGMENTS_DIR, filename)

            with open(out_path, "wb") as f:
                f.write(video_bytes)

            print("Video saved to:", out_path)

            # Clean up the file inside the app sandbox
            try:
                requests.post(f"{SERVER}/delete", timeout=5)
                print("Sandbox file deleted.")
            except Exception as e:
                print("Delete request failed (non-critical):", e)

            return out_path


if __name__ == "__main__":
    prompt = "Generate a cinematic video of a robot walking in a futuristic city"
    path = generate_video(prompt)
    print("Done. File saved at:", path)
