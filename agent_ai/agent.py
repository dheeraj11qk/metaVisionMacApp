"""
agent.py
Orchestrates content_gen → voice_gen pipeline.
Generates a story then produces voice audio, with live terminal progress.
"""

import sys
import os

# allow imports from sibling folders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from content_ai.content_gen import get_story
from audio_ai.voice_gen import VoiceGen


def run(topic: str, output_path: str = "output_voice.wav"):

    print("=" * 50)
    print(f"[Agent] Topic: {topic}")
    print("=" * 50)

    # Step 1: generate story
    print("\n[Agent] Generating story...")
    story = get_story(topic)
    print("[Agent] Story:\n")
    print(story)

    # Step 2: generate voice
    print("\n[Agent] Starting voice generation...")
    vg = VoiceGen(speaker_wav="audio_ai/voice_sample.wav")
    path = vg.generate(story, output_path=output_path)

    print("\n" + "=" * 50)
    print(f"[Agent] Done. Audio saved at: {path}")
    print("=" * 50)

    return path


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "It was midnight. A strange sound came from the forest. Someone was watching him."
    run(topic)
