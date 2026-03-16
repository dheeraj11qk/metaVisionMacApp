"""
voice_gen.py
Generates natural-sounding voice audio with human pauses between segments.
"""

import os
import shutil
import uuid
from TTS.api import TTS
from pydub import AudioSegment


class VoiceGen:
    """
    Splits text into segments, generates audio for each with human-like pauses,
    then merges into a single output file.
    """

    PAUSE_SHORT  = 400   # ms — comma / breath pause
    PAUSE_MEDIUM = 700   # ms — sentence end pause
    PAUSE_LONG   = 1200  # ms — paragraph / section pause

    def __init__(
        self,
        speaker_wav: str = "voice_sample.wav",
        language: str = "en",
        model: str = "tts_models/multilingual/multi-dataset/xtts_v2",
    ):
        print("[VoiceGen] Loading TTS model...")
        self.tts = TTS(model_name=model)
        self.speaker_wav = speaker_wav
        self.language = language
        print("[VoiceGen] Model ready.")

    def _split_segments(self, text: str) -> list[tuple[str, int]]:
        """
        Split text into (segment, pause_ms) tuples.
        Paragraphs → long pause, sentences → medium, clauses → short.
        """
        segments = []
        paragraphs = [p.strip() for p in text.strip().split("\n\n") if p.strip()]

        for i, para in enumerate(paragraphs):
            sentences = [s.strip() for s in para.replace("...", "…").split(".") if s.strip()]
            for j, sentence in enumerate(sentences):
                # split on commas for short pauses
                clauses = [c.strip() for c in sentence.split(",") if c.strip()]
                for k, clause in enumerate(clauses):
                    if not clause:
                        continue
                    # determine trailing pause
                    if k < len(clauses) - 1:
                        pause = self.PAUSE_SHORT
                    elif j < len(sentences) - 1:
                        pause = self.PAUSE_MEDIUM
                    else:
                        pause = self.PAUSE_LONG
                    segments.append((clause, pause))

        return segments

    def generate(self, text: str, output_path: str = "voice_output.wav") -> str:
        """
        Generate voice audio for the given text and save to output_path.
        Returns the output file path.
        """
        segments = self._split_segments(text)
        print(f"[VoiceGen] {len(segments)} segments to process")

        audio_parts = []

        # use project root /temp/segments for segment files
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tmp_dir = os.path.join(root, "temp", "segments", uuid.uuid4().hex)
        os.makedirs(tmp_dir, exist_ok=True)

        try:
            for i, (segment, pause_ms) in enumerate(segments):
                tmp_path = os.path.join(tmp_dir, f"seg_{i}.wav")
                print(f"[VoiceGen] [{i+1}/{len(segments)}] '{segment[:60]}' pause={pause_ms}ms")

                self.tts.tts_to_file(
                    text=segment,
                    speaker_wav=self.speaker_wav,
                    language=self.language,
                    file_path=tmp_path,
                )

                audio_parts.append(AudioSegment.from_wav(tmp_path))
                audio_parts.append(AudioSegment.silent(duration=pause_ms))
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

        print("[VoiceGen] Merging segments...")
        final = sum(audio_parts, AudioSegment.empty())
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        final.export(output_path, format="wav")

        print(f"[VoiceGen] Done → {output_path} ({len(final)/1000:.1f}s)")
        return output_path


if __name__ == "__main__":
    vg = VoiceGen(speaker_wav="voice_sample.wav")

    story = """
Once upon a time, in a quiet pond at the edge of a forest, there lived a small turtle named Teo.
"""

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "temp", "turtle_story.wav")
    vg.generate(story, output_path=out)
    print("Saved to:", out)
