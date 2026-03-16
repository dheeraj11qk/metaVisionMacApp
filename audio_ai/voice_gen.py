from TTS.api import TTS


# ffmpeg -i voices/my_voice.mp4 voices/my_voice.wav

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

text = """
In this demo, we are going to demonstrate a flow where we will be registering a loan provider.
"""
tts.tts_to_file(
    text=text,
    speaker_wav="voice_sample.wav",
    language="en",
    #  temperature=0.3,
    emotion="calm",
    file_path="voice_output.wav"
)

print("Voice generated: voice_output.wav")