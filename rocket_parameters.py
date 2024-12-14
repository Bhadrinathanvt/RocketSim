import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange  # For loop parallelization

###################################################################################################
# Weight parameters
initial_weight = 4  # Rocket's initial weight(Kg-f)

# Thrust parameters
thrust_duration = 4  # in s
max_thrust = 200  # in N
thrust_return = 40  # in N
thrust_direction = np.array([0, 1, 1], dtype=np.float32)
t1 = 1  # in s
t2 = 2  # in s
t3 = 3  # in s

# Drag Parameters
rocket_drag_coefficient = 0.75
rho = 1.225
rocket_diameter = 0.25  # in m
reference_area = np.pi * ((rocket_diameter/2)**2)
drag_factor = 0.5*rocket_drag_coefficient*rho*reference_area

# Fuel parameters
no_fuel_mass = 0.062/9.81
fuel_burn_rate = (initial_weight-no_fuel_mass) / (thrust_duration*9.81)  # Fuel burn rate (kg/s)

# Impulse
r1 = t1 / thrust_duration
r2 = t2 / thrust_duration
r3 = t3 / thrust_duration
thrust_return_fact = thrust_return / max_thrust
impulse = 0.5*max_thrust * thrust_duration * (thrust_return_fact*r1 + r2*(1-3*thrust_return_fact)+thrust_return_fact*r3+thrust_return_fact)

@njit
def thrust_function(time):
    thrust_return_factor = thrust_return / max_thrust
    global t1, t2, t3
    r1 = t1/thrust_duration
    r2 = t2/thrust_duration
    r3 = t3/thrust_duration
    if time <= r1 * thrust_duration:
        return max_thrust * (time / thrust_duration) * (1/r1)
    elif r1 * thrust_duration < time <= r2 * thrust_duration:
        return max_thrust * (1 - (time / thrust_duration - r1) * (1/(r2-r1)) * (1 - thrust_return_factor))
    elif r2 * thrust_duration < time <= r3 * thrust_duration:
        return max_thrust * thrust_return_factor
    elif r3 * thrust_duration <= time < thrust_duration:
        return max_thrust * thrust_return_factor * (1 - (time / thrust_duration - r3) * (1/(1-r3)))
    return 0.0  # No thrust after 10 seconds


def drag_function(velocity):
    vel = np.linalg.norm(velocity)  # Ensure velocity is within bounds
    return drag_factor * (vel ** 2)
###################################################################################################


def plot_thrust():
    # Generate time values for plotting
    time = np.linspace(0, thrust_duration, 1000)  # 1000 points between 0 and thrust_duration

    # Evaluate thrust function for each time value
    thrust_values = [thrust_function(t) for t in time]

    # Plot the function
    plt.figure(figsize=(10, 6))
    plt.plot(time, thrust_values, label="Thrust vs Time", color="blue")

    # Add labels, title, and legend
    plt.xlabel("Time (s)")
    plt.ylabel("Thrust (N)")
    plt.title("Thrust Function Over Time")
    plt.legend()
    plt.grid(True)

    # Display the plot
    plt.show()


def print_parameters(thrust_plot=False):
    avg_thrust = impulse / thrust_duration
    print("____________________________________________")
    print("| Full Weight(kg-f)            |", round(initial_weight + 0.00, 3), '      |')
    print("| Dry weight(kg-f)             |", round(no_fuel_mass * 9.81 + 0.00, 3), '     |')
    print("| Propellant weight(kg-f)      |", round(initial_weight - no_fuel_mass * 9.81 + 0.00, 3), '     |')
    print("| Max thrust(N)                |", round(max_thrust + 0.00, 3), '    |')
    print("| Thrust duration(s)           |", round(thrust_duration + 0.00, 3), '      |')
    print("| Fuel burn rate(kg/s)         |", round(fuel_burn_rate + 0.00, 3), '   |')
    print("| Drag factor(Drag/v^2)        |", round(drag_factor, 5), '  |')
    print("____________________________________________")
    print("| Impulse(N-s)                 |", round(impulse, 3), '    |')
    print("| Average thrust(N)            |", round(avg_thrust + 0.00, 3), '     |')
    print("____________________________________________")

    if thrust_plot:
        plot_thrust()

if __name__ == "__main__":
    print_parameters(False)
    # Time range for plotting
    time_values = np.linspace(0, thrust_duration, 10000)
