import pygame as pg
import numpy as np
from numba import njit
import json

SCREEN_W, SCREEN_H = 800, 600
FOV_V = np.pi / 4  # 45 degrees vertical fov
FOV_H = FOV_V * SCREEN_W / SCREEN_H


def main(sim_rocket, rocket_model):
    pg.init()
    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    running = True
    clock = pg.time.Clock()
    # edited
    surf = pg.Surface((SCREEN_W, SCREEN_H - 100))  # Main rendering area
    dashboard = pg.Surface((SCREEN_W, 100))  # Dashboard at the bottom
    # edited

    points, triangles = read_obj(rocket_model)
    rotate_model(points, [0, 1, 0])
    color_scale = 230 / np.max(np.abs(points))

    camera = np.asarray([3.19788002e+02, 5.00000000e-01, 2.81602353e+02, 3.87887500e+00, 0])
    camera = np.asarray([72.25923125, 0.5, 67.88797055, 3.878875, 0])

    z_order = np.zeros(len(triangles))
    shade = z_order.copy()

    # added
    pg.font.init()
    font = pg.font.Font(None, 20)
    TEXT_COLOR = (255, 255, 255)
    DASHBOARD_BG = (100, 100, 100)

    init = 1
    current_forward = np.array([0, 1, 0])

    translation = np.array(sim_rocket['p'])
    direction = np.array(sim_rocket['v'])
    time_point = sim_rocket['t']

    frame = 0
    max_frame = len(translation)
    frame_increment = 200
    sim_status = 'going'


    MAX_HEIGHT = 10
    # /added

    while running:
        # pg.mouse.set_pos(SCREEN_W / 2, SCREEN_H / 2)
        surf.fill([50, 127, 200])
        elapsed_time = clock.tick() * 0.001
        light_dir = np.asarray([np.sin(pg.time.get_ticks() / 1000), 1, 1])
        light_dir = light_dir / np.linalg.norm(light_dir)

        draw_xyz_axis(surf, camera, axis_length=100)

        for event in pg.event.get():
            if event.type == pg.QUIT: running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE: running = False

        # added
        surf.fill([50, 127, 200])
        dashboard.fill(DASHBOARD_BG)

        # Axis Parameters
        AXIS_COLOR = (255, 255, 255)  # White
        AXIS_X_POS = 50  # X position of the axis
        AXIS_Y_START = 50  # Start Y position
        AXIS_Y_END = SCREEN_H - 150  # End Y position
        NUM_TICKS = 10  # Number of ticks on the axis
        MAX_HEIGHT = max(translation[frame][1], 1000)   # Update with the maximum height in the current frame

        # Draw vertical axis
        pg.draw.line(surf, AXIS_COLOR, (AXIS_X_POS, AXIS_Y_START), (AXIS_X_POS, AXIS_Y_END), 2)


        # Draw ticks and labels
        for i in range(NUM_TICKS + 1):
            # Calculate tick position and height value
            tick_y = AXIS_Y_START + i * (AXIS_Y_END - AXIS_Y_START) / NUM_TICKS
            height_value = MAX_HEIGHT - i * (MAX_HEIGHT / NUM_TICKS)

            # Draw horizontal tick line
            pg.draw.line(surf, AXIS_COLOR, (AXIS_X_POS - 5, tick_y), (AXIS_X_POS + 5, tick_y), 2)

            # Render height label
            height_label = font.render(f"{int(height_value)}", True, AXIS_COLOR)
            surf.blit(height_label, (AXIS_X_POS - 40, tick_y - height_label.get_height() / 2))

        if init == 1:
            print('once')
            init = 0

        target_direction = normalise(direction[frame])
        target_direction[1] = -target_direction[1]
        if not target_direction.any():
            target_direction[1] = -1
        rotate_to_direct(points, current_forward, target_direction)
        current_forward = target_direction
        # /added

        project_points(points, camera)
        sort_triangles(points, triangles, camera, light_dir, z_order, shade)

        for index in np.argsort(z_order):
            if z_order[index] == 9999: break
            triangle = [points[triangles[index][0]][3:], points[triangles[index][1]][3:],
                        points[triangles[index][2]][3:]]
            color = shade[index] * np.abs(points[triangles[index][0]][:3]) * color_scale + 25
            pg.draw.polygon(surf, color, triangle)

        if sim_status == 'going':
            # added
            # Dashboard: Display information
            fps_text = font.render(f"FPS: {round(1 / (elapsed_time + 1e-16), 1)}", True, TEXT_COLOR)
            time_text = font.render(f"Time: {round(time_point[frame], 2)} s", True, TEXT_COLOR)
            position_text = font.render(f"Position: {np.round(translation[frame],2)}", True, TEXT_COLOR)
            dashboard.blit(fps_text, (10, 10))
            dashboard.blit(time_text, (10, 40))
            dashboard.blit(position_text, (10, 70))
            # /added

        # added
        # time_text = font.render(f"Time: {round(time_point[frame], 2)} s", True, TEXT_COLOR)
        # screen.blit(time_text, (10, 25))
        if frame + frame_increment < max_frame:
            frame += frame_increment
        else:
            text = font.render("Simulation Complete", True, TEXT_COLOR)
            dashboard.blit(text, (10, 10))
            sim_status = 'complete'
        # /added

        # Blit the main rendering surface
        screen.blit(surf, (0, 0))

        # Blit the dashboard at the bottom of the screen
        screen.blit(dashboard, (0, SCREEN_H - 100))


        # Update the display
        pg.display.update()

        # Set the window caption
        pg.display.set_caption(str(round(1 / (elapsed_time + 1e-16), 1)) + ' ' + str(camera))

        # Handle camera movement
        movement(camera, elapsed_time * 10)




