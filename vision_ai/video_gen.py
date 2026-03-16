import requests
import time
import subprocess
import os
import glob

SERVER = "http://localhost:5003"

# Path to the built app — finds the most recently modified build automatically
def find_app_path() -> str:
    pattern = os.path.expanduser(
        "~/Library/Developer/Xcode/DerivedData/meta_ai_app-*/Build/Products/Debug/meta_ai_app.app"
    )
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError("meta_ai_app.app not found. Build it in Xcode first.")
    # pick the most recently modified
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

    # Wait up to 30s for server to come up
    for i in range(30):
        time.sleep(1)
        if is_server_running():
            print(f"App started and server ready ({i+1}s)")
            return

    raise RuntimeError("App launched but server did not respond on port 5003 after 30s")


def generate_video(prompt: str, timeout: int = 120) -> str:
    """
    Ensure the app is running, send a prompt, poll until video is ready,
    and return the file path.
    """

    ensure_app_running()

    # Send prompt
    resp = requests.post(
        f"{SERVER}/generate",
        json={"prompt": prompt},
        timeout=10
    )
    resp.raise_for_status()
    print("Sent prompt:", resp.json())

    # Poll /status until completed or timeout
    start = time.time()

    while True:

        elapsed = time.time() - start

        if elapsed > timeout:
            raise TimeoutError(f"Video not ready after {timeout}s")

        time.sleep(3)

        data = requests.get(f"{SERVER}/status", timeout=10).json()
        print(f"[{int(elapsed)}s] status:", data)

        if data.get("status") == "completed":
            video_path = data.get("video_path", "")
            print("Video ready:", video_path)
            return video_path


if __name__ == "__main__":

    prompt = "Generate a cinematic video of a robot walking in a futuristic city"

    path = generate_video(prompt)
    print("Done. File saved at:", path)
