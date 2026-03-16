"""
content_gen.py
Generates story and video prompts using Ollama (dummy data for now).
"""


def get_story(topic: str) -> str:
    """
    Generate a short story for the given topic.
    TODO: replace with ollama call
    """
    return (
        f"In a world transformed by technology, a lone explorer named Aria "
        f"embarks on a journey through {topic}. "
        f"With every step, she uncovers ancient secrets hidden beneath the surface, "
        f"leading her to a discovery that will change humanity forever."
    )


def get_video_prompts(topic: str, count: int = 3) -> list[str]:
    """
    Generate a list of video prompts for the given topic.
    TODO: replace with ollama call
    """
    return [
        f"Cinematic aerial shot of {topic} at golden hour, ultra realistic, 4K",
        f"Close-up slow motion of {topic} with dramatic lighting and fog",
        f"Futuristic timelapse of {topic} transitioning from day to night",
    ][:count]


if __name__ == "__main__":

    topic = "a robot walking in a futuristic city"

    story = get_story(topic)
    prompts = get_video_prompts(topic)

    print("=== Story ===")
    print(story)

    print("\n=== Video Prompts ===")
    for i, p in enumerate(prompts, 1):
        print(f"{i}. {p}")