def movement(camera, elapsed_time):
    # if pg.mouse.get_focused():
    #     p_mouse = pg.mouse.get_pos()
    #     camera[3] = (camera[3] + 10 * elapsed_time * np.clip((p_mouse[0] - SCREEN_W / 2) / SCREEN_W, -0.2, .2)) % (
    #             2 * np.pi)
    #     camera[4] = camera[4] + 10 * elapsed_time * np.clip((p_mouse[1] - SCREEN_H / 2) / SCREEN_H, -0.2, .2)
    #     camera[4] = np.clip(camera[4], -.3, .3)

    pressed_keys = pg.key.get_pressed()

    if pressed_keys[ord('e')]:
        camera[1] += elapsed_time
    elif pressed_keys[ord('q')]:
        camera[1] -= elapsed_time

    if (pressed_keys[ord('w')] or pressed_keys[ord('s')]) and (pressed_keys[ord('a')] or pressed_keys[ord('d')]):
        elapsed_time *= 0.707  # keep speed for diagonals

    if pressed_keys[pg.K_UP] or pressed_keys[ord('w')]:
        camera[0] += elapsed_time * np.cos(camera[3])
        camera[2] += elapsed_time * np.sin(camera[3])

    elif pressed_keys[pg.K_DOWN] or pressed_keys[ord('s')]:
        camera[0] -= elapsed_time * np.cos(camera[3])
        camera[2] -= elapsed_time * np.sin(camera[3])

    if pressed_keys[pg.K_LEFT] or pressed_keys[ord('a')]:
        camera[0] += elapsed_time * np.sin(camera[3])
        camera[2] -= elapsed_time * np.cos(camera[3])

    elif pressed_keys[pg.K_RIGHT] or pressed_keys[ord('d')]:
        camera[0] -= elapsed_time * np.sin(camera[3])
        camera[2] += elapsed_time * np.cos(camera[3])


@njit()  # TODO: better vertical projection
def project_points(points, camera):
    for point in points:
        # Calculate xy angle of vector from camera point to projection point
        h_angle_camera_point = np.arctan((point[2] - camera[2]) / (point[0] - camera[0] + 1e-16))

        # Check if it isn't pointing backwards
        if abs(camera[0] + np.cos(h_angle_camera_point) - point[0]) > abs(camera[0] - point[0]):
            h_angle_camera_point = (h_angle_camera_point - np.pi) % (2 * np.pi)

        # Calculate difference between camera angle and pointing angle
        h_angle = (h_angle_camera_point - camera[3]) % (2 * np.pi)

        # Bring to -pi to pi range
        if h_angle > np.pi: h_angle = h_angle - 2 * np.pi

        # Calculate the point horizontal screen coordinate
        point[3] = SCREEN_W * h_angle / FOV_H + SCREEN_W / 2

        # Calculate xy distance from camera point to projection point
        distance = np.sqrt((point[0] - camera[0]) ** 2 + (point[1] - camera[1]) ** 2 + (point[2] - camera[2]) ** 2)

        # Calculate angle to xy plane
        v_angle_camera_point = np.arcsin((camera[1] - point[1]) / distance)

        # Calculate difference between camera verticam angle and pointing vertical angle
        v_angle = (v_angle_camera_point - camera[4]) % (2 * np.pi)
        if v_angle > np.pi: v_angle = v_angle - 2 * np.pi

        # Bring to -pi to pi range
        if v_angle > np.pi: v_angle = v_angle - 2 * np.pi

        # Calculate the point vertical screen coordinate
        point[4] = SCREEN_H * v_angle / FOV_V + SCREEN_H / 2


