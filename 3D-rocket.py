import json
import matplotlib.pyplot as plt
import numpy as np


def simulate_rocket(duration, dt, initial_mass, fuel_burn_rate, thrust_function,  drag_function, thrust_direction=np.array([0, 1, 0]), gravity=9.81):
    time = 0
    position = np.array([0, 0, 0])
    velocity = np.array([0, 0, 0])
    acceleration = np.array([0, 0, 0])
    idx = 0
    results = [{
        "time": 0,
        "mass": initial_mass,
        "position": (position + position_bias).tolist(),
        "velocity": velocity.tolist(),
        "acceleration": acceleration.tolist()
    }]
    max_pos = 0
    while time <= duration:
        # Calculate thrust, drag, and net force
        mass = results[idx]["mass"]
        thrust = thrust_function(time)
        thrust = thrust * normalise(thrust_direction)
        drag = drag_function(velocity)
        drag = -1 * drag * normalise(velocity)
        weight = mass * gravity * np.array([0, -1, 0])
        net_force = thrust + drag + weight

        # Acceleration (Newton's second law)
        acceleration = net_force / mass
        if position[1] <= 0 and acceleration[1] < 0:
            acceleration = np.zeros(3)
            velocity = np.zeros(3)
            position = np.zeros(3)
        # Update velocity and position using kinematics
        velocity += acceleration * dt
        position += velocity * dt
        if position[1] > max_pos:
            max_pos = position[1]
        # Update mass (reduce fuel)
        fuel_mass_loss = fuel_burn_rate * dt
        idx += 1
        mass = max(mass - fuel_mass_loss, no_fuel_mass)  # Mass can't go below 0

        # Record data for this timestep
        results.append({
            "time": time,
            "mass": mass,
            "position": (position + position_bias).tolist(),
            "velocity": velocity.tolist(),
            "acceleration": acceleration.tolist()
        })

        # Update time
        time += dt

    return results, max_pos


def thrust_function(t):
    thrust_return_factor = thrust_return / max_thrust
    if t <= 0.3 * thrust_duration:
        return max_thrust * (t / thrust_duration) * 10 / 3
    elif 0.3 * thrust_duration < t <= 0.5 * thrust_duration:
        return max_thrust * (1 - (t / thrust_duration - 0.3) * 5 * (1 - thrust_return_factor))
    elif 0.5 * thrust_duration < t <= 0.9 * thrust_duration:
        return max_thrust * thrust_return_factor
    elif 0.9 * thrust_duration <= t < thrust_duration:
        return max_thrust * thrust_return_factor * (1 - (t / thrust_duration - 0.9) * 10)
    return 0  # No thrust after 10 seconds


# Example drag function (quadratic drag model)
def drag_function(velocity):
    vel = np.linalg.norm(velocity)  # Ensure velocity is within bounds
    return drag_factor * (vel ** 2)


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
    impulse = max_thrust * thrust_duration * (0.25 + 0.55 * (thrust_return / max_thrust))
    avg_thrust = impulse / thrust_duration
    print("____________________________________________")
    print("| Full Weight(kg-f)            |", round(initial_mass * 9.81 + 0.00, 3), '      |')
    print("| Dry weight(kg-f)             |", round(no_fuel_mass * 9.81 + 0.00, 3), '     |')
    print("| Propellant weight(kg-f)      |", round((initial_mass - no_fuel_mass) * 9.81 + 0.00, 3), '     |')
    print("| Max thrust(N)                |", round(max_thrust + 0.00, 3), '    |')
    print("| Thrust duration(s)           |", round(thrust_duration + 0.00, 3), '      |')
    print("| Fuel burn rate(kg/s)         |", round(fuel_burn_rate + 0.00, 3), '    |')
    print("| Drag factor(Drag/v^2)        |", drag_factor, '   |')
    print("____________________________________________")
    print("| Impulse(N-s)                 |", round(impulse, 3), '    |')
    print("| Average thrust(N)            |", round(avg_thrust + 0.00, 3), '     |')
    print("| Max altitude(m)              |", round(max_altitude, 3), '   |')
    print("| Max altitude(ft)             |", round(max_altitude * 3.28084, 3), ' |')
    print("____________________________________________")

    if thrust_plot:
        plot_thrust()


def store_in_json(file_path):
    # Writing to the JSON file
    with open(file_path, "w") as json_file:
        json.dump(simulation_results, json_file, indent=4)

    print(f"Data successfully written to {file_path}")


def normalise(v):
    magnitude = np.linalg.norm(v)
    if magnitude == 0:
        return np.zeros(3)
    normalized_vector = v / magnitude
    return normalized_vector

# Simulation parameters
duration = 25
dt = 0.0002  # Time step
position_bias = np.array([0, 0.5, 0])

# Rocket parameters
initial_mass = 4 / 9.81  # Rocket's initial mass (kg)

# Thrust parameters
thrust_duration = 4
max_thrust = 200
thrust_return = 80
thrust_direction = np.array([0, 1, 0])

# Drag Parameters
drag_factor = 0.0036

# Fuel parameters
no_fuel_mass = 0.09 * initial_mass
fuel_burn_rate = 0.91 * initial_mass / thrust_duration  # Fuel burn rate (kg/s)

# Run the simulation
simulation_results, max_altitude = simulate_rocket(duration, dt, initial_mass, fuel_burn_rate, thrust_function,
                                                   drag_function, thrust_direction)
# print_parameters(True)
print_parameters(False)
file_path = "rocket_trajectory(3D).json"
store_in_json(file_path)

