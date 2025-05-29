from pydub.generators import WhiteNoise
from pydub import AudioSegment
import random
import os

# --- SETTINGS ---
hours = 8
segment_minutes = 30
segment_ms = segment_minutes * 60 * 1000
total_segments = int((hours * 60) / segment_minutes)
final_audio = AudioSegment.silent(duration=0)

def generate_rain_segment():
    white = WhiteNoise().to_audio_segment(duration=segment_ms)
    rain = white.low_pass_filter(8000).apply_gain(-10)
    return rain

def generate_thunder():
    dur = random.randint(2000, 5000)
    thunder = WhiteNoise().to_audio_segment(duration=dur)
    thunder = thunder.low_pass_filter(400).apply_gain(-5)
    return thunder.fade_in(1000).fade_out(2000)

# Build segments
for i in range(total_segments):
    rain = generate_rain_segment()
    # Add thunder randomly
    if random.random() < 0.6:  # ~60% chance of thunder in a 30-min segment
        position = random.randint(1 * 60 * 1000, segment_ms - 5 * 1000)
        rain = rain.overlay(generate_thunder(), position=position)
    final_audio += rain

# Export
final_audio.export("gentle_rain_with_thunder_8h.mp3", format="mp3")
print("Exported: gentle_rain_with_thunder_8h.mp3")
