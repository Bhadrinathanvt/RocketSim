import json
import numpy as np
import rocket_parameters as rkt
import simulation_parameters as sim
import time as top
from hardware import MCUs, Sensors


def simulate_rocket(duration, dt, initial_mass, fuel_burn_rate, no_fuel_mass, thrust_duration, thrust_function,
                    drag_function, drag_factor,
                    thrust_direction=np.array([0, 1, 0]), gravity=9.81):
    time = 0
    position = np.array([0, 0, 0], dtype=np.float32)
    velocity = np.array([0, 0, 0], dtype=np.float32)
    acceleration = np.array([0, 0, 0], dtype=np.float32)
    idx = 0
    results = {
        "t": [0],
        "m": [initial_mass],
        "p": [position.tolist()],
        "v": [velocity.tolist()],
        "a": [acceleration.tolist()]
    }
    max_pos, max_vel, max_acc = 0, 0, 0
    print("Physics engine booted...")
    frame = 0
    gravity_vector = gravity * np.array([0, -1, 0])
    while time <= duration:
        # Calculate thrust, drag, and net force
        mass = results["m"][idx]
        thrust = thrust_function(time)
        normalised_velocity = normalise(velocity)
        thrust_direction_normalized = normalise(thrust_direction)
        drag = -drag_factor * np.linalg.norm(velocity) ** 2 * normalised_velocity
        net_force = thrust * thrust_direction_normalized + drag + gravity_vector * mass

        # Acceleration (Newton's second law)
        acceleration = net_force / mass
        if position[1] <= 0 and acceleration[1] < 0:
            acceleration.fill(0)
            velocity.fill(0)
            position.fill(0)
        # Update velocity and position using kinematics
        np.add(velocity, acceleration * dt, out=velocity)
        np.add(position, velocity * dt, out=position)
        max_pos = max(max_pos, position[1])
        max_vel = max(max_vel, velocity[1])
        max_acc = max(max_acc, acceleration[1])

        # Update mass (reduce fuel)
        fuel_mass_loss = fuel_burn_rate * dt
        idx += 1
        mass = max(mass - fuel_mass_loss, no_fuel_mass)
        frame = frame + 1

        # Record data for this timestep
        results['t'].append(round(time, sim.digit_precision))
        results['m'].append(round(mass, sim.digit_precision))
        results['p'].append(np.round(position, sim.digit_precision).tolist())
        results['v'].append(np.round(velocity, sim.digit_precision).tolist())
        results['a'].append(np.round(acceleration, sim.digit_precision).tolist())

        # Update time
        time += dt
        flight_duration = time - dt
        if time > thrust_duration and position[1] == 0.0:
            time = duration + dt

    return results, max_pos, max_vel, max_acc, flight_duration


def store_in_json(obj, file_path):
    # Writing to the JSON file
    with open(file_path, "w") as json_file:
        json.dump(obj, json_file, indent=4)

    print(f"Data successfully written to {file_path}")


def normalise(v):
    magnitude = np.linalg.norm(v)
    if magnitude == 0:
        return np.zeros(3)
    normalized_vector = v / magnitude
    return normalized_vector


# Thrust parameters
thrust_return = rkt.thrust_return


# Fuel parameters


def initialise(thrust_init=0, duration=sim.duration, dt=sim.dt, initial_weight=rkt.initial_weight,
               thrust_duration=rkt.thrust_duration, max_thrust=rkt.max_thrust, thrust_direction=rkt.thrust_direction,
               no_fuel_mass=rkt.no_fuel_mass, fuel_burn_rate=rkt.fuel_burn_rate, rho=rkt.rho,
               rocket_drag_coefficient=rkt.rocket_drag_coefficient, rocket_diameter=rkt.rocket_diameter):
    initial_mass = initial_weight / 9.81  # Rocket's initial mass (kg)
    reference_area = np.pi * ((rocket_diameter / 2) ** 2)
    drag_factor = 0.5 * rocket_drag_coefficient * rho * reference_area
    # Run the simulation
    print("Starting simulation...")
    start_time = top.time()
    simulation_results, max_altitude, max_velocity, max_acceleration, flight_time = simulate_rocket(duration, dt,
                                                                                                    initial_mass,
                                                                                                    fuel_burn_rate,
                                                                                                    no_fuel_mass,
                                                                                                    thrust_duration,
                                                                                                    rkt.thrust_function,
                                                                                                    rkt.drag_function,
                                                                                                    drag_factor,
                                                                                                    rkt.thrust_direction,
                                                                                                    9.81)
    print("Physics Simulation is over...")
    end_time = top.time()
    time_elapsed = end_time - start_time
    print('time elapsed: ' + str(time_elapsed))

    print("Printing Parameters")
    impulse = rkt.impulse
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
    print("| Max velocity(m/s)            |", round(max_velocity, 3), '   |')
    print("| Max acceleration(m/s-2)      |", round(max_acceleration, 3), '   |')
    print("| Air time(s)                  |", round(flight_time, 3), '   |')
    print("____________________________________________")

    if thrust_init:
        rkt.plot_thrust()
    if __name__ =='__main__':
        start_time = top.time()
        print("Saving the simulation data into JSON file...")
        file_path = "../Simulation data files/rocket_trajectory(3D).json"
        store_in_json(simulation_results, file_path)
        end_time = top.time()
        time_elapsed = end_time - start_time
        print('time elapsed for saving to JSON file: ' + str(time_elapsed))
    else:
        start_time = top.time()
        print("Saving the simulation data into JSON file...")
        file_path = "Simulation data files/rocket_trajectory(3D).json"
        store_in_json(simulation_results, file_path)
        end_time = top.time()
        time_elapsed = end_time - start_time
        print('time elapsed for saving to JSON file: ' + str(time_elapsed))


if __name__ == '__main__':
    initialise()
