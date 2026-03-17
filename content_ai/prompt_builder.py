"""
prompt_builder.py
Parses user request to determine video duration/length,
calculates number of 5-second video segments needed,
and builds detailed cinematic prompts matched to story content.
"""

import re


# Each meta.ai video clip is ~5 seconds
CLIP_DURATION_SEC = 5


MIN_DURATION_SEC = 20
MAX_DURATION_SEC = 300  # 5 min


def parse_duration(user_request: str) -> int:
    """
    Parse user request and return target video duration in seconds.
    Clamped between 20s and 5 min (300s).

    Supports:
      - "2 min video"  → 120s
      - "30 sec video" → 30s
      - "100 words"    → ~100 words * 0.5s/word = 50s
      - default        → 60s (1 min)
    """
    text = user_request.lower()
    duration = 60  # default

    # Match "X min" or "X minute"
    m = re.search(r'(\d+)\s*min', text)
    if m:
        duration = int(m.group(1)) * 60

    # Match "X sec" or "X second"
    elif re.search(r'(\d+)\s*sec', text):
        m = re.search(r'(\d+)\s*sec', text)
        duration = int(m.group(1))

    # Match "X words" — estimate ~0.5s per word narration pace
    elif re.search(r'(\d+)\s*words?', text):
        m = re.search(r'(\d+)\s*words?', text)
        duration = int(int(m.group(1)) * 0.5)

    return max(MIN_DURATION_SEC, min(duration, MAX_DURATION_SEC))


def segment_count(duration_sec: int) -> int:
    """How many 5-second clips needed to fill the duration."""
    return max(1, round(duration_sec / CLIP_DURATION_SEC))


# Cinematic style modifiers cycled across segments for variety
_STYLES = [
    "cinematic aerial shot, golden hour lighting, ultra realistic, 8K",
    "close-up slow motion, dramatic fog and depth of field, cinematic",
    "wide establishing shot, vibrant colors, lush environment, epic scale",
    "dramatic low-angle camera pan, moody lighting, photorealistic",
    "tracking shot following subject, dynamic movement, cinematic grade",
    "bird's eye view, sweeping landscape, atmospheric haze, ultra detailed",
    "medium shot, warm natural light, shallow depth of field, film grain",
    "time-lapse style, sweeping motion, vivid sky, hyper realistic",
]


def build_video_prompts(topic: str, story: str, duration_sec: int) -> list[str]:
    """
    Split the story into segments and build one detailed video prompt per segment.
    Each prompt is matched to that part of the story + a cinematic style.
    """
    count = segment_count(duration_sec)

    # Split story into roughly equal sentence chunks per segment
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', story) if s.strip()]

    prompts = []
    for i in range(count):
        # Pick the story sentence closest to this segment's position
        if sentences:
            idx = min(int(i * len(sentences) / count), len(sentences) - 1)
            scene_context = sentences[idx]
        else:
            scene_context = topic

        style = _STYLES[i % len(_STYLES)]

        prompt = (
            f"Generate a video of {topic}. "
            f"Scene: {scene_context} "
            f"Style: {style}."
        )
        prompts.append(prompt)

    return prompts


if __name__ == "__main__":
    topic = "a turtle exploring a magical pond"
    story = (
        "Deep within the heart of a magical pond, an extraordinary journey begins. "
        "Ancient forces stir as a lone turtle ventures forward. "
        "Every step reveals hidden wonders and breathtaking beauty. "
        "The world holds its breath as destiny unfolds."
    )
    duration = parse_duration("2 min video")
    prompts = build_video_prompts(topic, story, duration)
    print(f"Duration: {duration}s → {segment_count(duration)} segments")
    for i, p in enumerate(prompts, 1):
        print(f"\n{i}. {p}")
