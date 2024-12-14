from simulation_parameters import duration, dt
from Physics_Engine.Rocket3D import initialise
from rocket_parameters import thrust_direction, thrust_duration, max_thrust, rho, rocket_diameter, initial_weight, \
    rocket_drag_coefficient, fuel_burn_rate, no_fuel_mass
from control_compiler import debug
from Renders_plotters.plotter import plot
from Renders_plotters.renderer_pyg import render

code_debugger = False
code_file = "code.txt"

# make the above False and run
if not code_debugger:
    skip_prompt = input("do you want the default settings?(y/n)")
    if skip_prompt == 'n':
        x = 1
        while x:
            sim_para_init = input("do you want to change simulation parameters again?(y/n)")
            y = 1
            if sim_para_init == 'y':
                while y:
                    try:
                        duration = float(input("duration: "))
                    except ValueError or TypeError:
                        print("Invalid Duration")
                        y = not y
                    y = not y
                while not y:
                    try:
                        dt = float(input("time step: "))
                    except ValueError or TypeError:
                        print("Invalid Time step")
                        y = not y
                    y = not y
                x = not x
            elif sim_para_init == 'n':
                x = not x

        print("Max operation", round(.001 / dt, 2), "KHz")
        while not x:
            rocket_para_init = input("do you want to change rocket parameters again?(y/n)")
            y = 1
            if rocket_para_init == 'y':
                while y:
                    try:
                        thrust_duration = float(input("thrust duration: "))
                    except ValueError or TypeError:
                        print("Invalid Duration")
                        y = not y
                    y = not y
                while not y:
                    try:
                        max_thrust = float(input("max thrust: "))
                    except ValueError or TypeError:
                        print("Invalid Thrust")
                        y = not y
                    y = not y
                while y:
                    try:
                        initial_weight = float(input("Full weight: "))
                    except ValueError or TypeError:
                        print("Invalid")
                        y = not y
                    y = not y
                while not y:
                    try:
                        rocket_diameter = float(input("Rocket diameter: "))
                    except ValueError or TypeError:
                        print("Invalid")
                        y = not y
                    y = not y
                while y:
                    try:
                        rocket_drag_coefficient = float(input("Rocket drag coefficient: "))
                    except ValueError or TypeError:
                        print("Invalid")
                        y = not y
                    y = not y
                while not y:
                    try:
                        rho = float(input("Density: "))
                    except ValueError or TypeError:
                        print("Invalid")
                        y = not y
                    y = not y
                while y:
                    try:
                        fuel_burn_rate = float(input("Fuel burn rate: "))
                    except ValueError or TypeError:
                        print("Invalid")
                        y = not y
                    y = not y
                while not y:
                    try:
                        no_fuel_mass = float(input("Dry mass: "))
                    except ValueError or TypeError:
                        print("Invalid")
                        y = not y
                    y = not y
                x = not x
            elif rocket_para_init == 'n':
                x = not x
    x = 1
    while x:
        physics_init = input("do you want to run physics simulation again?(y/n)")
        if physics_init == 'y':
            thrust_init = input("do you want to plot thrust?(y/n)")
            if thrust_init == 'y':
                initialise(thrust_init, duration, dt, initial_weight, thrust_duration, max_thrust, thrust_direction,
                           rho, rocket_drag_coefficient, rocket_diameter, no_fuel_mass, fuel_burn_rate)
            elif thrust_init == 'n':
                initialise(0, duration, dt, initial_weight, thrust_duration, max_thrust, thrust_direction, rho,
                           rocket_drag_coefficient, rocket_diameter, no_fuel_mass, fuel_burn_rate)
            x = not x
        elif physics_init == 'n':
            x = not x

    while not x:
        plot_init = input("do you want to plot the simulation?(y/n)")
        if plot_init == 'y':
            plot()
            x = not x
        elif plot_init == 'n':
            x = not x
    while x:
        render_init = input("do you want to open render window?(y/n)")
        if render_init == 'y':
            render()
            x = not x
        elif render_init == 'n':
            x = not x


debug(code_file)
