#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Wed Apr 29 16:55:33 2026
HUADUO LI
sid:550239448
Python version: 3.13.9 
| packaged by Anaconda, Inc. 
| (main, Oct 21 2025, 19:11:29) [Clang 20.1.8 ]
Tkinter version: 8.6
9001 final project
@author: lihuaduo

Relativistic Solar System Simulator
Einstein-inspired orbital mechanics simulation

Features:
- Newtonian + relativistic gravity correction
- Multi-body orbital simulation
- Velocity Verlet integration
- Orbit trails
- Mercury perihelion precession
- Zoom interaction
- Tkinter GUI
- File-based planetary system
"""


import tkinter as tk                       # Import Tkinter for GUI rendering
import math                                # Import math module for calculations

# =========================================================
# Constants
# =========================================================

G = 4 * math.pi**2                         # Gravitational constant in AU/year units
c = 63239.7                                # Speed of light in AU/year

dt = 0.001                                 # Simulation timestep

WIDTH = 1000                               # Width of simulation window
HEIGHT = 1000                              # Height of simulation window

# =========================================================
# Body Class
# =========================================================

class Body:

    def __init__(self, name, mass, pos, color, radius=5, fixed=False):

        self.name = name                   # Name of the celestial body
        self.mass = mass                   # Mass of the body
        self.pos = pos[:]                  # Copy of position vector [x, y]
        self.vel = [0, 0]                  # Initial velocity vector

        self.color = color                 # Display color
        self.radius = radius               # Radius for GUI drawing
        self.fixed = fixed                 # Whether body is fixed in space

        self.trail = []                    # Store previous positions

        self.last_r = None                 # Store previous orbital distance
        self.perihelion_points = []        # Store perihelion markers


# =========================================================
# Load Planet Data From File
# =========================================================


def load_bodies(filename):                 # Function to load planets from file

    bodies = []                            # Create empty body list

    try:

        with open(filename, "r") as f:    # Open data file

            for line in f:                 # Read file line by line

                parts = line.strip().split() # Split line into tokens

                if len(parts) < 7:         # Validate data format
                    continue               # Skip invalid lines

                name = parts[0]            # Read body name
                mass = float(parts[1])     # Read body mass
                x = float(parts[2])        # Read x coordinate
                y = float(parts[3])        # Read y coordinate
                color = parts[4]           # Read display color
                radius = int(parts[5])     # Read body radius
                fixed = parts[6] == "True" # Convert fixed flag to boolean

                bodies.append(             # Create and append Body object
                    Body(name, mass, [x, y], color, radius, fixed)
                )

    except FileNotFoundError:              # Handle missing file error

        print("planet.txt not found")     # Print error message
        return []                          # Return empty list

    return bodies                          # Return loaded bodies


# =========================================================
# Recursive Counting Function
# =========================================================


def count_bodies_recursive(bodies, index=0):

    if index >= len(bodies):               # Base case
        return 0                           # Stop recursion

    return 1 + count_bodies_recursive(     # Recursive step
        bodies,
        index + 1
    )


# =========================================================
# Orbit Initialization
# =========================================================


def init_orbit(body, sun, eccentricity):

    dx = body.pos[0] - sun.pos[0]          # X distance from Sun
    dy = body.pos[1] - sun.pos[1]          # Y distance from Sun

    r = math.sqrt(dx**2 + dy**2)           # Radial distance

    a = r / (1 - eccentricity)             # Semi-major axis

    v = math.sqrt(                         # Vis-viva equation
        G * sun.mass * (2/r - 1/a)
    )

    body.vel[0] = -v * dy / r              # Perpendicular x velocity
    body.vel[1] =  v * dx / r              # Perpendicular y velocity


# =========================================================
# Physics Engine
# =========================================================

class Physics:

    def __init__(self, bodies, relativistic=True):

        self.bodies = bodies               # Store all bodies
        self.relativistic = relativistic   # Enable relativistic correction


    def forces(self):

        F = []                             # Store force vectors

        for i, b1 in enumerate(self.bodies):

            fx = 0                         # Net force x component
            fy = 0                         # Net force y component

            for j, b2 in enumerate(self.bodies):

                if i == j:                 # Skip self-interaction
                    continue

                dx = b2.pos[0] - b1.pos[0] # Distance x
                dy = b2.pos[1] - b1.pos[1] # Distance y

                r = math.sqrt(dx*dx + dy*dy) + 1e-9 # Radial distance

                # =====================================================
                # Newtonian Gravity
                # =====================================================

                f_newton = G * b1.mass * b2.mass / r**2

                # =====================================================
                # Einstein-Inspired Relativistic Correction
                # =====================================================

                if self.relativistic:

                    correction = 1 + (3 * G * b2.mass) / (r * c**2)

                    f = f_newton * correction

                else:

                    f = f_newton

                fx += f * dx / r           # Add x force component
                fy += f * dy / r           # Add y force component

            F.append((fx, fy))             # Save total force

        return F                           # Return force list


    def step(self, dt):

        F = self.forces()                  # Compute current forces

        acc = [                            # Compute accelerations
            (
                fx/b.mass if not b.fixed else 0,
                fy/b.mass if not b.fixed else 0
            )
            for b, (fx, fy) in zip(self.bodies, F)
        ]

        # =====================================================
        # Position Update (Velocity Verlet)
        # =====================================================

        for i, b in enumerate(self.bodies):

            if b.fixed:
                continue

            ax, ay = acc[i]                # Current acceleration

            b.pos[0] += b.vel[0]*dt + 0.5*ax*dt*dt
            b.pos[1] += b.vel[1]*dt + 0.5*ay*dt*dt


        F2 = self.forces()                 # Recalculate forces

        # =====================================================
        # Velocity Update
        # =====================================================

        for i, b in enumerate(self.bodies):

            if b.fixed:
                continue

            ax1, ay1 = acc[i]              # Old acceleration

            fx, fy = F2[i]                 # New force

            ax2 = fx / b.mass              # New acceleration x
            ay2 = fy / b.mass              # New acceleration y

            b.vel[0] += 0.5 * (ax1 + ax2) * dt
            b.vel[1] += 0.5 * (ay1 + ay2) * dt


# =========================================================
# Setup Simulation
# =========================================================

bodies = load_bodies("planet.txt")        # Load all planets

if not bodies:                             # Stop if loading failed
    raise SystemExit("Simulation aborted")

sun = None                                 # Initialize Sun variable

for b in bodies:                           # Find Sun object

    if b.name == "Sun":

        sun = b
        break

if sun is None:                            # Validate Sun existence
    raise ValueError("Sun not found")


for b in bodies:                           # Initialize orbits

    if b.name != "Sun":

        init_orbit(b, sun, 0.3)


physics = Physics(                         # Create physics engine
    bodies,
    relativistic=True
)

print(                                     # Print recursive body count
    "Total bodies:",
    count_bodies_recursive(bodies)
)


# =========================================================
# GUI Setup
# =========================================================

root = tk.Tk()                             # Create main window

root.title(                                # Set window title
    "Relativistic Solar System Simulator"
)

canvas = tk.Canvas(                        # Create drawing canvas
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="black"
)

canvas.pack()                              # Add canvas to window

zoom = 30                                  # Initial zoom scale


# =========================================================
# Mouse Zoom Control
# =========================================================


def on_mousewheel(event):

    global zoom                            # Use global zoom variable

    if event.delta > 0:                    # Zoom in
        zoom *= 1.1

    else:                                  # Zoom out
        zoom /= 1.1

    zoom = max(5, min(zoom, 300))          # Clamp zoom range


canvas.bind("<MouseWheel>", on_mousewheel) # Windows/Mac zoom

canvas.bind(                               # Linux scroll up
    "<Button-4>",
    lambda e: on_mousewheel(type("e", (object,), {"delta":1})())
)

canvas.bind(                               # Linux scroll down
    "<Button-5>",
    lambda e: on_mousewheel(type("e", (object,), {"delta":-1})())
)


# =========================================================
# Coordinate Transform
# =========================================================


def transform(x, y):

    r = math.sqrt(x*x + y*y)               # Distance from origin

    if r < 1e-6:                           # Prevent division by zero
        return WIDTH/2, HEIGHT/2

    log_r = math.log1p(r * 5)              # Logarithmic scaling

    scale = log_r / r                      # Compute scaling factor

    return (                               # Convert to screen coords
        WIDTH/2 + x * scale * zoom,
        HEIGHT/2 + y * scale * zoom
    )


# =========================================================
# Draw Background Grid
# =========================================================


def draw_grid():

    spacing = 40                           # Grid spacing

    for i in range(0, WIDTH, spacing):

        canvas.create_line(                # Draw vertical lines
            i,
            0,
            i,
            HEIGHT,
            fill="#111"
        )

    for j in range(0, HEIGHT, spacing):

        canvas.create_line(                # Draw horizontal lines
            0,
            j,
            WIDTH,
            j,
            fill="#111"
        )


# =========================================================
# Main Animation Loop
# =========================================================


def update():

    canvas.delete("all")                  # Clear previous frame

    draw_grid()                            # Draw spacetime grid

    for _ in range(20):                    # Run multiple physics steps
        physics.step(dt)


    canvas.create_text(                    # Display simulation mode
        160,
        20,
        text="Einstein Relativistic Mode",
        fill="cyan",
        font=("Arial", 14)
    )


    for b in bodies:                       # Process every body

        x, y = transform(                  # Convert world coords
            b.pos[0],
            b.pos[1]
        )

        b.trail.append((x, y))             # Save trail point

        if len(b.trail) > 400:             # Limit trail size
            b.trail.pop(0)


        for i in range(len(b.trail)-1):    # Draw orbit trail

            canvas.create_line(
                *b.trail[i],
                *b.trail[i+1],
                fill=b.color
            )


        r = math.sqrt(                     # Current orbital radius
            b.pos[0]**2 + b.pos[1]**2
        )

        if b.last_r is not None:

            if r > b.last_r and len(b.trail) > 20:

                b.perihelion_points.append((x, y))

        b.last_r = r                       # Save previous radius


        for px, py in b.perihelion_points: # Draw perihelion markers

            canvas.create_oval(
                px-2,
                py-2,
                px+2,
                py+2,
                fill="white"
            )


        canvas.create_oval(                # Draw celestial body
            x - b.radius,
            y - b.radius,
            x + b.radius,
            y + b.radius,
            fill=b.color
        )


        speed = math.sqrt(                 # Compute speed magnitude
            b.vel[0]**2 + b.vel[1]**2
        )


        canvas.create_text(                # Draw planet name
            x,
            y - 12,
            text=b.name,
            fill="white"
        )


        canvas.create_text(                # Draw velocity
            x,
            y + 15,
            text=f"v={speed:.3f}",
            fill="white"
        )


        if b.name != "Sun":               # Skip Sun time dilation

            dilation = math.sqrt(          # Compute time dilation
                max(0, 1 - 2*G*sun.mass/(r*c**2))
            )

            canvas.create_text(            # Display time dilation
                x,
                y + 30,
                text=f"t={dilation:.8f}",
                fill="yellow"
            )


    root.after(16, update)                 # Schedule next frame


# =========================================================
# Start Simulation
# =========================================================

update()                                   # Start animation loop

root.mainloop()                            # Run Tkinter event loop
