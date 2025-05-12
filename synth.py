import sounddevice as sd
import numpy as np
import random
import time

# === Constants ===
sample_rate = 44100
amplitude = 0.1
blocksize = 1024
two_pi = 2 * np.pi

# === Musical Notes (C major) ===
notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]

# === Voice Settings ===
num_voices = 4
phases = [0.0] * num_voices
current_freqs = [random.choice(notes) for _ in range(num_voices)]
target_freqs = current_freqs.copy()
glide_durations = [2.0] * num_voices  # seconds
glide_timers = [0.0] * num_voices
change_intervals = [random.uniform(2.0, 7.0) for _ in range(num_voices)]
change_timers = [0.0] * num_voices

# === LFO Settings (Frequency Modulation) ===
lfo_speed = [random.uniform(0.1, 3.0) for _ in range(num_voices)]  # LFO Speed (in Hz)
lfo_depth = [random.uniform(0.05, 0.2) for _ in range(num_voices)]  # How much the LFO modulates the frequency

# === Amplitude Modulation Settings ===
amp_lfo_speed = [random.uniform(0.1, 1.0) for _ in range(num_voices)]  # LFO Speed (in Hz) for amplitude modulation
amp_lfo_depth = [random.uniform(0.5, 1.0) for _ in range(num_voices)]  # LFO Depth for amplitude modulation

time_counter = 0

# === Smooth Linear Glide ===
def interpolate(start, end, progress):
    return (1 - progress) * start + progress * end

# === Callback ===
def callback(outdata, frames, time_info, status):
    global time_counter, phases, current_freqs, target_freqs, glide_timers, change_timers, lfo_depth, lfo_speed, amp_lfo_speed, amp_lfo_depth

    t = (np.arange(frames) + time_counter) / sample_rate
    signal = np.zeros(frames)

    for i in range(num_voices):
        # Update timers
        glide_timers[i] += frames / sample_rate
        change_timers[i] += frames / sample_rate

        # If it's time to change target note
        if change_timers[i] >= change_intervals[i]:
            change_timers[i] = 0.0
            glide_timers[i] = 0.0
            current_freqs[i] = target_freqs[i]  # lock in current freq
            target_freqs[i] = random.choice(notes)  # new target
            change_intervals[i] = random.uniform(4.0, 7.0)

        # LFO modulation for frequency
        lfo_freq = np.sin(two_pi * lfo_speed[i] * t) * lfo_depth[i]  # Frequency modulation LFO
        modulated_freq = current_freqs[i] + lfo_freq

        # Calculate the final frequency using linear interpolation
        progress = min(glide_timers[i] / glide_durations[i], 1.0)
        freq = interpolate(modulated_freq, target_freqs[i], progress)

        # Generate wave
        wave = np.sin(phases[i] + two_pi * freq * (1/sample_rate) * np.arange(frames))
        phases[i] += two_pi * freq * frames / sample_rate

        # LFO modulation for amplitude (tremolo effect)
        amp_lfo = 1 + np.sin(two_pi * amp_lfo_speed[i] * t) * amp_lfo_depth[i]  # Amplitude modulation LFO
        wave *= amp_lfo  # Apply amplitude modulation

        signal += wave

    # Normalize the signal
    signal *= (amplitude / num_voices)
    outdata[:] = signal.reshape(-1, 1)
    time_counter += frames

# === Playback ===
try:
    with sd.OutputStream(callback=callback, samplerate=sample_rate, channels=1, blocksize=blocksize):
        print("Playing ambient synth with smooth note glides, LFO modulation (frequency and amplitude)... Press Ctrl+C to stop.")
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped by User.")