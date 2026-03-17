"""
prompt_builder.py
Stores all prompt templates and duration/segment utilities.
"""

import re

# ── Duration / segment config ────────────────────────────────────────────────

CLIP_DURATION_SEC = 5   # each meta.ai clip is ~5 seconds
MIN_DURATION_SEC  = 20
MAX_DURATION_SEC  = 300  # 5 min


def parse_duration(user_request: str) -> int:
    """
    Parse user request → duration in seconds, clamped 20s–300s.
      "2 min video"  → 120s
      "30 sec video" → 30s
      "100 words"    → 50s  (0.5s per word)
      default        → 60s
    """
    text = user_request.lower()
    duration = 60

    m = re.search(r'(\d+)\s*min', text)
    if m:
        duration = int(m.group(1)) * 60
    else:
        m = re.search(r'(\d+)\s*sec', text)
        if m:
            duration = int(m.group(1))
        else:
            m = re.search(r'(\d+)\s*words?', text)
            if m:
                duration = int(int(m.group(1)) * 0.5)

    return max(MIN_DURATION_SEC, min(duration, MAX_DURATION_SEC))


def segment_count(duration_sec: int) -> int:
    """Number of 5-second clips needed."""
    return max(1, round(duration_sec / CLIP_DURATION_SEC))


# ── Prompt templates ─────────────────────────────────────────────────────────

def title_prompt(topic: str) -> str:
    return f"""\
Create a catchy YouTube title for a children's animated story.
Topic: {topic}
Rules:
- max 8 words
- no quotes
- engaging and fun
- output ONLY the title, nothing else"""


def description_prompt(topic: str) -> str:
    return f"""\
Write a YouTube description for a children's animated story.
Topic: {topic}
Rules:
- 3 sentences
- friendly, warm tone
- mention the main characters and adventure
- end with a call to action (like/subscribe)
- no hashtags
- output ONLY the description, nothing else"""


def story_prompt(topic: str) -> str:
    return f"""\
Write a warm, vivid children's story in EXACTLY 50 words about: {topic}
Rules:
- simple, expressive language
- introduce characters and a small journey or challenge
- end with a happy resolution
- no title, no headings
- output ONLY the story text"""


def video_prompts_prompt(topic: str, count: int) -> str:
    return f"""\
Create EXACTLY {count} cinematic AI video generation prompts for a children's animated story.
Topic: {topic}

Rules for each prompt:
- Start with: "Generate a video of"
- Include the main subject with rich visual detail (colors, textures, expressions)
- Describe the environment: lighting, atmosphere, background elements
- Specify camera style: aerial shot / close-up / wide shot / tracking shot / low-angle pan
- Include art style: soft illustration style, fluffy storybook textures, warm pastel palette
- Each prompt must be a unique sequential scene that advances the story
- Prompts must flow as a narrative from beginning → middle → end
- Be highly descriptive (40-60 words per prompt)
- Output ONLY a valid JSON array of strings, no extra text, no markdown

Example format:
["Generate a video of ...", "Generate a video of ...", ...]"""
