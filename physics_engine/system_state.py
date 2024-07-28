from .state_space import StateSpace
import matplotlib.pyplot as plt
import numpy as np

class SystemState(StateSpace):
    def __init__(self, end_time, num_grids):
        self.end_time = end_time
        self.num_grids = num_grids
        self.timeline = np.linspace(0, end_time, num_grids * 10)
        t = np.linspace(0, self.end_time, self.num_grids)
        theta = np.linspace(0, 2 * np.pi, self.num_grids)
        phi = np.linspace(0, np.pi, self.num_grids)
        self.R, self.Theta, self.Phi = np.meshgrid(t, theta, phi)
        self.X, self.Y, self.Z = self.spherical_to_cartesian(self.R, self.Theta, self.Phi)
        self.particles = []

    def get_space_time_grid(self):
        return self.X, self.Y, self.Z

    def get_timeline(self):
        return self.timeline

    def get_time_space_grid(self):
        return self.R, self.Theta, self.Phi

    def spatial_to_timodal(self, x, y, z):
        return self.cartesian_to_spherical(x, y, z)

    def add_particle(self, particle):
        self.particles.append(particle)

    def plot_system(self):
        for particle in self.particles:
            x, y, z = self.get_space_time_grid()
            x_path, y_path, z_path = particle.get_path(self.get_timeline())

            r, theta, phi = self.get_time_space_grid()
            r_path, theta_path, phi_path = self.spatial_to_timodal(x_path, y_path, z_path)

            fig = plt.figure(figsize=(12, 6))  # Adjusted for better spacing

            ax1 = fig.add_subplot(141, projection='3d')
            ax1.plot(x_path, y_path, z_path, color='r', label=particle.path_type + ' Path')
            ax1.set_xlabel('X', fontsize=10, labelpad=15)
            ax1.set_ylabel('Y', fontsize=10, labelpad=15)
            ax1.set_zlabel('Z', fontsize=10, labelpad=15)
            ax1.set_title('3D Space-Time Grid', fontsize=10)
            ax1.legend(fontsize=10)

            ax2 = fig.add_subplot(142, projection='polar')
            ax2.plot(phi_path, r_path, color='r', label=particle.path_type + ' Path')
            ax2.plot(phi[self.end_time//2, :, :], r[self.end_time//2, :, :], color='b')
            ax2.set_xlabel('X', fontsize=10, labelpad=15)
            ax2.set_ylabel('Y', fontsize=10, labelpad=15)
            ax2.set_title('Time-Space Grid (Phi-R)', fontsize=10)
            ax2.legend(fontsize=10)

            ax3 = fig.add_subplot(143, projection='polar')
            ax3.plot(theta_path, r_path, color='r', label=particle.path_type + ' Path')
            ax3.plot(theta[:, :, self.end_time//2], r[:, :, self.end_time//2], color='b')
            ax3.set_xlabel('Theta', fontsize=10, labelpad=15)
            ax3.set_ylabel('Radius', fontsize=10, labelpad=15)
            ax3.set_title('Time-Space Grid (Theta-R)', fontsize=10)
            ax3.legend(fontsize=10)

            ax4 = fig.add_subplot(144, projection='polar')
            ax4.plot(theta_path, phi_path, color='r', label=particle.path_type + ' Path')
            ax4.plot(theta[:, self.end_time//2, :], phi[:, self.end_time//2, :], color='b')
            ax4.set_xlabel('Theta', fontsize=10, labelpad=15)
            ax4.set_ylabel('Radius', fontsize=10, labelpad=15)
            ax4.set_title('Time-Space Grid (Theta-Phi)', fontsize=10)
            ax4.legend(fontsize=10)

            plt.tight_layout()
            plt.savefig('plot_system.pdf', bbox_inches='tight')
            plt.show()

# Font settings and sizes
plt.rc('font', size=8)
plt.rc('axes', titlesize=8)
plt.rc('legend', fontsize=8)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams["savefig.format"] = 'pdf'
