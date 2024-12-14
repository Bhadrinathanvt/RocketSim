digit_precision = 4
duration = 50  # time in seconds(s)
dt = 2*(10**(-digit_precision))  # time step in seconds(s)
if __name__ == "__main__":
    print("Max operation", round(.001/dt, 2), "KHz")
