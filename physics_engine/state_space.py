import numpy as np
from scipy.constants import c
import matplotlib.pyplot as plt

class StateSpace:
    @staticmethod
    def spherical_to_cartesian(r, theta, phi):
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        return x, y, z

    @staticmethod
    def cartesian_to_spherical(x, y, z):
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arctan2(y, x)
        phi = np.arccos(z / r)
        return r, theta, phi
    
    @staticmethod
    def gamma(initial_velocity):
        v = np.linalg.norm(initial_velocity)
        return 1 / np.sqrt(1 - (v / c)**2)

    @staticmethod
    def angle_of_existence(x, y, v):
        # Calculate the standard angle
        angle = np.arctan2(y, x)
        # Adjust the angle based on gamma
        if v >= c:
            raise ValueError("Velocity cannot be equal to or exceed the speed of light")
        elif v == 0:
            # If velocity is zero, no relativistic effects
            return angle
        else:
            # Adjust the angle based on gamma
            # Increase the angle as gamma increases
            adjusted_angle = angle * StateSpace.gamma(v)
            # Ensure angle is within a valid range (0 to 2*pi)
            adjusted_angle = np.mod(adjusted_angle, 2 * np.pi)
            return adjusted_angle

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
                Psi[n + 1, i] = 2 * Psi[n, i] - Psi[n - 1, i] + (c * dt / dx)**2 * (Psi[n, i + 1] - 2 * Psi[n, i] + Psi[n, i - 1])
        plt.imshow(Psi, extent=[0, L, 0, T], origin='lower', aspect='auto', cmap='viridis')
        plt.colorbar(label='Wave Function $\Psi$')
        plt.xlabel('Position $x$')
        plt.ylabel('Time $t$')
        plt.title('Wave Propagation')
        plt.show()