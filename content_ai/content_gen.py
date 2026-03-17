"""
content_gen.py
Generates story and video prompts.
Video count and prompt detail driven by prompt_builder based on user request.
TODO: replace get_story with ollama call
"""

from content_ai.prompt_builder import parse_duration, build_video_prompts, segment_count


def get_story(topic: str) -> str:
    """
    Generate a story for the given topic.
    TODO: replace with ollama call
    """
    return (
        f"Deep within the heart of {topic}, an extraordinary journey begins. "
        f"Ancient forces stir as a lone traveler ventures forward, guided only by curiosity and courage. "
        f"Every step reveals hidden wonders, forgotten secrets, and breathtaking beauty. "
        f"Shadows dance across the landscape as the traveler pushes deeper into the unknown. "
        f"Strange creatures watch from the edges, curious but cautious. "
        f"The world holds its breath, watching as destiny unfolds in the most unexpected, magical way."
    )


def get_video_prompts(topic: str, user_request: str = "1 min video") -> list[str]:
    """
    Parse user_request to determine duration, generate story,
    then build one detailed cinematic prompt per 5-second segment.
    """
    duration_sec = parse_duration(user_request)
    story = get_story(topic)
    prompts = build_video_prompts(topic, story, duration_sec)
    print(f"[ContentGen] Duration: {duration_sec}s → {len(prompts)} video segments")
    return prompts


if __name__ == "__main__":
    topic = "a turtle exploring a magical pond"
    user_request = "2 min video"

    story = get_story(topic)
    prompts = get_video_prompts(topic, user_request)

    print("=== Story ===")
    print(story)

    print(f"\n=== Video Prompts ({len(prompts)}) ===")
    for i, p in enumerate(prompts, 1):
        print(f"\n{i}. {p}")