@njit()
def dot_3d(arr1, arr2):
    return arr1[0] * arr2[0] + arr1[1] * arr2[1] + arr1[2] * arr2[2]


@njit()
def sort_triangles(points, triangles, camera, light_dir, z_order, shade):
    for i in range(len(triangles)):
        triangle = triangles[i]

        # Use Cross-Product to get surface normal
        vet1 = points[triangle[1]][:3] - points[triangle[0]][:3]
        vet2 = points[triangle[2]][:3] - points[triangle[0]][:3]

        # backface culling with dot product between normal and camera ray
        normal = np.cross(vet1, vet2)
        normal = normal / np.sqrt(normal[0] * normal[0] + normal[1] * normal[1] + normal[2] * normal[2])

        CameraRay = points[triangle[0]][:3] - camera[:3]
        dist2cam = np.sqrt(CameraRay[0] * CameraRay[0] + CameraRay[1] * CameraRay[1] + CameraRay[2] * CameraRay[2])
        CameraRay = CameraRay / dist2cam

        # get projected 2d points for filtering of offscreen triangles
        xxs = np.asarray([points[triangle[0]][3:5][0], points[triangle[1]][3:5][0], points[triangle[2]][3:5][0]])
        yys = np.asarray([points[triangle[0]][3:5][1], points[triangle[1]][3:5][1], points[triangle[2]][3:5][1]])

        # check valid values
        if (dot_3d(normal, CameraRay) < 0 and np.min(xxs) > - SCREEN_W and np.max(xxs) < 2 * SCREEN_W
                and np.min(yys) > - SCREEN_H and np.max(yys) < 2 * SCREEN_H):

            z_order[i] = -dist2cam

            # calculate shading, normalize, dot and to 0 - 1 range
            shade[i] = 0.5 * dot_3d(light_dir, normal) + 0.5

        # big value for last positions in sort
        else:
            z_order[i] = 9999


def read_obj(fileName):
    vertices = []
    triangles = []
    f = open(fileName)
    for line in f:
        if line[:2] == "v ":
            index1 = line.find(" ") + 1
            index2 = line.find(" ", index1 + 1)
            index3 = line.find(" ", index2 + 1)

            vertex = [float(line[index1:index2]), float(line[index2:index3]), float(line[index3:-1]), 1, 1]
            vertices.append(vertex)

        elif line[0] == "f":
            index1 = line.find(" ") + 1
            index2 = line.find(" ", index1 + 1)
            index3 = line.find(" ", index2 + 1)

            triangles.append([int(line[index1:index2]) - 1, int(line[index2:index3]) - 1, int(line[index3:-1]) - 1])

    f.close()

    return np.asarray(vertices), np.asarray(triangles)


# added
# This where brain ends


