# InfiMix - Infinite Music Generator

## Overview

**InfiMix** is an ambient music generator that creates infinite, unique music using wave-based synthesis. It generates loops that are rich in texture and can be used by streamers, cafes, workspaces, or anyone looking for ambient background music. The goal of this project is to provide a versatile and efficient way to generate beautiful-sounding, low-CPU music in real-time.

This project is built with Python, leveraging libraries like `sounddevice`, `numpy`, and `scipy` to generate the audio and provide users with an engaging experience.

## Features

- **Ambient Synth Textures**: Generate smooth, evolving ambient sounds using simple wave-based synthesis.
- **Dynamic Kick and Hi-Hat**: Add rhythmic beats to your ambient music with a customizable kick drum and hi-hat pattern generator.
- **LFO Modulation**: Frequency and amplitude modulation for adding depth to the sound.
- **Real-Time Audio**: Generate audio in real time, designed to be both low-latency and low-CPU intensive.
- **Infinite Loops**: Never-ending music that can be customized by adjusting various parameters like synth frequency, modulation depth, and more.

## Getting Started

### Prerequisites

1. Python 3.x installed on your machine.
2. The following Python libraries:
   - `sounddevice`
   - `numpy`
   - `scipy`

You can install the dependencies using `pip`:

```bash
pip install sounddevice numpy scipy
```

How to Run
Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/InfiMix.git
cd InfiMix
```
Run the script:

```bash
python main.py
```

The program will start generating ambient synth music along with kick drums and hi-hat patterns. Press Ctrl + C to stop.

## Goals Achieved

- **Basic Ambient Synth**: Successfully generated ambient synth textures with modulation.
- **Kick and Hi-Hat Integration**: Added rhythmic elements such as kick drums and hi-hats for more musical depth.
- **LFO Modulation**: Integrated frequency and amplitude LFOs for richer, evolving sounds.
- **Real-Time Audio Generation**: Implemented real-time audio generation using the sounddevice library.
- **Basic Rhythm Generation**: Randomized kick and hi-hat pattern generation.

## Future Goals
- **Intelligent Beat Placement Based on Synth Rhythm**: Implement algorithms that sync the beats (kick/hi-hat) with the current synth rhythm for more musical coherence.
- **Basic Mobile App GUI**: Create a mobile-friendly GUI for ease of use and accessibility, focusing on control of synth parameters and beat patterns.
- **More Complex Rhythmic Patterns**: Design and implement more advanced beat generation algorithms based on real-time input or user-defined patterns.
- **Multi-Genre Support**: Allow the user to select different genres for the ambient music (e.g., chill, electronic, lofi) and dynamically change the synthesis parameters based on the selected genre.
- **Customizable Synthesis Parameters**: Allow users to fine-tune the synth sounds, LFOs, and beat patterns in the app.
- **Web Version**: Implement a browser-based version of the music generator to make it accessible from any device.
- **Real-Time Audio Processing Effects**: Add real-time effects like reverb, delay, and EQ for better audio customization.

## Contributing
We welcome contributions to this project! If you have any suggestions, improvements, or bug fixes, feel free to reach out with your work to my given gmail address.
