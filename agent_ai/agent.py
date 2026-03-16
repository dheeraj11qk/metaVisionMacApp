"""
agent.py
Orchestrates: content_gen → voice_gen → video_gen → video_edit → output
"""

import sys
import os
import shutil

# allow imports from sibling folders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from content_ai.content_gen import get_story, get_video_prompts
from audio_ai.voice_gen import VoiceGen
# from vision_ai.video_gen import generate_video
from video_edit.video_edit import VideoEditor


def run(topic: str):

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(root, "output")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 50)
    print(f"[Agent] Topic: {topic}")
    print("=" * 50)

    # Step 1: generate story + video prompt
    # print("\n[Agent] Step 1: Generating story and video prompt...")
    # story = get_story(topic)
    # video_prompts = get_video_prompts(topic, count=1)
    # video_prompt = video_prompts[0]
    # print(f"[Agent] Story: {story[:80]}...")
    # print(f"[Agent] Video prompt: {video_prompt}")

    # Step 2: generate voice
    # print("\n[Agent] Step 2: Generating voice...")
    # speaker_wav = os.path.join(root, "audio_ai", "voice_sample.wav")
    # voice_path = os.path.join(root, "temp", "content_voice.wav")
    # vg = VoiceGen(speaker_wav=speaker_wav)
    # vg.generate(story, output_path=voice_path)
    # print(f"[Agent] Voice ready: {voice_path}")

    # Step 3: generate video via meta.ai
    # print("\n[Agent] Step 3: Generating video...")
    # raw_video = generate_video(video_prompt)
    # video path comes from ~/Downloads — copy to temp so ffmpeg can access it
    # video_path = os.path.join(root, "temp", "input_video.mp4")
    # shutil.copy2(raw_video, video_path)
    # print(f"[Agent] Video ready: {video_path}")

    # --- Static paths for testing ---
    voice_path = os.path.join(root, "temp", "content_voice.wav")
    video_path = os.path.join(root, "temp", "input_video.mp4")
    print(f"[Agent] Video: {video_path}")
    print(f"[Agent] Voice: {voice_path}")

    # Step 4: combine video + voice
    print("\n[Agent] Step 4: Combining video and audio...")
    output_path = os.path.join(output_dir, "final_output.mp4")
    editor = VideoEditor()
    final_path = editor.combine(video_path, voice_path, output_path)

    print("\n" + "=" * 50)
    print(f"[Agent] Done. Final video: {final_path}")
    print("=" * 50)

    return final_path


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "a turtle exploring a magical pond"
    run(topic)
