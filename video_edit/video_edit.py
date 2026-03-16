"""
video_edit.py
Combines a video file and an audio file into a final output using moviepy.
"""

import os
from moviepy.editor import VideoFileClip, AudioFileClip


class VideoEditor:

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

        # trim video to audio length if video is longer, loop if shorter
        if video.duration < audio.duration:
            from moviepy.editor import concatenate_videoclips
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
