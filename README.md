# COMP9001-Final-Project
N-Body Solar System Simulation
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 12:26:20 2026

@author: lihuaduo
"""

N-Body Solar System Simulation (Final Project 9001)

 1. Project Overview

This project implements a **2D solar system simulation** using Python and Tkinter. It models gravitational interactions between celestial bodies based on Newtonian physics.

Main features:

* Multi-body gravitational simulation
* Elliptical orbit initialization
* Real-time animation using GUI
* Zoomable visualization
* Orbit trails and speed display


2. How to Run
 Requirements

Python version: 3.13.9 
| packaged by Anaconda, Inc. 
| (main, Oct 21 2025, 19:11:29) [Clang 20.1.8 ]
Tkinter version: 8.6
9001 final project

Run Steps

1. Make sure the following files are in the same directory:

   * `project_9001.py`
   * `planet.txt`

2. Run the program:

```bash
python project_9001.py
```

 Expected Output

* A window (800×800) will open
* Planets orbit around the Sun
* Each planet displays:

  * Name
  * Current speed
* Orbit trails are visible

Controls

| Action      | Description   |
| ----------- | ------------- |
| Mouse wheel | Zoom in / out |

---

3. Input File Design (`planet.txt`)

Each line defines a celestial body using the following format:

```
Name Mass X Y Color Radius Fixed
```

Example:

```
Earth 3e-6 1 0 blue 6 False
```

Explanation:

* Mass: in solar mass units
* Position: in astronomical units (AU)
* Color: used for GUI display
* Radius: visual size
* Fixed: whether the body is stationary (e.g., Sun)

---

4. System Design

4.1 Body Class

The `Body` class represents each celestial object.

Attributes:

* Position and velocity
* Mass
* Display color
* Radius
* Orbit trail

Design purpose:

* Encapsulates both physical and visual properties
* Simplifies simulation and rendering logic

---

4.2 Physics Engine

The `Physics` class is responsible for:

* Computing gravitational forces
* Updating positions and velocities

Integration Method: Velocity Verlet

This method is used instead of Euler integration because:

* It is more stable
* It preserves energy better
* It is suitable for orbital simulations

---

4.3 Gravitational Model

The simulation uses Newton's law of gravitation:

F = G * m1 * m2 / r^2

Design notes:

* The gravitational constant is scaled as:
  G = 4π²
* This works well with astronomical units and keeps values stable

---

4.4 Orbit Initialization

Initial velocities are calculated using the vis-viva equation:

v = sqrt(GM(2/r - 1/a))

Design purpose:

* Ensures planets start in stable elliptical orbits
* Avoids chaotic or unrealistic motion

---

4.5 Recursion Usage

Function:

```python
count_bodies_recursive()
```

Purpose:

* Counts the number of bodies recursively

Design significance:

* Demonstrates recursion as required by the course
* Shows understanding of base case and recursive step

---

4.6 GUI System (Tkinter)

The GUI is implemented using:

* Tkinter window
* Canvas for drawing
* `after()` for animation loop (~60 FPS)

Features:

* Real-time updates
* Orbit trails
* Speed display

---

4.7 Visualization Design

Logarithmic Scaling

Distance is transformed using logarithmic scaling:

* Prevents outer planets from being too far away
* Improves visualization of the entire system

Orbit Trails

* Each body stores recent positions
* Trail length is limited to 200 points
* Prevents memory overflow

---

4.8 Zoom Interaction

* Controlled via mouse wheel
* Supports Windows, Mac, and Linux
* Zoom range is limited to prevent crashes
* If you find the display too small, 
* you can adjust the zoom level on line 182, 
* or you can use mouse scrolling to zoom in and out. 
* The zoom value of 25 is only suitable for my computer's window;
* I'm not sure how it will work on other computer windows, 
* so I added mouse scrolling and zoom settings specifically to adapt to other computer windows.

---

5. Error Handling

The program handles basic errors:

* File not found
* Invalid data format
* Missing Sun object

---

6. Conclusion

This project demonstrates:

* Object-oriented programming
* Numerical physics simulation
* GUI development
* Recursion usage

It integrates physics, visualization, and user interaction into a functional and educational simulation system.