# Calculate angles with axes
def angles_with_axes(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return 0, 0, 0  # Avoid division by zero
    unit_vector = vector / norm
    angle_x = np.arccos(unit_vector[0])
    angle_y = np.arccos(unit_vector[1])
    angle_z = np.arccos(unit_vector[2])
    return angle_x, angle_y, angle_z


def normalise(vector):
    if np.linalg.norm(vector) != 0:
        vector = vector / np.linalg.norm(vector)
    else:
        vector.fill(0)
    return vector


def rotate_to_direct(points, current_forward, target_direction):
    # Compute the rotation axis (cross product)
    axis = np.cross(current_forward, target_direction)
    axis_norm = np.linalg.norm(axis)

    # Handle edge cases: collinear vectors
    if axis_norm < 1e-6:
        if np.allclose(current_forward, target_direction):
            # Vectors are identical; no rotation needed
            return
        else:
            # Vectors are opposite; rotate around an arbitrary perpendicular axis
            axis = np.array([1, 0, 0])
    else:
        axis = normalise(axis)

    # Compute the rotation angle
    angle = np.arccos(np.clip(np.dot(current_forward, target_direction), -1.0, 1.0))

    # Compute the rotation matrix using Rodrigues' rotation formula
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    one_minus_cos = 1 - cos_angle
    x, y, z = axis

    rotation_matrix = np.array([
        [cos_angle + x * x * one_minus_cos, x * y * one_minus_cos - z * sin_angle, x * z * one_minus_cos + y * sin_angle],
        [y * x * one_minus_cos + z * sin_angle, cos_angle + y * y * one_minus_cos, y * z * one_minus_cos - x * sin_angle],
        [z * x * one_minus_cos - y * sin_angle, z * y * one_minus_cos + x * sin_angle, cos_angle + z * z * one_minus_cos]
    ])

    # Apply the rotation to all points
    for point in points:
        point[:3] = np.dot(rotation_matrix, point[:3])


def draw_ground_plane(surf, camera, grid_size=1, grid_count=50):
    """
    Draw a ground plane grid.
    """
    ground_color = (200, 200, 200)  # Light gray
    for i in range(-grid_count, grid_count + 1):
        # Horizontal lines
        start_x, start_y = project_point(camera, (i * grid_size, 0, -grid_count * grid_size))
        end_x, end_y = project_point(camera, (i * grid_size, 0, grid_count * grid_size))
        pg.draw.line(surf, ground_color, (start_x, start_y), (end_x, end_y), 1)

        # Vertical lines
        start_x, start_y = project_point(camera, (-grid_count * grid_size, 0, i * grid_size))
        end_x, end_y = project_point(camera, (grid_count * grid_size, 0, i * grid_size))
        pg.draw.line(surf, ground_color, (start_x, start_y), (end_x, end_y), 1)


def draw_xyz_axis(surf, camera, axis_length=10):
    """
    Draw XYZ axes.
    """
    axis_colors = {
        "X": (255, 0, 0),  # Red for X
        "Y": (0, 255, 0),  # Green for Y
        "Z": (0, 0, 255),  # Blue for Z
    }

    # X Axis
    start_x, start_y = project_point(camera, (0, 0, 0))
    end_x, end_y = project_point(camera, (axis_length, 0, 0))
    pg.draw.line(surf, axis_colors["X"], (start_x, start_y), (end_x, end_y), 2)

    # Y Axis
    end_x, end_y = project_point(camera, (0, axis_length, 0))
    pg.draw.line(surf, axis_colors["Y"], (start_x, start_y), (end_x, end_y), 2)

    # Z Axis
    end_x, end_y = project_point(camera, (0, 0, axis_length))
    pg.draw.line(surf, axis_colors["Z"], (start_x, start_y), (end_x, end_y), 2)
# /added


def project_point(camera, point):
    """
    Project a 3D point into 2D screen coordinates.
    """
    point = np.array(point)
    projected = np.zeros(5)  # Mock a full 5D point array
    projected[:3] = point
    project_points([projected], camera)
    return projected[3], projected[4]


def rotate_model(points, vector):
    angleY, angleX, angleZ = angles_with_axes(vector)
    cX, sX = np.cos(angleX), np.sin(angleX)
    cY, sY = np.cos(angleY), np.sin(angleY)
    cZ, sZ = np.cos(angleZ), np.sin(angleZ)

    rotation_matrix = np.array([
        [
            cY * cZ,
            cZ * sX * sY - sX * sZ,
            cX * cZ * sY + sX * sZ,
        ],
        [
            cY * sZ,
            cX * cZ + sX * sY * sZ,
            -cZ * sX + cX * sY * sZ,
        ],
        [
            -sY,
            cY * sX,
            cX * cY,
        ],
    ])

    # Apply the rotation to all points
    for point in points:
        point[:3] = np.dot(rotation_matrix, point[:3])


def read_from_json(path_to_file):
    with open(path_to_file, 'r') as file:
        return json.load(file)


if __name__ == '__main__':
    # added
    # Read simulation data file
    print('Starting simulation...')
    sim_file_path = "../Simulation data files/rocket_trajectory(3D).json"
    sim_data = read_from_json(sim_file_path)
    print('Read sim file...')

    # Text Properties
    # TEXT_COLOR = (10, 255, 255)
    # font_ = pg.font.Font(None, 36)

    # /added
    main(sim_data, '../obj models/Rocket.obj')
    pg.quit()


def render():
    print('Starting simulation...')
    sim_file = "Simulation data files/rocket_trajectory(3D).json"
    sim_dat = read_from_json(sim_file)
    print('Read sim file...')

    roc_model = 'obj models/Rocket.obj'

    # Text Properties
    # TEXT_COLOR = (10, 255, 255)
    # font_ = pg.font.Font(None, 36)

    # /added
    main(sim_dat, roc_model)
    pg.quit()