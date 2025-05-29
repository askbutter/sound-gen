import random
from pydub.generators import WhiteNoise
from pydub import AudioSegment

# --- SETTINGS ---
duration_ms = 2 * 60 * 1000  # 2 minutes in milliseconds
thunder_probability = 0.3
thunder_min_gap_ms = 20 * 1000  # 20 seconds (shorter for sample)
thunder_durations_ms = (1500, 3000)

def generate_gentle_rain(duration):
    """Layered white noise for more natural rain."""
    base = WhiteNoise().to_audio_segment(duration=duration)
    layer1 = base.low_pass_filter(7000).high_pass_filter(300).apply_gain(-14)
    layer2 = base.low_pass_filter(9000).high_pass_filter(1000).apply_gain(-18)
    return layer1.overlay(layer2, position=20)

def generate_softer_thunder(duration):
    """Soft low-frequency thunder rumble."""
    thunder = WhiteNoise().to_audio_segment(duration=duration)
    thunder = thunder.low_pass_filter(250).apply_gain(-12)
    return thunder.fade_in(1000).fade_out(2000)

def add_sparse_thunder(segment):
    """Randomly place gentle thunder in segment."""
    pos = 0
    while pos < duration_ms - thunder_durations_ms[1]:
        if random.random() < thunder_probability:
            thunder = generate_softer_thunder(random.randint(*thunder_durations_ms))
            segment = segment.overlay(thunder, position=pos)
            pos += thunder_min_gap_ms
        else:
            pos += 10 * 1000  # move ahead 10s
    return segment

# --- Generate 2-minute preview ---
print("🎧 Generating 2-minute rain sample with sparse thunder...")
rain = generate_gentle_rain(duration_ms)
sample = add_sparse_thunder(rain)

# --- Export sample ---
sample.export("gentle_rain_sample_2min.mp3", format="mp3")
print("✅ Sample saved as 'gentle_rain_sample_2min.mp3'")
