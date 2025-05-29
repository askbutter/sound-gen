import random
from pydub import AudioSegment
from pydub.effects import low_pass_filter, normalize

'we r gonna use real samples of rain n thunder'

'take out settings and load rain samples instead'
rain_samples = [
    AudioSegment.from_file("rain1.mp3"),
    AudioSegment.from_file("rain2.wav"),
    AudioSegment.from_file("rain3.wav"),
]

# Load thunder samples
thunder_samples = [
    AudioSegment.from_file("thunder1.wav"),
    AudioSegment.from_file("thunder2.wav"),
]

def loop_segment(segment, target_duration_ms):
    """Loop audio segment until reaching at least target duration."""
    """loops short rain samples into 30 sec chuncks,
      until the length of the audio (2min or 8 hrs)
      This helps create continuous rain chunks by repeating shorter samples."""
    loops = target_duration_ms // len(segment) + 1
    return segment * loops

def generate_ambient_rain(duration_ms):
    """
    Generate ambient rain by randomly selecting rain samples,
    looping them to 30 seconds each, then concatenating until
    the desired total duration is reached.
    Volume is slightly raised randomly for natural variation.
    """
    output = AudioSegment.silent(duration=0)

    current_length = 0

    while current_length < duration_ms:
        rain = random.choice(rain_samples)
        # Loop or trim rain sample to 30 seconds
        chunk = loop_segment(rain, 30 * 1000)[:30 * 1000]
        # Slight volume increase (2 to 4 dB) for gentle boost
        chunk = chunk + random.randint(2, 4)
        
        # Apply low-pass filter around 6000 Hz to soften harsh highs
        chunk = low_pass_filter(chunk, 6000)
        
        # Add small fade-in/out to avoid pops between chunks
        chunk = chunk.fade_in(500).fade_out(500)
        
        # Optional: normalize to even out loudness
        chunk = normalize(chunk)
        
        output += chunk
        current_length = len(output)
    # Trim to exact duration
    return output[:duration_ms]

def add_thunder(ambient_rain, thunder_chance=0.1, min_gap_ms=5 * 60 * 1000):
    """
    Overlay thunder sounds sparsely on the ambient rain track.
    Thunder is faded in and out for smoothness and lowered in volume.
    Thunder events are spaced apart by at least min_gap_ms milliseconds.
    """
    output = ambient_rain
    pos = 0
    duration = len(output)
    while pos < duration:
        if random.random() < thunder_chance:
            thunder = random.choice(thunder_samples)
            # Reduce thunder volume by 10 dB for subtlety
            thunder = thunder - 10
            # Fade thunder in/out to blend naturally
            thunder = thunder.fade_in(1000).fade_out(2000)
            # Overlay thunder sound at current position
            output = output.overlay(thunder, position=pos)
            # Skip ahead by min_gap_ms to avoid clustering thunder
            pos += min_gap_ms
        else:
            # Check again after 18 minutes (18 * 60 * 1000 milliseconds)
            pos += 18 * 60 * 1000
    return output

if __name__ == "__main__":
    # 30 seconds duration for a quick sample (in milliseconds)
    total_duration = 30 * 1000

    print("Generating ambient rain...")
    ambient_rain = generate_ambient_rain(total_duration)

    print("Adding thunder...")
    final_audio = add_thunder(ambient_rain, thunder_chance=0.15, min_gap_ms=3 * 60 * 1000)

    # Export the final mixed audio to an MP3 file
    print("Exporting audio...")
    final_audio.export("ambient_rain_with_thunder_30sec.mp3", format="mp3")
    print("Done! File saved as 'ambient_rain_with_thunder_30sec.mp3'")