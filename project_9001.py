#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 16:55:33 2026
HUADUO LI
Python version: 3.13.9 
| packaged by Anaconda, Inc. 
| (main, Oct 21 2025, 19:11:29) [Clang 20.1.8 ]
Tkinter version: 8.6
9001 final project
@author: lihuaduo
"""

import tkinter as tk            # Import Tkinter for GUI rendering
import math                     # Import math module for calculations

# ---------- Constants ----------
G = 4 * math.pi**2             # Gravitational constant (scaled for astronomical units)
dt = 0.0002                    # Time step for simulation


# ---------- Body Class ----------
class Body:
    def __init__(self, name, mass, pos, color, radius=5, fixed=False):
        self.name = name       # Name of the celestial body (e.g., Sun, Earth)
        self.mass = mass       # Mass of the body
        self.pos = pos[:]      # Position as a list [x, y] (copy to avoid reference issues)
        self.vel = [0, 0]      # Velocity vector [vx, vy], initially zero
        self.color = color     # Display color in GUI
        self.radius = radius   # Radius for drawing on canvas
        self.fixed = fixed     # Whether the body is fixed (e.g., Sun)
        self.trail = []        # Store previous positions for orbit trail


# ---------- File Input ----------
def load_bodies(filename):
    bodies = []                # List to store all body objects
    try:
        with open(filename, "r") as f:     # Open input file
            for line in f:
                parts = line.strip().split()   # Split each line into components

                # basic validation
                if len(parts) < 7:
                    continue   # Skip invalid or incomplete lines

                name = parts[0]               # Body name
                mass = float(parts[1])        # Convert mass to float
                x = float(parts[2])           # X position
                y = float(parts[3])           # Y position
                color = parts[4]              # Display color
                radius = int(parts[5])        # Radius for drawing
                fixed = parts[6] == "True"    # Convert string to boolean

                bodies.append(Body(name, mass, [x, y], color, radius, fixed))  # Create Body object

    except FileNotFoundError:
        print("Error: file not found.")   # Handle missing file
        return []                        # Return empty list

    except ValueError:
        print("Error: invalid data in file.")  # Handle conversion errors
        return []

    return bodies   # Return list of bodies


# ---------- Recursion ----------
def count_bodies_recursive(bodies, index=0):
    if index >= len(bodies):       # Base case: reached end of list
        return 0
    return 1 + count_bodies_recursive(bodies, index + 1)  # Recursive count


# ---------- Orbit Initialization ----------
def init_orbit(body, sun, e):
    dx = body.pos[0] - sun.pos[0]   # X distance from Sun
    dy = body.pos[1] - sun.pos[1]   # Y distance from Sun
    r = math.sqrt(dx**2 + dy**2)    # Radial distance

    a = r / (1 - e)                 # Semi-major axis (from eccentricity)
    v = math.sqrt(G * sun.mass * (2/r - 1/a))  # Orbital velocity (vis-viva equation)

    body.vel[0] = -v * dy / r       # Set perpendicular velocity (x component)
    body.vel[1] = v * dx / r        # Set perpendicular velocity (y component)


# ---------- Physics ----------
class Physics:
    def __init__(self, bodies):
        self.bodies = bodies       # Store all bodies in simulation

    def forces(self):
        F = []                     # List of force vectors

        for i, b1 in enumerate(self.bodies):
            fx, fy = 0, 0          # Initialize net force

            for j, b2 in enumerate(self.bodies):
                if i == j:
                    continue       # Skip self-interaction

                dx = b2.pos[0] - b1.pos[0]   # Distance in x
                dy = b2.pos[1] - b1.pos[1]   # Distance in y
                r = math.sqrt(dx*dx + dy*dy) + 1e-9  # Distance with small epsilon

                f = G * b1.mass * b2.mass / r**2     # Gravitational force magnitude

                fx += f * dx / r    # X component of force
                fy += f * dy / r    # Y component of force

            F.append((fx, fy))      # Store total force for this body

        return F


    def step(self, dt):
        F = self.forces()           # Compute initial forces

        # Compute acceleration for each body
        acc = [(fx/b.mass if not b.fixed else 0,
                fy/b.mass if not b.fixed else 0)
               for b,(fx,fy) in zip(self.bodies,F)]

        # Update positions using Velocity Verlet method
        for i,b in enumerate(self.bodies):
            if b.fixed:
                continue           # Skip fixed bodies

            ax,ay = acc[i]
            b.pos[0] += b.vel[0]*dt + 0.5*ax*dt*dt
            b.pos[1] += b.vel[1]*dt + 0.5*ay*dt*dt

        F2 = self.forces()         # Recalculate forces after position update

        # Update velocities
        for i,b in enumerate(self.bodies):
            if b.fixed:
                continue

            ax1,ay1 = acc[i]
            fx,fy = F2[i]
            ax2,ay2 = fx/b.mass, fy/b.mass

            b.vel[0] += 0.5*(ax1+ax2)*dt
            b.vel[1] += 0.5*(ay1+ay2)*dt


# ---------- Setup ----------
bodies = load_bodies("planet.txt")   # Load data from file

if not bodies:
    raise SystemExit("Simulation stopped due to input error.")  # Exit if load failed

# find sun with break
sun = None
for b in bodies:
    if b.name == "Sun":
        sun = b
        break            # Stop loop once Sun is found

if sun is None:
    raise ValueError("No Sun found in data.")   # Ensure Sun exists

# init orbits
for b in bodies:
    if b.name != "Sun":
        init_orbit(b, sun, 0.3)   # Initialize elliptical orbits

physics = Physics(bodies)   # Create physics engine

# recursion usage
print("Total bodies:", count_bodies_recursive(bodies))  # Print count


# ---------- GUI ----------
root = tk.Tk()   # Create main window
canvas = tk.Canvas(root, width=800, height=800, bg="black")  # Drawing area
canvas.pack()

zoom = 25   # Zoom scaling factor
# ---------- Mouse Zoom ----------
def on_mousewheel(event):
    global zoom

    # Windows / Mac
    if event.delta > 0:
        zoom *= 1.1
    else:
        zoom /= 1.1

    # Limit the scaling range (to prevent the kernel from crashing).
    zoom = max(5, min(zoom, 200))


# Bind scroll wheel events (Windows / Mac)
canvas.bind("<MouseWheel>", on_mousewheel)

# Linux compatibility 
canvas.bind("<Button-4>", lambda e: on_mousewheel(type("e",(object,),{"delta":1})()))
canvas.bind("<Button-5>", lambda e: on_mousewheel(type("e",(object,),{"delta":-1})()))

# ---------- Transform ----------
def transform(x,y):
    r = math.sqrt(x*x+y*y)   # Distance from origin
    if r < 1e-6:
        return 400,400       # Center if too close

    log_r = math.log1p(r*5)  # Log scaling for better visualization
    scale = log_r / r

    return 400 + x*scale*zoom, 400 + y*scale*zoom  # Map to screen coords


# ---------- Update ----------
def update():
    canvas.delete("all")   # Clear previous frame

    for _ in range(5):
        physics.step(dt)   # Advance simulation multiple steps per frame

    for b in bodies:
        x,y = transform(b.pos[0], b.pos[1])  # Convert to screen coords

        b.trail.append((x,y))   # Store trail point
        if len(b.trail) > 200:
            b.trail.pop(0)      # Limit trail length

        # Draw orbit trail
        for i in range(len(b.trail)-1):
            canvas.create_line(*b.trail[i], *b.trail[i+1], fill=b.color)
        speed = math.sqrt(b.vel[0]**2 + b.vel[1]**2)
        canvas.create_text(x, y + 15,text=f"{b.name} speed: {speed:.2f}",#This speed is the speed within the entire simulated coordinate system (usually with the Sun as a reference, but essentially a global coordinate system).Therefore, it represents the speed of a planet's motion in a "cosmic coordinate system".
                       fill="white")

        # Draw body
        canvas.create_oval(x-b.radius, y-b.radius,
                           x+b.radius, y+b.radius,
                           fill=b.color)

        # Draw label
        canvas.create_text(x, y-10, text=b.name, fill="white")# print planet label here

    root.after(16, update)   # Schedule next frame (~60 FPS)


update()        # Start animation loop
root.mainloop() # Run GUI event loop