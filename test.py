import sounddevice as sd
import numpy as np
import random
import time

# === Constants === 
sample_rate = 44100
amplitude = 0.3
blocksize = 1024
note_duration = 0.5 #How frequent to change notes 

# === Musical Notes in Frequencies (C Major Scale) ===
notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493,88]


# === Phase Tracker ===
phase = 0.0
two_pi = 2 * np.pi
current_frequency = random.choice(notes)

# === Phase Increment Function ===
def get_phase_increment(freq):
    return (two_pi * freq) / sample_rate

# === Time to change Note ===
next_note_change_time = time.time() + note_duration

# === Callback for Continuous Sound ===
def callback(outdata, frames, time_info, status):
    global phase, current_frequency, next_note_change_time

    t = np.arange(frames)
    wave = amplitude * np.sin(phase + get_phase_increment(current_frequency) * t) # Wave Generation

    phase += get_phase_increment(current_frequency) * frames
    phase = np.mod(phase, two_pi) # Keep phase on [0,2pi]

    outdata[:] = wave.reshape(-1,1)

    # Check if time to Change the note
    if time.time() >= next_note_change_time:
        current_frequency = random.choice(notes)
        next_note_change_time = time.time() + note_duration


# === Playback ===
try:
    with sd.OutputStream(callback=callback, samplerate=sample_rate, channels=1, blocksize=blocksize):
        print("Playing random notes from C major Scale... Press Ctrl+C to stop.")
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped by User.")


  