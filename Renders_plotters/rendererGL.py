import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

# Screen dimensions
SCREEN_W, SCREEN_H = 800, 600

# Camera variables
camera_pos = np.array([13.0, 0.5, 3.3])
camera_angle_h = 0.0  # Horizontal angle
camera_angle_v = 0.0  # Vertical angle
camera_speed = 0.5

# Camera velocity for smooth movement
camera_velocity = np.array([0.0, 0.0, 0.0])
camera_acceleration = 0.1
camera_deceleration = 0.05

# Lighting direction
light_dir = np.array([1.0, 1.0, 1.0])

# Key states dictionary
key_states = {}

# Mouse tracking variables
mouse_last_x, mouse_last_y = SCREEN_W // 2, SCREEN_H // 2
mouse_sensitivity = 0.005  # Adjust sensitivity for mouse movements


def key_callback(window, key, scancode, action, mods):
    """GLFW key callback to handle key presses."""
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        else:
            key_states[key] = True
    elif action == glfw.RELEASE:
        key_states[key] = False


def handle_mouse_movement(window):
    """Handle mouse movement to update camera angles."""
    global camera_angle_h, camera_angle_v, mouse_last_x, mouse_last_y

    # Get current mouse position
    mouse_x, mouse_y = glfw.get_cursor_pos(window)

    # Calculate the offset since the last frame
    x_offset = (mouse_x - mouse_last_x) * mouse_sensitivity
    y_offset = (mouse_last_y - mouse_y) * mouse_sensitivity  # Inverted for OpenGL

    # Update last mouse positions
    mouse_last_x, mouse_last_y = SCREEN_W // 2, SCREEN_H // 2

    # Update camera angles
    camera_angle_h += x_offset
    camera_angle_v += y_offset

    # Limit the vertical angle to prevent flipping
    camera_angle_v = np.clip(camera_angle_v, -np.pi / 2, np.pi / 2)

    # Recenter the mouse cursor
    glfw.set_cursor_pos(window, SCREEN_W // 2, SCREEN_H // 2)


def read_obj(file_name):
    """Read vertices and faces from an OBJ file."""
    vertices = []
    triangles = []
    try:
        with open(file_name) as f:
            for line in f:
                if line.startswith("v "):
                    vertices.append([float(x) for x in line.strip().split()[1:]])
                elif line.startswith("f "):
                    triangles.append([int(x.split("/")[0]) - 1 for x in line.strip().split()[1:]])
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()
    return np.array(vertices), np.array(triangles)


def draw_triangles(vertices, triangles, color_scale=1.0):
    """Render triangles."""
    light_dir_normalized = light_dir / np.linalg.norm(light_dir)

    glBegin(GL_TRIANGLES)
    for tri in triangles:
        tri_vertices = vertices[tri]

        # Calculate normal for lighting
        vec1 = tri_vertices[1] - tri_vertices[0]
        vec2 = tri_vertices[2] - tri_vertices[0]
        normal = np.cross(vec1, vec2)
        normal = normal / np.linalg.norm(normal)

        # Compute shading (simple Lambertian reflection)
        shade = max(0.0, np.dot(normal, light_dir_normalized)) * color_scale + 0.2

        glColor3f(shade, shade, shade)
        for vertex in tri_vertices:
            glVertex3f(*vertex)
    glEnd()


def handle_camera_movement():
    """Update camera position and direction based on input."""
    global camera_pos, camera_angle_h, camera_angle_v, camera_velocity

    # Calculate the desired movement direction
    direction = np.array([0.0, 0.0, 0.0])
    if key_states.get(glfw.KEY_W, False):
        direction += np.array([np.sin(camera_angle_h), 0, -np.cos(camera_angle_h)])
    if key_states.get(glfw.KEY_S, False):
        direction -= np.array([np.sin(camera_angle_h), 0, -np.cos(camera_angle_h)])
    if key_states.get(glfw.KEY_A, False):
        direction -= np.cross([np.sin(camera_angle_h), 0, -np.cos(camera_angle_h)], [0, 1, 0])
    if key_states.get(glfw.KEY_D, False):
        direction += np.cross([np.sin(camera_angle_h), 0, -np.cos(camera_angle_h)], [0, 1, 0])
    if key_states.get(glfw.KEY_SPACE, False):
        direction[1] += 1
    if key_states.get(glfw.KEY_LEFT_SHIFT, False):
        direction[1] -= 1

    # Normalize direction
    if np.linalg.norm(direction) > 0:
        direction = direction / np.linalg.norm(direction)

    # Apply acceleration
    if np.any(direction != 0):
        camera_velocity += direction * camera_acceleration
    else:
        # Decelerate to stop if no key is pressed
        camera_velocity -= camera_velocity * camera_deceleration

    # Update camera position
    camera_pos += camera_velocity


def main():
    if not glfw.init():
        return

    # Create window
    window = glfw.create_window(SCREEN_W, SCREEN_H, "Rocket Simulation - OpenGL", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, glfw.TRUE)

    glfw.set_key_callback(window, key_callback)

    # OpenGL setup
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.3, 0.5, 1.0)

    # Load rocket model
    vertices, triangles = read_obj("../obj models/Rocket.obj")
    color_scale = 230 / np.max(np.abs(vertices))

    # Center mouse cursor
    glfw.set_cursor_pos(window, SCREEN_W // 2, SCREEN_H // 2)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Handle mouse movement
        handle_mouse_movement(window)

        # Set perspective projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, SCREEN_W / SCREEN_H, 0.1, 100)

        # Set camera view
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
                  camera_pos[0] + np.sin(camera_angle_h), camera_pos[1] + np.sin(camera_angle_v),
                  camera_pos[2] - np.cos(camera_angle_h),
                  0, 1, 0)

        # Handle camera movement
        handle_camera_movement()

        # Draw rocket
        draw_triangles(vertices, triangles, color_scale)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
