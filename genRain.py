from pydub.generators import WhiteNoise   # Import generator to create white noise sounds
from pydub import AudioSegment             # Import AudioSegment class to manipulate audio segments
import random                             # Import random module to generate randomness (for thunder placement)

# --- SETTINGS ---
segment_hours = 2                        # Length of each audio segment in hours
segment_ms = segment_hours * 60 * 60 * 1000  # Convert hours to milliseconds (2 hours * 3600 seconds * 1000 ms)
num_segments = 4                        # Total number of segments to create (4 segments of 2 hours = 8 hours)
thunder_probability_per_segment = 0.3  # Probability of thunder occurring at each possible time slot (30%)
thunder_min_gap_ms = 28 * 60 * 1000    # Minimum gap between thunder sounds in milliseconds (20 minutes)
thunder_durations_ms = (3000, 5000)    # Tuple defining min and max thunder duration in milliseconds (3-5 seconds)

def generate_rain_segment():
    """Generate a 2-hour audio segment of gentle rain noise."""
    white = WhiteNoise().to_audio_segment(duration=segment_ms)  # Generate white noise for full segment length
    rain = white.low_pass_filter(8000).apply_gain(-10)         # Filter out high frequencies above 8kHz and reduce volume to soften sound
    return rain                                                # Return the processed rain sound segment

def generate_thunder(duration_ms):
    """Generate a thunder sound of a given duration."""
    thunder = WhiteNoise().to_audio_segment(duration=duration_ms)  # Generate white noise of thunder duration
    thunder = thunder.low_pass_filter(400).apply_gain(-5)         # Filter to lower frequencies (rumble) and raise volume slightly
    return thunder.fade_in(1000).fade_out(2000)                   # Smoothly fade in over 1s and fade out over 2s for natural effect

def add_thunder_to_segment(segment):
    """Add sparse thunder sounds spaced out within the given segment."""
    thunder_times = []       # List to keep track of thunder start times within the segment
    pos = 0                 # Initialize current position in segment at 0 ms (start)

    while pos < segment_ms - thunder_durations_ms[1]:  # Loop through segment until near the end (leave room for max thunder duration)
        if random.random() < thunder_probability_per_segment:  # Decide randomly if thunder should be placed here (30% chance)
            thunder_times.append(pos)           # Record this position as a thunder start time
            pos += thunder_min_gap_ms            # Skip forward by minimum gap (20 minutes) to space out thunder
        else:
            pos += 5 * 60 * 1000                 # Otherwise move forward by 5 minutes to check next possible position

    # Overlay thunder sounds at the recorded times
    for t_start in thunder_times:
        dur = random.randint(*thunder_durations_ms)           # Randomize thunder length between 3 and 5 seconds
        thunder_sound = generate_thunder(dur)                 # Generate thunder audio of that length
        segment = segment.overlay(thunder_sound, position=t_start)  # Overlay thunder sound on rain segment at start time

    return segment   # Return segment with thunder added

# --- Generate all 4 segments and concatenate ---
final_audio = AudioSegment.silent(duration=0)  # Start with an empty audio segment to concatenate onto

for i in range(num_segments):                   # Loop 4 times to generate 4 segments
    print(f"Generating segment {i+1}/{num_segments}...")  # Print progress
    segment = generate_rain_segment()           # Generate the 2-hour rain segment
    segment = add_thunder_to_segment(segment)   # Add sparse thunder sounds to the segment
    final_audio += segment                        # Concatenate this segment to the final audio

# --- Export the full 8-hour audio file ---
final_audio.export("gentle_rain_with_sparse_thunder_8h.mp3", format="mp3")  # Export the full concatenated audio as MP3
print("Finished! Exported 'gentle_rain_with_sparse_thunder_8h.mp3'")        # Notify completion
