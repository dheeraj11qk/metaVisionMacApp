"""
content_gen.py
Generates story and video prompts using Ollama (dummy data for now).
"""


def get_story(topic: str) -> str:
    """
    ~50 word illustrated children's story about a rabbit and turtle.
    TODO: replace with ollama call
    """
    return (
        "Benny the fluffy rabbit laughed at slow Tilly the turtle. "
        "They raced through Whispering Woods on a bright sunny morning. "
        "Benny napped beneath a cozy mushroom, dreaming of victory. "
        "Tilly tiptoed past, her shell gleaming softly. "
        "At the finish line, Tilly waited, waving cheerfully as Benny finally arrived, blushing."
    )


def get_video_prompts(topic: str, count: int = 4) -> list[str]:
    """
    4 video prompts in illustration style with fluffy texture.
    Prefixed with 'Generate a video of' to trigger meta.ai video mode.
    TODO: replace with ollama call
    """
    prompts = [
        "Generate a video of a fluffy cartoon rabbit and a cute turtle standing at a forest race start line, illustration style with fluffy texture, soft pastel colors, warm golden light, storybook art",
        "Generate a video of a fluffy cartoon rabbit sleeping under a giant mushroom in an enchanted forest, illustration style with fluffy texture, dreamy soft lighting, storybook art",
        "Generate a video of a cute cartoon turtle walking steadily along a glowing forest path, illustration style with fluffy texture, magical fireflies, vibrant storybook colors",
        "Generate a video of a cute cartoon turtle crossing a flower-covered finish line while a fluffy rabbit watches in surprise, illustration style with fluffy texture, cheerful storybook art, confetti",
    ]
    return prompts[:count]


if __name__ == "__main__":

    topic = "a robot walking in a futuristic city"

    story = get_story(topic)
    prompts = get_video_prompts(topic)

    print("=== Story ===")
    print(story)

    print("\n=== Video Prompts ===")
    for i, p in enumerate(prompts, 1):
        print(f"{i}. {p}")
