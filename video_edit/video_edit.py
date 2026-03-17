"""
video_edit.py
Combines video segments and audio into a final output using moviepy.
"""

import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips


class VideoEditor:

    def combine_segments(self, segment_paths: list[str], output_path: str) -> str:
        """
        Concatenate multiple video segments into one file.
        Saves to output_path and returns the path.
        """
        print(f"[VideoEdit] Combining {len(segment_paths)} segments...")
        clips = [VideoFileClip(p) for p in segment_paths]
        final = concatenate_videoclips(clips, method="compose")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        final.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)

        for c in clips:
            c.close()
        final.close()

        print(f"[VideoEdit] Segments combined → {output_path}")
        return output_path

    def combine(self, video_path: str, audio_path: str, output_path: str) -> str:
        """
        Replace the audio of a video with the given audio file.
        Trims or loops video to match audio length.
        Saves result to output_path and returns the path.
        """
        print(f"[VideoEdit] Loading video: {video_path}")
        video = VideoFileClip(video_path)

        print(f"[VideoEdit] Loading audio: {audio_path}")
        audio = AudioFileClip(audio_path)

        # loop video if shorter than audio
        if video.duration < audio.duration:
            loops = int(audio.duration / video.duration) + 1
            video = concatenate_videoclips([video] * loops)

        video = video.subclip(0, audio.duration)
        final = video.set_audio(audio)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        print(f"[VideoEdit] Exporting to: {output_path}")
        final.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)

        video.close()
        audio.close()
        final.close()

        print(f"[VideoEdit] Done → {output_path}")
        return output_path
