"""
content_gen.py
All content generation functions using Ollama (qwen2.5:7b).
Falls back to static data if Ollama is unavailable.
"""

import requests
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from content_ai.prompt_builder import (
    parse_duration,
    segment_count,
    title_prompt,
    description_prompt,
    story_prompt,
    video_prompts_prompt,
)

OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"


# ── Ollama core ──────────────────────────────────────────────────────────────

def _ollama(prompt: str, num_predict: int = 300) -> str:
    """Send a prompt to Ollama and return the text response."""
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.8, "num_predict": num_predict},
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json().get("response", "").strip()


# ── Fallbacks ────────────────────────────────────────────────────────────────

_FALLBACK_TITLE = "The Magical Adventure Begins"

_FALLBACK_DESCRIPTION = (
    "Join our lovable characters on a breathtaking journey full of wonder and surprises! "
    "Watch as they discover the true meaning of friendship and courage in a magical world. "
    "Don't forget to like and subscribe for more enchanting stories!"
)

_FALLBACK_STORY = (
    "Benny the fluffy rabbit laughed at slow Tilly the turtle. "
    "They raced through Whispering Woods on a bright sunny morning. "
    "Benny napped beneath a cozy mushroom, dreaming of victory. "
    "Tilly tiptoed past, her shell gleaming softly. "
    "At the finish line, Tilly waited, waving cheerfully as Benny finally arrived, blushing."
)

_FALLBACK_PROMPTS = [
    "Generate a video of a fluffy cartoon rabbit and a cute turtle standing at a sunlit forest race start line, soft pastel colors, warm golden hour light, wide establishing shot, illustration style with fluffy storybook textures, lush green trees in background, cheerful expressions, 8K detail",
    "Generate a video of a fluffy cartoon rabbit dashing through an enchanted forest path lined with glowing flowers, motion blur on legs, dynamic tracking shot, vibrant storybook colors, magical sparkles in the air, illustration style with fluffy textures, cinematic depth of field",
    "Generate a video of a fluffy cartoon rabbit sleeping peacefully under a giant spotted mushroom, dreamy soft lighting, close-up shot, golden dappled sunlight through leaves, illustration style with fluffy storybook textures, tiny butterflies resting nearby, warm pastel palette",
    "Generate a video of a cute cartoon turtle walking steadily along a glowing forest path, determined expression, low-angle tracking shot, magical fireflies lighting the way, illustration style with fluffy textures, deep enchanted forest background, vibrant storybook colors, cinematic atmosphere",
    "Generate a video of a cute cartoon turtle crossing a flower-covered finish line, triumphant pose, wide celebratory shot, confetti raining down, a surprised fluffy rabbit in background, illustration style with fluffy storybook textures, warm cheerful lighting, vibrant pastel colors",
]


# ── Public functions ─────────────────────────────────────────────────────────

def get_title(topic: str) -> str:
    """Generate a short YouTube title."""
    try:
        return _ollama(title_prompt(topic), num_predict=50)
    except Exception as e:
        print(f"[ContentGen] Ollama unavailable for title ({e}), using fallback.")
        return _FALLBACK_TITLE


def get_description(topic: str) -> str:
    """Generate a YouTube description."""
    try:
        return _ollama(description_prompt(topic), num_predict=150)
    except Exception as e:
        print(f"[ContentGen] Ollama unavailable for description ({e}), using fallback.")
        return _FALLBACK_DESCRIPTION


def get_story(topic: str) -> str:
    """Generate a ~50 word children's story."""
    try:
        return _ollama(story_prompt(topic), num_predict=200)
    except Exception as e:
        print(f"[ContentGen] Ollama unavailable for story ({e}), using fallback.")
        return _FALLBACK_STORY


def get_video_prompts(topic: str, user_request: str = "1 min video") -> list[str]:
    """
    Parse user_request for duration, calculate segment count,
    generate that many detailed cinematic prompts via Ollama.
    """
    duration_sec = parse_duration(user_request)
    count = segment_count(duration_sec)
    print(f"[ContentGen] Duration: {duration_sec}s → {count} video segments")

    try:
        raw = _ollama(video_prompts_prompt(topic, count), num_predict=count * 120)
        start = raw.find("[")
        end   = raw.rfind("]") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON array found in response")
        prompts = json.loads(raw[start:end])
        if isinstance(prompts, list) and len(prompts) > 0:
            # pad with cycled prompts if Ollama returned fewer than needed
            while len(prompts) < count:
                prompts.append(prompts[len(prompts) % len(prompts)])
            return prompts[:count]
        raise ValueError("Empty or invalid JSON array")
    except Exception as e:
        print(f"[ContentGen] Ollama unavailable for video prompts ({e}), using fallback.")
        return [_FALLBACK_PROMPTS[i % len(_FALLBACK_PROMPTS)] for i in range(count)]


# ── CLI test ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    topic       = "a rabbit and turtle race through an enchanted forest"
    user_request = "1 min video"

    print("\n=== TITLE ===")
    print(get_title(topic))

    print("\n=== DESCRIPTION ===")
    print(get_description(topic))

    print("\n=== STORY ===")
    print(get_story(topic))

    prompts = get_video_prompts(topic, user_request)
    print(f"\n=== VIDEO PROMPTS ({len(prompts)}) ===")
    for i, p in enumerate(prompts, 1):
        print(f"\n{i}. {p}")
