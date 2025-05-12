import sounddevice as sd
import numpy as np
import time
import random


# === Constants ===
sample_rate = 44100
blocksize = 1024
amplitude = 0.3
two_pi = 2 * np.pi

# === Ambient Synth Settings ===
synth_freq = 220.0  # Base frequency (A3)
synth_phase = 0.0

# Frequency LFO
freq_lfo_speed = 0.1  # Hz
freq_lfo_depth = 10.0  # Hz

# Amplitude LFO
amp_lfo_speed = 0.05  # Hz
amp_lfo_depth = 0.4  # 0 to 1 scale

# === Kick Drum Settings ===
#kick_interval = 0.5  # Every 0.5s = 120 BPM
last_kick_time = 0.0
kick_sample = np.array([])
kick_position = 0

# === Hi-Hat Settings ===
#hat_interval = 0.25  # Every 0.25s = Offbeat hat
last_hat_time = 0.0
hat_sample = np.array([])
hat_position = 0

# === Time Counter ===
time_counter = 0

# === Drum Generators ===
def generate_kick(length):
    t = np.linspace(0, length / sample_rate, length, False)
    
    # Exponential pitch drop from 100Hz to ~40Hz
    freq = 60 * np.exp(-5 * t) + 40
    phase = np.cumsum(freq) / sample_rate * two_pi
    body = np.sin(phase)

    # Smooth envelope, slow decay for sub-bass thump
    envelope = np.exp(-8 * t)
    
    # Optional: Add click at start (transient)
    click = np.zeros_like(t)
    click_len = int(sample_rate * 0.005)
    click[:click_len] = np.hanning(click_len) * 0.8

    return (body * envelope + click) * 1.2

def generate_hat(length):
    t = np.linspace(0, length / sample_rate, length, False)
    noise = np.random.uniform(-1, 1, size=length)
    envelope = np.exp(-50 * t)
    return envelope * noise

# === Callback ===
def callback(outdata, frames, time_info, status):
    global time_counter, synth_phase
    global last_kick_time, kick_sample, kick_position
    global last_hat_time, hat_sample, hat_position

    t = np.arange(frames) + time_counter
    t = t / sample_rate

    signal = np.zeros(frames)

    # === Ambient Synth ===
    freq_lfo = np.sin(two_pi * freq_lfo_speed * t) * freq_lfo_depth
    amp_lfo = 1 - amp_lfo_depth * (1 + np.sin(two_pi * amp_lfo_speed * t)) / 2
    synth_wave = amp_lfo * np.sin(synth_phase + two_pi * (synth_freq + freq_lfo) * (1 / sample_rate) * np.arange(frames))
    synth_phase += two_pi * (synth_freq + freq_lfo[-1]) * frames / sample_rate
    signal += 0.2 * synth_wave

    # === Kick Trigger ===
    current_time = time_counter / sample_rate
    kick_interval = random.choice([0.5,1,0.5])  # Every 0.5s = 120 BPM
    if current_time - last_kick_time >= kick_interval:
        kick_sample = generate_kick(sample_rate // 6)  # ~0.16s kick
        kick_position = 0
        last_kick_time = current_time

    # Add kick if still playing
    if kick_position < len(kick_sample):
        chunk = kick_sample[kick_position:kick_position+frames]
        if len(chunk) < frames:
            chunk = np.pad(chunk, (0, frames - len(chunk)))
        signal += 0.5 * chunk
        kick_position += frames

    # === Hi-Hat Trigger ===
    hat_interval = random.choice([0.25,0.5,1,0.25])  # Every 0.25s = Offbeat hat
    if current_time - last_hat_time >= hat_interval:
        hat_sample = generate_hat(sample_rate // 12)  # ~0.08s hat
        hat_position = 0
        last_hat_time = current_time

    if hat_position < len(hat_sample):
        chunk = hat_sample[hat_position:hat_position+frames]
        if len(chunk) < frames:
            chunk = np.pad(chunk, (0, frames - len(chunk)))
        signal += 0.05 * chunk
        hat_position += frames

    # === Output ===
    outdata[:] = (amplitude * signal).reshape(-1, 1)
    time_counter += frames

# === Start Stream ===
try:
    with sd.OutputStream(callback=callback, samplerate=sample_rate, channels=1, blocksize=blocksize):
        print("Playing ambient synth with kick drum and hi-hat... Press Ctrl+C to stop.")
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped by user.")