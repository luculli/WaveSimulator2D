# 2D Wave Simulation on the GPU

This repository contains a lightweight 2D wave simulator running on the GPU using CuPy library (probably requires a NVIDIA GPU). It can be used for 2D light and sound simulations.
A simple visualizer shows the field and its intensity on the screen and writes a movie file for each to disks. The goal is to provide a fast, easy to use but still felxible wave simulator.

<div style="display: flex;">
    <img src="images/simulation_1.jpg" alt="Example Image 1" width="49%">
    <img src="images/simulation_2.jpg" alt="Example Image 2" width="49%">
</div>

###  Image Scene Description Usage

When using the 'StaticImageScene' class the simulation scenes can given as an 8Bit RGB image with the following channel semantics:
* Red:   The Refractive index times 100 (for refractive index 1.5 you would use value 150)
* Green: Each pixel with a green value above 0 is a sinusoidal wave source. The green value defines its frequency.
* Blue:  Absorbtion field. Larger values correspond to higher dampening of the waves, use graduated transitions to avoid reflections

WARNING: Do not use anti-aliasing for the green channel ! The shades produced are interpreted as different source frequencies, which yields weird results.

<div style="display: flex;">
    <img src="images/source_antialiasing.png" alt="Example Image 5" width="50%">
</div>

### Recommended Installation for PyCharm

1. Install Python and PyCharm IDE
2. Clone the Project to you hard disk
3. Open the folder as a Project using PyCharm
4. If prompted to install requirements, accept (or install requirements using pip -r requirements.txt)
5. Right click on one of the examples in the folder examples/ and select run

### Recommended Installation for Python cli

1. Install module: pip install -e .
2. Run example: python examples/example0.py


