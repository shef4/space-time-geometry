import numpy as np

class Particle:
    def __init__(self, initial_r, initial_theta, initial_phi, initial_velocity, spin_frequency=1.0, spin_amplitude=1.0):
        """
        Initialize the Particle with its properties.
        
        Parameters:
        - initial_r: Radial distance from the origin
        - initial_theta: Polar angle in spherical coordinates
        - initial_phi: Azimuthal angle in spherical coordinates
        - initial_velocity: Dictionary with 'linear_v', 'angular_v', and 'complex_spin'
        - spin_frequency: Frequency of the spin
        - spin_amplitude: Amplitude of the spin
        - path_type: Type of path ('stationary', 'linear_motion', etc.)
        """
        self.r = initial_r
        self.theta = initial_theta
        self.phi = initial_phi
        self.spin_frequency = spin_frequency
        self.spin_amplitude = spin_amplitude
        
        # Extract velocities and spins from the dictionary
        self.linear_v = initial_velocity.get('linear_v', {'x': 0, 'y': 0, 'z': 0})
        self.angular_v = initial_velocity.get('angular_v', {'xy': 0, 'xz': 0, 'yz': 0})
        self.spin_states = initial_velocity.get('spin_states', {'xy': 0, 'xz': 0, 'yz': 0})

    
    def get_path(self, t):
        """Compute the particle's path based on its type and parameters."""
        # Calculate linear momentum effects
        linear_momentum_x = self.linear_v['x'] * t
        linear_momentum_y = self.linear_v['y']  * t
        linear_momentum_z = self.linear_v['z']  * t

        # Calculate complex spin states
        complex_spin_xy = np.exp(1j * self.spin_states['xy'] * self.spin_frequency * t)
        complex_spin_xz = np.exp(1j * self.spin_states['xz'] * self.spin_frequency * t)
        complex_spin_yz = np.exp(1j * self.spin_states['yz'] * self.spin_frequency * t)

        # Calculate rotational effects
        rotation_xy = np.exp(1j * self.angular_v['xy'] * t)
        rotation_xz = np.exp(1j * self.angular_v['xz'] * t)
        rotation_yz = np.exp(1j * self.angular_v['yz'] * t)

        # Combine linear, spin, and rotational effects to compute the final coordinates
        x = (linear_momentum_x 
            + self.r * np.sin(self.phi) * np.cos(self.theta) * np.real(complex_spin_xy) 
            + self.spin_amplitude * np.real(rotation_xy))
        y = (linear_momentum_y 
            + self.r * np.sin(self.phi) * np.sin(self.theta) * np.imag(complex_spin_yz) 
            + self.spin_amplitude * np.imag(rotation_yz))
        z = (linear_momentum_z 
            + self.r * np.cos(self.phi) 
            + self.spin_amplitude * np.imag(rotation_xz) 
            + self.spin_amplitude * np.real(complex_spin_xz))

        return x, y, z
