"""
agent.py
Orchestrates: content_gen → voice_gen → video_gen (multi-segment) → video_edit → output
"""

import sys
import os
import glob
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from content_ai.content_gen import get_story, get_video_prompts
from audio_ai.voice_gen import VoiceGen
from vision_ai.video_gen import generate_video
from video_edit.video_edit import VideoEditor


def run(topic: str):

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(root, "output")
    segments_dir = os.path.join(root, "temp", "video_segments")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(segments_dir, exist_ok=True)

    print("=" * 50)
    print(f"[Agent] Topic: {topic}")
    print("=" * 50)

    # Step 1: generate story + video prompts
    print("\n[Agent] Step 1: Generating story and video prompts...")
    story = get_story(topic)
    video_prompts = get_video_prompts(topic, user_request=topic)
    print(f"[Agent] Story: {story[:80]}...")
    print(f"[Agent] Video prompts: {len(video_prompts)}")

    # Step 2: generate voice
    print("\n[Agent] Step 2: Generating voice...")
    speaker_wav = os.path.join(root, "audio_ai", "voice_sample.wav")
    voice_path = os.path.join(root, "temp", "content_voice.wav")
    vg = VoiceGen(speaker_wav=speaker_wav)
    vg.generate(story, output_path=voice_path)
    print(f"[Agent] Voice ready: {voice_path}")

    # Step 3: generate video segments via meta.ai
    print("\n[Agent] Step 3: Generating video segments...")
    segment_paths = []
    for i, prompt in enumerate(video_prompts):
        print(f"[Agent] Segment {i+1}/{len(video_prompts)}: {prompt}")
        seg_path = generate_video(prompt)
        segment_paths.append(seg_path)
        print(f"[Agent] Segment {i+1} ready: {seg_path}")

    # Step 4: combine segments into content_video.mp4
    print("\n[Agent] Step 4: Combining video segments...")
    editor = VideoEditor()
    combined_video = os.path.join(root, "temp", "content_video.mp4")
    editor.combine_segments(segment_paths, combined_video)

    # Step 5: merge combined video with voice
    print("\n[Agent] Step 5: Merging video with voice...")
    final_path = os.path.join(output_dir, "final_output.mp4")
    editor.combine(combined_video, voice_path, final_path)

    print("\n" + "=" * 50)
    print(f"[Agent] Done. Final video: {final_path}")
    print("=" * 50)

    # Cleanup: delete all segment files in temp/video_segments/
    for f in os.listdir(segments_dir):
        file_path = os.path.join(segments_dir, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print("[Agent] Cleaned up temp/video_segments/")

    return final_path


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "a turtle exploring a magical pond"
    run(topic)
