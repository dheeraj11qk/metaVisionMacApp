# metaVisionMacApp

AI-powered video generation pipeline. Generates a story, voice narration, and video segments via meta.ai, then combines them into a final MP4.

## Requirements

- macOS
- Python 3.10+
- Xcode (to build the Swift app)
- `xcpretty` (optional, for cleaner build logs): `gem install xcpretty`

## Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install requests moviepy pydub TTS torch
```

## Usage

### Generate a video

```bash
make video TOPIC="a turtle exploring a magical pond, 1 min video"
```

This will:
1. Build the macOS Swift app
2. Launch it in the background (HTTP server on port 5003)
3. Generate story + voice narration
4. Generate video segments via meta.ai
5. Combine everything into `output/final_output.mp4`

### Video duration options

| Command | Duration | Segments |
|---|---|---|
| `make video TOPIC="..., 20 sec video"` | 20s | 4 clips |
| `make video TOPIC="..., 1 min video"` | 60s | 12 clips |
| `make video TOPIC="..., 2 min video"` | 120s | 24 clips |
| `make video TOPIC="..., 5 min video"` | 300s | 60 clips |
| `make video TOPIC="..., 100 words"` | ~50s | ~10 clips |

Duration is clamped between **20 seconds** and **5 minutes**.

### Run just the Python agent (app already running)

```bash
.venv/bin/python agent_ai/agent.py "a turtle exploring a magical pond, 2 min video"
```

### Build app only

```bash
make build-app
```

### Launch app only

```bash
make open-app
```

## Output

- Final video: `output/final_output.mp4`
- Temp voice: `temp/content_voice.wav`
- Video segments are auto-deleted after combining

## Project Structure

```
agent_ai/        # Orchestration pipeline
audio_ai/        # Voice generation (XTTS v2)
content_ai/      # Story + prompt generation
vision_ai/       # meta.ai video generation client
video_edit/      # Video combining and audio merging
meta_ai_app/     # macOS SwiftUI browser app (HTTP server)
output/          # Final output videos
temp/            # Temporary files (voice, video segments)
```
