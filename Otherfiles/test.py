import numpy as np


def angles_with_axes(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return 0, 0, 0  # Avoid division by zero
    unit_vector = vector / norm
    angle_x = np.arccos(unit_vector[0]) * (180 / np.pi)
    angle_y = np.arccos(unit_vector[1]) * (180 / np.pi)
    angle_z = np.arccos(unit_vector[2]) * (180 / np.pi)
    return angle_x, angle_y, angle_z


# Rotate the rocket to align with velocity
def rotate(vertices, direction):
    if np.linalg.norm(direction) == 0:
        return vertices

    # Convert velocity to rotation angles
    rX, rY, rZ = angles_with_axes(direction)

    # Precompute cosines and sines of angles
    cosX, sinX = np.cos(rX), np.sin(rX)
    cosY, sinY = np.cos(rY), np.sin(rY)
    cosZ, sinZ = np.cos(rZ), np.sin(rZ)

    # Define rotation matrices
    rotX = np.array([[1, 0, 0], [0, cosX, -sinX], [0, sinX, cosX]])
    rotY = np.array([[cosY, 0, sinY], [0, 1, 0], [-sinY, 0, cosY]])
    rotZ = np.array([[cosZ, -sinZ, 0], [sinZ, cosZ, 0], [0, 0, 1]])

    # Combined rotation matrix
    rotation_matrix = rotZ @ rotY @ rotX

    # Rotate vertices
    return np.dot(vertices, rotation_matrix.T)

print(angles_with_axes([1, 1, 1]))
print(rotate([[1, 0, 0], [1, 1, 1], [0, 0, 0]], [1, 1, 1]))
