from pydub import AudioSegment

def slow_down_audio(input_file, output_file, speed=0.75):
    # Load audio file
    audio = AudioSegment.from_file(input_file)

    # Change speed (stretch audio duration)
    slowed_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed)
    })

    # Export slowed audio
    slowed_audio.export(output_file, format="mp3")

# Example Usage
slow_down_audio("stories/25-02-11-00:13:38/story_25-02-11-00:13:38.mp3", "stories/25-02-11-00:13:38/story_25-02-11-00:13:38_5.mp3", speed=0.5)