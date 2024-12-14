import json
import numpy as np
import matplotlib.pyplot as plt


def read_from_json(path_to_file):
    with open(path_to_file, 'r') as file:
        return json.load(file)


def get_column(column_index, data):
    column = [row[column_index] for row in data]
    return column


def plot():
    # Load the simulation data from JSON
    sim_file_path = "Simulation data files/rocket_trajectory(3D).json"
    Sim_rocket = read_from_json(sim_file_path)
    position = []
    time = []
    velocity = []
    acceleration = []

    apogee_point = 0
    for i, elements in enumerate(Sim_rocket['t']):
        time.append(Sim_rocket['t'][i])
        position.append(Sim_rocket['p'][i])
        velocity.append(Sim_rocket['v'][i])
        acceleration.append(Sim_rocket['a'][i])
        if apogee_point == 0 and Sim_rocket['v'][i][1] - Sim_rocket['v'][i - 1][1] < 0:
            apogee_point = i

    # Create the subplots
    # Create the subplots
    fig, axs = plt.subplots(2, 2, figsize=(20, 9))  # 2 rows, 2 columns

    # First subplot for trajectory (x vs y)
    axs[0, 0].plot(get_column(0, position), get_column(1, position), label='Trajectory', color=(1, 0.5, 0.5))
    axs[0, 0].set_xlabel("Height")
    axs[0, 0].set_ylabel("Range")
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    # Second subplot for position
    axs[0, 1].plot(time, get_column(1, position), label='Position', color='g')
    axs[0, 1].set_xlabel("Time")
    axs[0, 1].set_ylabel("Position")
    axs[0, 1].grid(True)
    axs[0, 1].legend()

    # Third subplot for velocity
    axs[1, 0].plot(time, get_column(1, velocity), label='Velocity', color='b')
    axs[1, 0].set_xlabel("Time")
    axs[1, 0].set_ylabel("Velocity")
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    # Fourth subplot for acceleration
    axs[1, 1].plot(time, get_column(1, acceleration), label='Acceleration', color='r')
    axs[1, 1].set_xlabel("Time")
    axs[1, 1].set_ylabel("Acceleration")
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show the plot
    plt.show()

    # Create the subplots
    # Create the subplots
    fig, axs = plt.subplots(2, 2, figsize=(20, 9))  # 2 rows, 2 columns

    # First subplot for trajectory (x vs y)
    axs[0, 0].plot(get_column(0, position)[:apogee_point], get_column(1, position)[:apogee_point], label='Trajectory', color=(1, 0.5, 0.5))
    axs[0, 0].set_xlabel("Height")
    axs[0, 0].set_ylabel("Range")
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    # Second subplot for position
    axs[0, 1].plot(time[:apogee_point], get_column(1, position)[:apogee_point], label='Position', color='g')
    axs[0, 1].set_xlabel("Time")
    axs[0, 1].set_ylabel("Position")
    axs[0, 1].grid(True)
    axs[0, 1].legend()

    # Third subplot for velocity
    axs[1, 0].plot(time[:apogee_point], get_column(1, velocity)[:apogee_point], label='Velocity', color='b')
    axs[1, 0].set_xlabel("Time")
    axs[1, 0].set_ylabel("Velocity")
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    # Fourth subplot for acceleration
    axs[1, 1].plot(time[:apogee_point], get_column(1, acceleration)[:apogee_point], label='Acceleration', color='r')
    axs[1, 1].set_xlabel("Time")
    axs[1, 1].set_ylabel("Acceleration")
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    # Adjust layout to prevent overlap
    plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    val = 100000
    # Load the simulation data from JSON
    sim_file_path = "../Simulation data files/rocket_trajectory(3D).json"
    Sim_rocket = read_from_json(sim_file_path)
    position = []
    time = []
    velocity = []
    acceleration = []

    apogee_point = 0
    for i, elements in enumerate(Sim_rocket['t']):
        time.append(Sim_rocket['t'][i])
        position.append(Sim_rocket['p'][i])
        velocity.append(Sim_rocket['v'][i])
        acceleration.append(Sim_rocket['a'][i])
        if apogee_point == 0 and Sim_rocket['v'][i][1] - Sim_rocket['v'][i - 1][1] < 0:
            apogee_point = i

    # Create the subplots
    fig, axs = plt.subplots(2, 2, figsize=(20, 9))  # 2 rows, 2 columns

    # First subplot for trajectory (x vs y)
    axs[0, 0].plot(get_column(0, position), get_column(1, position), label='Trajectory', color=(1, 0.5, 0.5))
    axs[0, 0].set_xlabel("Height")
    axs[0, 0].set_ylabel("Range")
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    # Second subplot for position
    axs[0, 1].plot(time, get_column(1, position), label='Position', color='g')
    axs[0, 1].set_xlabel("Time")
    axs[0, 1].set_ylabel("Position")
    axs[0, 1].grid(True)
    axs[0, 1].legend()

    # Third subplot for velocity
    axs[1, 0].plot(time, get_column(1, velocity), label='Velocity', color='b')
    axs[1, 0].set_xlabel("Time")
    axs[1, 0].set_ylabel("Velocity")
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    # Fourth subplot for acceleration
    axs[1, 1].plot(time, get_column(1, acceleration), label='Acceleration', color='r')
    axs[1, 1].set_xlabel("Time")
    axs[1, 1].set_ylabel("Acceleration")
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show the plot
    plt.show()


    # Create the subplots
    # Create the subplots
    fig, axs = plt.subplots(2, 2, figsize=(20, 9))  # 2 rows, 2 columns

    # First subplot for trajectory (x vs y)
    axs[0, 0].plot(get_column(0, position)[:apogee_point], get_column(1, position)[:apogee_point], label='Trajectory', color=(1, 0.5, 0.5))
    axs[0, 0].set_xlabel("Height")
    axs[0, 0].set_ylabel("Range")
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    # Second subplot for position
    axs[0, 1].plot(time[:apogee_point], get_column(1, position)[:apogee_point], label='Position', color='g')
    axs[0, 1].set_xlabel("Time")
    axs[0, 1].set_ylabel("Position")
    axs[0, 1].grid(True)
    axs[0, 1].legend()

    # Third subplot for velocity
    axs[1, 0].plot(time[:apogee_point], get_column(1, velocity)[:apogee_point], label='Velocity', color='b')
    axs[1, 0].set_xlabel("Time")
    axs[1, 0].set_ylabel("Velocity")
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    # Fourth subplot for acceleration
    axs[1, 1].plot(time[:apogee_point], get_column(1, acceleration)[:apogee_point], label='Acceleration', color='r')
    axs[1, 1].set_xlabel("Time")
    axs[1, 1].set_ylabel("Acceleration")
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    # Adjust layout to prevent overlap
    plt.tight_layout()

    plt.show()


