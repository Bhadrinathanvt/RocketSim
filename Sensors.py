
pos_initial = [0, 0, 0]
acceleration = [0, 10, 0]


def get_real_pos(time):
    pos = pos_initial+(1/2)*acceleration*(time**2)
    return pos


def sensor_data(error, time):
    real_pos = get_real_pos(time)
    data = real_pos+error
    return data
print(sensor_data((0.1, 0.1, -0.1), 20))