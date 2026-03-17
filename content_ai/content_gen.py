"""
content_gen.py
Generates story and video prompts using Ollama (dummy data for now).
"""


def get_story(topic: str) -> str:
    """
    Generate a short story for the given topic.
    TODO: replace with ollama call
    """
    return (f"In a world transformed by technology, a lone explorer named Aria "
        f"embarks on a journey through {topic}. ")


def get_video_prompts(topic: str, count: int = 3) -> list[str]:
    """
    Generate a list of video prompts for the given topic.
    Prefixed with 'Generate a video of' to trigger meta.ai video mode.
    TODO: replace with ollama call
    """
    return [
        f"Generate a video of {topic}, cinematic aerial shot, golden hour, ultra realistic",
        f"Generate a video of {topic}, close-up slow motion, dramatic lighting and fog"
    ]


if __name__ == "__main__":

    topic = "a robot walking in a futuristic city"

    story = get_story(topic)
    prompts = get_video_prompts(topic)

    print("=== Story ===")
    print(story)

    print("\n=== Video Prompts ===")
    for i, p in enumerate(prompts, 1):
        print(f"{i}. {p}")
