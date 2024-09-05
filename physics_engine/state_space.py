import numpy as np
from scipy.constants import c as speed_of_light
import matplotlib.pyplot as plt

class StateSpace:
    c = speed_of_light
    @staticmethod
    def spherical_to_cartesian(r, time_angle, spatial_polar_angle, azimuthal_angle):
        # Convert 4D spherical to Cartesian coordinates
        ct = r * np.sin(time_angle)  # This is the 4D time dimension
        x = ct * np.cos(spatial_polar_angle) * np.cos(azimuthal_angle)
        y = ct * np.cos(spatial_polar_angle) * np.sin(azimuthal_angle)
        z = ct * np.sin(spatial_polar_angle)
        return x, y, z, ct

    @staticmethod
    def cartesian_to_spherical(x, y, z, t):
        # Convert Cartesian to 4D spherical coordinates
        r = np.sqrt(x**2 + y**2 + z**2 + (StateSpace.c * t)**2)
        time_angle = np.arccos(StateSpace.c * t / r) if r != 0 else 0
        spatial_polar_angle = np.arccos(z / np.sqrt(x**2 + y**2 + z**2)) if x**2 + y**2 + z**2 != 0 else 0
        azimuthal_angle = np.arctan2(y, x)
        return r, time_angle, spatial_polar_angle, azimuthal_angle
    
    @staticmethod
    def gamma(initial_velocity):
        v = np.linalg.norm(initial_velocity)
        return 1 / np.sqrt(1 - (v / StateSpace.c )**2)

    @staticmethod
    def angle_of_existence(azimuthal_angle, v):
        # Calculate the standard angle
        # Adjust the angle based on gamma
        if v >= StateSpace.c:
            raise ValueError("Velocity cannot be equal to or exceed the speed of light")
        elif v == 0:
            # If velocity is zero, no relativistic effects
            return azimuthal_angle
        else:
            # Adjust the angle based on gamma
            # Increase the angle as gamma increases
            adjusted_angle = azimuthal_angle * StateSpace.gamma(v)
            # Ensure angle is within a valid range (0 to 2*pi)
            adjusted_angle = np.mod(adjusted_angle, 2 * np.pi)
            return adjusted_angle
        
    @staticmethod
    def spin_wave_function(x, y, z, t, spin_state='up'):
        # Define the wave function for a given spin state in 4D space-time
        r, theta1, theta2, theta3 = StateSpace.cartesian_to_spherical(x, y, z, t)
        
        if spin_state == 'up':
            phase = 1
        elif spin_state == 'down':
            phase = -1
        else:
            raise ValueError("Spin state must be 'up' or 'down'")
        
        # Define the wave function based on spin state and time
        wave_function = np.exp(1j * (theta1 + theta2 + theta3)) * phase
        return wave_function

    @staticmethod
    def antiparticle_wave_function(x, y, z, t):
        # Define the wave function for an antiparticle
        # This can be represented as a complex conjugate of the particle's wave function
        particle_wave_function = StateSpace.spin_wave_function(x, y, z, t, spin_state='up')
        antiparticle_wave_function = np.conj(particle_wave_function)
        return antiparticle_wave_function 

    @staticmethod
    def energy(initial_velocity, mass):
        v = np.linalg.norm(initial_velocity)
        gamma = StateSpace.gamma()
        return gamma * mass * v

    @staticmethod
    def solve_wave_equation(L, T, nx, nt):
        dx = L / (nx - 1)
        dt = T / (nt - 1)
        x = np.linspace(0, L, nx)
        t = np.linspace(0, T, nt)
        X, T = np.meshgrid(x, t)
        Psi = np.zeros((nt, nx))
        Psi[0, :] = np.exp(-100 * (x - L/2)**2)
        for n in range(0, nt - 1):
            for i in range(1, nx - 1):
                Psi[n + 1, i] = 2 * Psi[n, i] - Psi[n - 1, i] + (StateSpace.c * dt / dx)**2 * (Psi[n, i + 1] - 2 * Psi[n, i] + Psi[n, i - 1])
        plt.imshow(Psi, extent=[0, L, 0, T], origin='lower', aspect='auto', cmap='viridis')
        plt.colorbar(label='Wave Function $\Psi$')
        plt.xlabel('Position $x$')
        plt.ylabel('Time $t$')
        plt.title('Wave Propagation')
        plt.show()