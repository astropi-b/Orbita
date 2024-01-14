import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

# Constants
G = 6.67430e-11  # Gravitational constant
M_sun = 1.989e30  # Mass of the sun in kg
AU = 1.496e11  # Astronomical unit in meters

# Function to solve Kepler's equation
def solve_kepler(M, e, tol=1e-6):
    E = M  # Initial guess
    while True:
        delta = E - e * np.sin(E) - M
        if abs(delta) < tol:
            break
        E -= delta / (1 - e * np.cos(E))
    return E

# Function to be called when the 'Calculate' button is pressed
def on_calculate():
    # Get inputs from the GUI
    M_star = float(mass_entry.get()) * M_sun
    a = float(axis_entry.get()) * AU
    e = float(eccentricity_entry.get())
    num_steps = int(time_steps_entry.get())

    # Update plot limits based on semimajor axis
    max_plot_limit = a * (1 + e) * 1.2  # 20% padding for the aphelion point

    # Update plot limits
    ax.set_xlim(-max_plot_limit, max_plot_limit)
    ax.set_ylim(-max_plot_limit, max_plot_limit)
    # Prepare data for the orbit path
    orbit_path_x = []
    orbit_path_y = []


    # Animation update function
    def update(step):
        M = 2 * np.pi * step / num_steps
        E = solve_kepler(M, e)
        x = a * (np.cos(E) - e)
        y = a * np.sqrt(1 - e**2) * np.sin(E)
        planet.set_data(x, y)

        # Update orbit path
        orbit_path_x.append(x)
        orbit_path_y.append(y)
        orbit.set_data(orbit_path_x, orbit_path_y)

        return planet, orbit

    # Creating the animation with a faster interval
    ani = FuncAnimation(fig, update, frames=num_steps, blit=True, interval=20, repeat=False)
    canvas.draw()

# Creating the main window
window = tk.Tk()
window.title("Agastya's Orbit Simulator")

# Adding widgets for user inputs
ttk.Label(window, text="Mass of Star (solar masses):").grid(column=0, row=0, sticky='W')
mass_entry = ttk.Entry(window)
mass_entry.grid(column=1, row=0)

ttk.Label(window, text="Semimajor Axis (AU):").grid(column=0, row=1, sticky='W')
axis_entry = ttk.Entry(window)
axis_entry.grid(column=1, row=1)

ttk.Label(window, text="Eccentricity:").grid(column=0, row=2, sticky='W')
eccentricity_entry = ttk.Entry(window)
eccentricity_entry.grid(column=1, row=2)

ttk.Label(window, text="Number of Time Steps:").grid(column=0, row=3, sticky='W')
time_steps_entry = ttk.Entry(window)
time_steps_entry.grid(column=1, row=3)

# Calculate button
calculate_button = ttk.Button(window, text="Calculate", command=on_calculate)
calculate_button.grid(column=1, row=4)

# Matplotlib plot setup
# Matplotlib plot setup
fig, ax = plt.subplots()
planet, = ax.plot([], [], 'ro')  # Planet marker
orbit, = ax.plot([], [], 'b-', linewidth=1, alpha=0.5)  # Orbit path
ax.scatter([0], [0], color='orange', label='Star')  # Star position

ax.set_xlabel('Distance (A.u)')
ax.set_ylabel('Distance (A.u)')
ax.set_title('Planetary Orbit')

#Embed the plot into the Tkinter window

canvas = FigureCanvasTkAgg(fig, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(column=0, row=5, columnspan=2)

#Start the GUI event loop

window.mainloop()
