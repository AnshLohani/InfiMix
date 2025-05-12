import sounddevice as sd
import numpy as np
import random
import time

# === Constants === 
sample_rate = 44100
amplitude = 0.3
blocksize = 1024
bass_freq = random.choice([55, 65, 73, 82])  # Notes in E1 to E2 range
bass_phase = 0.0

# === Musical Notes in Frequencies (C Major Scale) ===
notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]

# === Guitar Settings ===
guitar_freq = random.choice([164.81, 174.61, 196.00, 220.00, 246.94])  # E3 to E4
guitar_mod_speed = random.uniform(0.05, 0.1)  # Slower modulation
guitar_mod_depth = random.uniform(0.1, 0.3)   # Shallower modulation
guitar_phase = 0.0

# === Synth Voice Settings ===
num_voices = 4
base_frequencies = [random.choice(notes) for _ in range(num_voices)]
mod_speed = [random.uniform(0.05, 0.2) for _ in range(num_voices)]  # How fast frequency drifts 
mod_depth = [random.uniform(0.5, 3.0) for _ in range(num_voices)]  # How much the frequency drifts 

# === Phase Increment Function ===
phases = [0.0] * num_voices
two_pi = 2 * np.pi
time_counter = 0

# === Callback for Continuous Sound ===
def callback(outdata, frames, time_info, status):
    global time_counter, phases, guitar_phase, bass_phase  # Make sure these variables are global

    t = np.arange(frames) + time_counter
    t = t / sample_rate

    signal = np.zeros(frames)

    # Add the voices (synth sounds)
    for i in range(num_voices):
        mod = np.sin(two_pi * mod_speed[i] * t) * mod_depth[i]  # Modulation
        freq = base_frequencies[i] + mod
        wave = np.sin(phases[i] + two_pi * freq * (1/sample_rate) * np.arange(frames))

        phases[i] += two_pi * freq[-1] * frames / sample_rate
        signal += 0.4 * wave  # Reduced individual voice volume
    
    # Add the bass wave (lower frequency, softer volume)
    #bass_wave = np.sin(two_pi * bass_freq * t + bass_phase)
    #signal += 0.15 * bass_wave  # Lower the bass volume further

    # Add the guitar wave (with modulation)
    guitar_mod = 1 + (np.sin(two_pi * guitar_mod_speed * t)**2 * guitar_mod_depth)  # Smooth modulation
    #guitar_wave = guitar_mod * np.sin(two_pi * guitar_freq * t + guitar_phase)
    #signal += 0.25 * guitar_wave  # Moderate volume for the guitar

    # Normalize the signal to prevent clipping
    max_val = np.max(np.abs(signal))
    if max_val > 1.0:
        signal = signal / max_val  # Normalize if needed

    # Output the final signal
    outdata[:] = (amplitude / num_voices) * signal.reshape(-1, 1)
    time_counter += frames

    # Update phases
    guitar_phase += two_pi * guitar_freq * frames / sample_rate
    bass_phase += two_pi * bass_freq * frames / sample_rate

# === Playback ===
try:
    with sd.OutputStream(callback=callback, samplerate=sample_rate, channels=1, blocksize=blocksize):
        print("Playing ambient Sine Pad with Synth, Bass, and Guitar... Press Ctrl+C to stop.")
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped by User.")