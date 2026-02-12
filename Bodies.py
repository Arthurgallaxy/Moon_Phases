import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Define the moon phases and their visual characteristics
phases = [
    {"name": "New Moon", "color": "black", "visibility": 0.0, "shape": "circle"}, 
    {"name": "Waxing Crescent", "color": "gray", "visibility": 0.2, "shape": "crescent"}, 
    {"name": "First Quarter", "color": "gray", "visibility": 0.5, "shape": "half"}, 
    {"name": "Waxing Gibbous", "color": "gray", "visibility": 0.7, "shape": "gibbous"}, 
    {"name": "Full Moon", "color": "white", "visibility": 1.0, "shape": "circle"},
    {"name": "Waning Gibbous", "color": "gray", "visibility": 0.7, "shape": "gibbous"}, 
    {"name": "Last Quarter", "color": "gray", "visibility": 0.5, "shape": "half"}, 
    {"name": "Waning Crescent", "color": "gray", "visibility": 0.2, "shape": "crescent"}
]

# Function to get the moon phase based on the day
def get_moon_phase(day):
    phase_index = int((day % 29.5) / (29.5 / 8))  # Divide the cycle into 8 phases
    return phases[phase_index]

# Function to plot the moon phase based on the day
def plot_moon_phase(day, ax):
    # Clear the axis for a new plot
    ax.cla()

    # Create the Earth (blue circle at the center)
    earth = plt.Circle((0, 0), 0.1, color='blue', label="Earth")
    ax.add_artist(earth)

    # Create a little person on Earth (a simple circle for the head)
    person_x = 0.1
    person_y = -0.12
    person = plt.Circle((person_x, person_y), 0.02, color='black', label="Observer")
    ax.add_artist(person)
    
    # Draw the orbit (dashed circle)
    orbit = plt.Circle((0, 0), 0.8, edgecolor='gray', facecolor='none', linestyle='--')
    ax.add_artist(orbit)

    # Calculate the moon's position
    angle = (day % 29.5) / 29.5 * 2 * np.pi  # Moon's position in the orbit
    moon_x = 0.8 * np.cos(angle)
    moon_y = 0.8 * np.sin(angle)
    
    # Get the moon's phase and appearance
    phase = get_moon_phase(day)
    
    # Plot the moon (gray circle) with varying shapes
    if phase["shape"] == "circle":
        moon = plt.Circle((moon_x, moon_y), 0.05, color=phase["color"], alpha=phase["visibility"], label=phase["name"])
        ax.add_artist(moon)
    elif phase["shape"] == "crescent":
        # Simulate a crescent moon by overlapping a circle with a darker "mask"
        moon = plt.Circle((moon_x, moon_y), 0.05, color=phase["color"], alpha=phase["visibility"], label=phase["name"])
        mask = plt.Circle((moon_x - 0.03, moon_y), 0.05, color='black', alpha=0.7)
        ax.add_artist(moon)
        ax.add_artist(mask)
    elif phase["shape"] == "half":
        # Simulate a half moon by drawing half of the circle
        wedge = plt.Wedge((moon_x, moon_y), 0.05, 90, 270, color=phase["color"], alpha=phase["visibility"])
        ax.add_artist(wedge)
    elif phase["shape"] == "gibbous":
        # Simulate a gibbous moon by showing most of the circle with a slight crescent
        moon = plt.Circle((moon_x, moon_y), 0.05, color=phase["color"], alpha=phase["visibility"], label=phase["name"])
        mask = plt.Circle((moon_x + 0.025, moon_y), 0.05, color='black', alpha=0.3)
        ax.add_artist(moon)
        ax.add_artist(mask)

    # Set the title with the phase of the moon
    ax.set_title(f"Moon Phase on Day {day}: {phase['name']}")

    # Set the aspect and limits
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')

    # Remove axis labels
    ax.axis('off')

# Update function for the slider
def update(val, canvas, ax):
    day = slider.get()  # Get the value of the slider
    plot_moon_phase(day, ax)  # Update the moon phase plot
    canvas.draw()  # Redraw the canvas with updated plot

# Set up the tkinter root window
root = tk.Tk()
root.title("Moon Phases Simulation")

# Create a frame to hold the matplotlib canvas and slider
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Create a matplotlib figure and axis
fig, ax = plt.subplots(figsize=(6, 6))

# Create a canvas to display the plot inside the tkinter window
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack()

# Set up the slider
slider = tk.Scale(root, from_=0, to=29.5, resolution=0.1, orient="horizontal", label="Day", length=500)
slider.set(0)  # Set initial value of slider to 0
slider.pack(pady=10)

# Register the update function with the slider
slider.bind("<Motion>", lambda event: update(slider.get(), canvas, ax))

# Initial plot
plot_moon_phase(0, ax)
canvas.draw()

# Start the tkinter event loop
root.mainloop()

