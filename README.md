# Relativistic N-Body Solar System Simulation

A real-time Einstein-inspired solar system simulator developed using Python and Tkinter.

This project simulates planetary motion using Newtonian gravity combined with relativistic correction terms inspired by General Relativity. The simulator visualizes orbital mechanics, gravitational interactions, and relativistic orbital behavior in an interactive GUI environment.

---

# 1. Project Overview

This project implements a **2D relativistic-inspired solar system simulation** using Python and Tkinter.

The simulation models gravitational interactions between celestial bodies and visualizes orbital motion in real time.

Main features:

* Multi-body gravitational simulation
* Relativistic orbital correction
* Elliptical orbit initialization
* Real-time GUI animation
* Orbit trail visualization
* Velocity display
* Interactive zoom system
* Recursive body counting
* File-based planetary system loading

---

# 2. Requirements

The project was developed and tested using:

* Python 3.13.9
* Tkinter 8.6

Required Python modules:

```python
tkinter
math
```

Tkinter is included with most standard Python installations.

---

# 3. Project Files

Make sure the following files are located in the same directory:

```text
project_9001.py
planet.txt
README.md
```

Recommended structure:

```text
Relativistic-Solar-System/
│
├── project_9001.py
├── planet.txt
├── README.md
└── screenshot.png
```

---

# 4. How To Run

## Step 1 — Open Terminal

Open Terminal (Mac/Linux) or Command Prompt (Windows).

---

## Step 2 — Navigate To Project Folder

Example:

```bash
cd path/to/Relativistic-Solar-System
```

Example on Mac:

```bash
cd ~/Desktop/Relativistic-Solar-System
```

---

## Step 3 — Run The Program

Execute:

```bash
python project_9001.py
```

or on some systems:

```bash
python3 project_9001.py
```

---

# 5. Expected Output

After running the program:

* A simulation window will open
* Planets orbit around the Sun
* Each planet displays:

  * Planet name
  * Current velocity
  * Relativistic time factor
* Orbit trails are rendered in real time
* Relativistic orbital precession can be observed

---

# 6. Controls

| Action      | Description |
| ----------- | ----------- |
| Mouse Wheel | Zoom in/out |

The zoom system supports:

* Windows
* MacOS
* Linux

If the display appears too small or too large, use the mouse wheel to adjust the zoom level.

---

# 7. Input File Design (`planet.txt`)

Each line defines a celestial body using the following format:

```text
Name Mass X Y Color Radius Fixed
```

Example:

```text
Earth 3e-6 1 0 blue 6 False
```

Parameter explanation:

| Parameter | Description                    |
| --------- | ------------------------------ |
| Name      | Celestial body name            |
| Mass      | Mass in solar-mass units       |
| X Y       | Initial position in AU         |
| Color     | GUI display color              |
| Radius    | Visual radius                  |
| Fixed     | Whether the body is stationary |

---

# 8. Physics Model

The simulation combines:

* Newtonian gravity
* Relativistic correction terms

Newtonian gravity:

F = G\frac{m_1m_2}{r^2}

Relativistic correction:

F_{rel} \approx F_N\left(1+\frac{3GM}{rc^2}\right)

The relativistic correction introduces:

* orbital precession
* non-closed elliptical orbits
* Einstein-inspired orbital behavior

---

# 9. Numerical Integration

The simulation uses the **Velocity Verlet integration method**.

Advantages:

* improved stability
* better energy conservation
* more realistic orbital motion
* suitable for long-term simulation

This method is significantly more accurate than Euler integration.

---

# 10. Orbit Initialization

Initial velocities are calculated using the vis-viva equation:

v = \sqrt{GM\left(\frac{2}{r}-\frac{1}{a}\right)}

Purpose:

* generate stable elliptical orbits
* prevent chaotic initial motion

---

# 11. Relativistic Effects

The simulation approximates several General Relativity effects:

## Mercury Perihelion Precession

Planetary orbits slowly rotate over time instead of remaining perfectly closed.

## Gravitational Time Dilation

Time progresses differently near massive objects.

## Einstein-Inspired Orbital Dynamics

Orbital trajectories deviate slightly from purely Newtonian motion.

---

# 12. GUI System

The GUI is implemented using:

* Tkinter window
* Canvas rendering
* Real-time animation loop

Features:

* real-time simulation
* orbit trails
* velocity display
* zoom interaction
* spacetime-inspired visualization

---

# 13. Recursion Usage

Function:

```python
count_bodies_recursive()
```

Purpose:

* recursively count celestial bodies

This demonstrates:

* recursion
* base case design
* recursive problem solving

---

# 14. Error Handling

The program handles:

* missing files
* invalid data format
* missing Sun object
* invalid simulation input

---

# 15. Educational Purpose

This project demonstrates:

* object-oriented programming
* computational physics
* numerical simulation
* GUI programming
* recursion
* scientific visualization

It integrates physics, mathematics, and real-time visualization into an interactive educational simulation system.

---

# 16. Scientific Disclaimer

This project is NOT a full numerical solution of the Einstein Field Equations.

Instead, it uses a post-Newtonian relativistic approximation inspired by General Relativity in order to maintain computational efficiency and real-time visualization performance.

---

# 17. Author

Huaduo Li
COMP9001 Final Project
