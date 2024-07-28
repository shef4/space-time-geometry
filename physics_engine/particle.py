import numpy as np

class Particle:
    def __init__(self, initial_r, initial_theta, initial_phi, initial_velocity, spin_frequency=1.0, spin_amplitude=1.0, path_type='stationary'):
        self.r = initial_r
        self.theta = initial_theta
        self.phi = initial_phi
        self.initial_velocity = initial_velocity
        self.spin_frequency = spin_frequency
        self.spin_amplitude = spin_amplitude
        self.path_type = path_type

    def set_path(self, path_type):
        self.path_type = path_type

    def get_path(self, t):
        v_x, v_y, v_z = self.initial_velocity
        if self.path_type == 'stationary':
            x = np.full_like(t, self.r * np.sin(self.phi) * np.cos(self.theta))
            y = np.full_like(t, self.r * np.sin(self.phi) * np.sin(self.theta))
            z = np.full_like(t, self.r * np.cos(self.phi))
        elif self.path_type == 'constant_motion':
            x = self.r * np.sin(self.phi) * np.cos(self.theta) + v_x * t
            y = self.r * np.sin(self.phi) * np.sin(self.theta) + v_y * t
            z = self.r * np.cos(self.phi) + v_z * t
        elif self.path_type == 'constant_motion_and_spin':
            x = self.r * np.sin(self.phi) * np.cos(self.theta) + self.spin_amplitude * np.cos(self.spin_frequency * t) + v_x * t
            y = self.r * np.sin(self.phi) * np.sin(self.theta) + self.spin_amplitude * np.sin(self.spin_frequency * t) + v_y * t
            z = self.r * np.cos(self.phi) + v_z * t
        elif self.path_type == 'stationary_and_spin':
            x = self.r * np.sin(self.phi) * np.cos(self.theta) + self.spin_amplitude * np.cos(self.spin_frequency * t)
            y = self.r * np.sin(self.phi) * np.sin(self.theta) + self.spin_amplitude * np.sin(self.spin_frequency * t)
            z = self.r * np.cos(self.phi)
        elif self.path_type == 'stationary_and_complex_spin':
            x = self.r * np.sin(self.phi) * np.cos(self.theta) + self.spin_amplitude * np.cos(self.spin_frequency * t)
            y = self.r * np.sin(self.phi) * np.sin(self.theta) + self.spin_amplitude * np.sin(self.spin_frequency * t)
            z = self.r * np.cos(self.phi) + self.spin_amplitude * np.sin(self.spin_frequency * t)
        elif self.path_type == 'rotation':
            x = self.r * np.sin(self.phi) * np.cos(self.theta + self.spin_frequency * t) + v_x * t
            y = self.r * np.sin(self.phi) * np.sin(self.theta + self.spin_frequency * t) + v_y * t
            z = self.r * np.cos(self.phi + self.spin_frequency * t) + v_z * t
        elif self.path_type == 'complex_rotation':
            x = self.r * np.sin(self.phi) * np.cos(self.theta + self.spin_frequency * t) + self.spin_amplitude * np.cos(self.spin_frequency * t) + v_x * t
            y = self.r * np.sin(self.phi) * np.sin(self.theta + self.spin_frequency * t) + self.spin_amplitude * np.sin(self.spin_frequency * t) + v_y * t
            z = self.r * np.cos(self.phi) + self.spin_amplitude * np.sin(self.spin_frequency * t) + v_z * t
        else:
            raise ValueError("Invalid path type")
        return x, y, z
