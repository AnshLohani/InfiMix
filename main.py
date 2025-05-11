import sounddevice as sd
import numpy as np
import random
import time

# === Constants === 
sample_rate = 44100
amplitude = 0.3
blocksize = 1024

# === Synth Voice Settings ===
num_voices = 5
base_frequencies = [random.uniform(100,500) for _ in range(num_voices)]
mod_speed = [random.uniform(0.05,0.2) for _ in range(num_voices)] # How fast frequency drifts 
mod_depth = [random.uniform(0.5,5.0) for _ in range(num_voices)] # How much the frequency drifts 

# === Phase Increment Function ===
phases = [0.0] * num_voices
two_pi = 2 * np.pi
time_counter = 0

# === Callback for Continuous Sound ===
def callback(outdata, frames, time_info, status):
    global time_counter, phases

    t = np.arange(frames) + time_counter
    t = t / sample_rate

    signal = np.zeros(frames)

    for i in range(num_voices):
        # Frequency drift via slow sine LFO (Low Frequency Osciallator)
        mod = np.sin( two_pi * mod_speed[i] * t) * mod_depth[i]
        freq = base_frequencies[i] + mod
        wave = np.sin(phases[i] + two_pi * freq * (1/sample_rate) * np.arange(frames))

        phases[i] += two_pi * freq[-1] * frames / sample_rate
        signal += wave
    
    # Normalize the signal
    signal = ( amplitude / num_voices ) * signal 
    outdata[:] = signal.reshape(-1,1)
    time_counter += frames


# === Playback ===
try:
    with sd.OutputStream(callback=callback, samplerate=sample_rate, channels=1, blocksize=blocksize):
        print("Playing ambient Sine Pad... Press Ctrl+C to stop.")
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped by User.")


  