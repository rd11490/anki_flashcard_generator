from google.cloud import texttospeech
from google.oauth2 import service_account
from secrets import google_tts_key_location

def create_mp3(text, location, file_name):

    # Authenticate using the service account key
    credentials = service_account.Credentials.from_service_account_file(google_tts_key_location)

    # Create the Text-to-Speech client with credentials
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    # Input text
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Voice configuration
    voice = texttospeech.VoiceSelectionParams(
        language_code="cmn-CN",
        name="cmn-CN-Wavenet-A",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    # Audio configuration
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Request TTS
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    file_path = f"{location}/{file_name}.mp3"
    # Save the audio as an MP3 file
    with open(file_path, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to 'output.mp3'")
    return file_path
