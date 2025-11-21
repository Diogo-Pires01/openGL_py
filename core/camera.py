import glm
import glfw

class Camera:
    def __init__(self, position=glm.vec3(0.0, 2.0, 15.0)):
        self.position = position
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.yaw = -90.0
        self.pitch = 0.0
        self.lastX = 640
        self.lastY = 360
        self.first_mouse = True
        self.speed = 0.03
        self.sensitivity = 0.1

        self.velocity_y = 0.0
        self.gravity = -0.001
        self.jump_strength = 0.2
        self.on_ground = True
        self.ground_height = 0.0

        self.min_x = -150
        self.max_x = 150
        self.min_z = -150
        self.max_z = 150

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def process_input(self, window):
        move_direction = glm.vec3(0.0, 0.0, 0.0)
        current_speed = self.speed

        if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
            current_speed *= 2.5

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            move_direction += self.front

        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            move_direction -= self.front

        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            move_direction -= glm.normalize(glm.cross(self.front, self.up))

        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            move_direction += glm.normalize(glm.cross(self.front, self.up))

        move_direction.y = 0.0

        if glm.length(move_direction) > 0:
            move_direction = glm.normalize(move_direction)
            self.position += move_direction * current_speed

        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False

        self.velocity_y += self.gravity
        self.position.y += self.velocity_y

        if self.position.y <= self.ground_height + 2.0:
            self.position.y = self.ground_height + 2.0
            self.velocity_y = 0.0
            self.on_ground = True

        self.position.x = max(self.min_x, min(self.position.x, self.max_x))
        self.position.z = max(self.min_z, min(self.position.z, self.max_z))

    def mouse_callback(self, window, xpos, ypos):
        if self.first_mouse:
            self.lastX = xpos
            self.lastY = ypos
            self.first_mouse = False

        xoffset = (xpos - self.lastX) * self.sensitivity
        yoffset = (self.lastY - ypos) * self.sensitivity
        self.lastX = xpos
        self.lastY = ypos

        self.yaw += xoffset
        self.pitch += yoffset
        self.pitch = max(-89.0, min(89.0, self.pitch))

        direction = glm.vec3()
        direction.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        direction.y = glm.sin(glm.radians(self.pitch))
        direction.z = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.front = glm.normalize(direction)
