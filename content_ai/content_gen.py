"""
content_gen.py
Generates story and video prompts using Ollama (qwen2.5:7b).
Falls back to static data if Ollama is not available.
"""

import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"


def _ollama(prompt: str) -> str:
    """Send a prompt to Ollama and return the response text."""
    resp = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=60
    )
    resp.raise_for_status()
    return resp.json().get("response", "").strip()


def get_story(topic: str) -> str:
    """
    Generate a ~50 word illustrated children's story for the topic using Ollama.
    Falls back to static story if Ollama is unavailable.
    """
    try:
        prompt = (
            f"Write a fun, warm children's story in exactly 50 words about: {topic}. "
            "Use simple language suitable for kids. No title, just the story."
        )
        return _ollama(prompt)
    except Exception as e:
        print(f"[ContentGen] Ollama unavailable, using static story. ({e})")
        return (
            "Benny the fluffy rabbit laughed at slow Tilly the turtle. "
            "They raced through Whispering Woods on a bright sunny morning. "
            "Benny napped beneath a cozy mushroom, dreaming of victory. "
            "Tilly tiptoed past, her shell gleaming softly. "
            "At the finish line, Tilly waited, waving cheerfully as Benny finally arrived, blushing."
        )


def get_video_prompts(topic: str, count: int = 4) -> list[str]:
    """
    Generate video prompts for the topic using Ollama.
    Each prompt uses illustration style with fluffy texture.
    Falls back to static prompts if Ollama is unavailable.
    """
    try:
        prompt = (
            f"Generate exactly {count} video prompts for the topic: '{topic}'. "
            "Each prompt must start with 'Generate a video of' and include: "
            "'illustration style with fluffy texture, storybook art'. "
            "Make them sequential scenes that tell a story. "
            f"Return only a JSON array of {count} strings, nothing else."
        )
        raw = _ollama(prompt)

        # parse JSON array from response
        start = raw.find("[")
        end = raw.rfind("]") + 1
        prompts = json.loads(raw[start:end])

        if isinstance(prompts, list) and len(prompts) >= count:
            return prompts[:count]

        raise ValueError("Invalid response format")

    except Exception as e:
        print(f"[ContentGen] Ollama unavailable, using static prompts. ({e})")
        return [
            "Generate a video of a fluffy cartoon rabbit and a cute turtle standing at a forest race start line, illustration style with fluffy texture, soft pastel colors, warm golden light, storybook art",
            "Generate a video of a fluffy cartoon rabbit sleeping under a giant mushroom in an enchanted forest, illustration style with fluffy texture, dreamy soft lighting, storybook art",
            "Generate a video of a cute cartoon turtle walking steadily along a glowing forest path, illustration style with fluffy texture, magical fireflies, vibrant storybook colors",
            "Generate a video of a cute cartoon turtle crossing a flower-covered finish line while a fluffy rabbit watches in surprise, illustration style with fluffy texture, cheerful storybook art, confetti",
        ][:count]


def get_title(topic: str) -> str:
    """
    Generate a short catchy video title for the topic using Ollama.
    Falls back to static title if Ollama is unavailable.
    """
    try:
        prompt = (
            f"Generate a short, catchy YouTube video title for a children's animated story about: {topic}. "
            "Max 8 words. No quotes, no punctuation at the end. Just the title."
        )
        return _ollama(prompt)
    except Exception as e:
        print(f"[ContentGen] Ollama unavailable, using static title. ({e})")
        return f"The Amazing Adventure of {topic.title()}"


def get_description(topic: str) -> str:
    """
    Generate a YouTube video description for the topic using Ollama.
    Falls back to static description if Ollama is unavailable.
    """
    try:
        prompt = (
            f"Write a short YouTube video description (2-3 sentences) for a children's animated story about: {topic}. "
            "Keep it fun, engaging, and suitable for kids. No hashtags."
        )
        return _ollama(prompt)
    except Exception as e:
        print(f"[ContentGen] Ollama unavailable, using static description. ({e})")
        return (
            f"Join us on a magical animated adventure about {topic}! "
            "A fun and heartwarming story for kids of all ages. "
            "Watch, laugh, and learn a valuable lesson along the way."
        )


if __name__ == "__main__":

    topic = "a rabbit and turtle race through an enchanted forest"

    title = get_title(topic)
    description = get_description(topic)
    story = get_story(topic)
    prompts = get_video_prompts(topic)

    print("=== Title ===")
    print(title)

    print("\n=== Description ===")
    print(description)

    print("\n=== Story ===")
    print(story)

    print("\n=== Video Prompts ===")
    for i, p in enumerate(prompts, 1):
        print(f"{i}. {p}")
