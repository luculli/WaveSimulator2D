### Update 20.11.2025 (Ver. 1.0.2)

* Refactored simulator


### Update 18.11.2025 (Ver. 1.0.1)

* Made python code into a package
* Added some documentation in docs/


### Update 06.04.2025

* Scene objects can now draw to a visualization layer (most of them do not yet, feel free to contribute) !
* Example 4 now shows a two-mirror optical cavity and how standing waves emerge.
* Added new Line Sources
* Added Refractive index Polygon object (StaticRefractiveIndexPolygon)
* Added Refractive index Box object (StaticRefractiveIndexBox)
* Fixed some issues with the examples

<div style="display: flex;">
    <img src="images/optical_cavity.jpg" alt="Example 4 - Optical Cavity with Standing Waves" width="50%">
</div>


### Update 01.04.2024

* Refactored the code to support a more flexible scene description. A simulation scene now consists of a list of objects that add their contribution to the fields.
They can be combined to build complex and time dependent simulations. The refactoring also made the core simulation code even simpler.
* Added a few new custom colormaps that work well for wave simulations.
* Added new examples, which should make it easier to understand the usage of the program and how you can setup your own simulations: [examples](source/examples).

<div style="display: flex;">
    <img src="images/simulation_3.jpg" alt="Example Image 3" width="45%">
    <img src="images/simulation_4.jpg" alt="Example Image 4" width="45%">
</div>

The old image based scene description is still available as a scene object. You can continue to use the convenience of an image editing software and create simulations
without much programming.
