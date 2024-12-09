import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Define a simple cube
cube_points = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1],
]


edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
]


# Perspective projection
def project(point):
    x, y, z = point
    z += 5  # Move cube into view
    factor = 200 / z
    x = x * factor + WIDTH // 2
    y = -y * factor + HEIGHT // 2
    return int(x), int(y)


# Rotate around Y-axis
def rotate_y(point, angle):
    x, y, z = point
    cos_theta, sin_theta = math.cos(angle), math.sin(angle)
    x_new = cos_theta * x - sin_theta * z
    z_new = sin_theta * x + cos_theta * z
    return [x_new, y, z_new]

running = True
angle = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    # Rotate and project points
    transformed_points = [rotate_y(point, angle) for point in cube_points]
    projected_points = [project(point) for point in transformed_points]

    # Draw edges
    for edge in edges:
        pygame.draw.line(
            screen, (200, 200, 200),
            projected_points[edge[0]], projected_points[edge[1]], 2
        )

    angle += 0.01  # Increment rotation angle
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
