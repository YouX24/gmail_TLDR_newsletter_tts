import os
from google.cloud import texttospeech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "tts_key.json"
cleint = texttospeech.TextToSpeechClient()

# turn text to speech
def synthesize_text(txt):
    input_text = texttospeech.SynthesisInput(text=txt)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-F",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.25,
    )

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech({
        "input": input_text,
        "voice": voice,
        "audio_config": audio_config,
        }
    )

    # The response's audio_content is binary.
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Generated speech audio saved to output.mp3')


with open("output.txt", "r", encoding="utf8") as textFile:
    content = textFile.read()
    synthesize_text(content)