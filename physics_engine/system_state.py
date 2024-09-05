from .state_space import StateSpace
import matplotlib.pyplot as plt
import numpy as np

class SystemState(StateSpace):
    def __init__(self, end_time, num_grids):
        self.end_time = end_time
        self.num_grids = num_grids
        self.timeline = np.linspace(0, end_time, num_grids * 10)
        t = np.linspace(0, self.end_time, self.num_grids)
        theta1 = np.linspace(0, np.pi, self.num_grids)  # Replaces theta for spherical coordinates
        theta2 = np.linspace(0, np.pi, self.num_grids)  # Replaces phi for spherical coordinates
        theta3 = np.linspace(0, 2 * np.pi, self.num_grids)  # Replaces phi for spherical coordinates
        self.R, self.Theta1, self.Theta2, self.Theta3 = np.meshgrid(t, theta1, theta2, theta3)
        self.X, self.Y, self.Z, self.CT = self.spherical_to_cartesian(self.R, self.Theta1, self.Theta2, self.Theta3)
        self.particles = []

    def get_space_time_grid(self):
        return self.X, self.Y, self.Z, self.CT

    def get_timeline(self):
        return self.timeline

    def get_time_space_grid(self):
        return self.R, self.Theta1, self.Theta2, self.Theta3

    def spatial_to_timodal(self, x, y, z, t):
        return self.cartesian_to_spherical(x, y, z, t)

    def add_particle(self, particle):
        self.particles.append(particle)

    def plot_system(self):
        for idx, particle in enumerate(self.particles):
            fig = plt.figure(figsize=(14, 10))  # Adjusted for better spacing

            # Plot 3D Space-Time Grid
            ax1 = fig.add_subplot(141, projection='3d')
            x, y, z, ct = self.get_space_time_grid()
            x_path, y_path, z_path, t_path = particle.get_path(self.get_timeline())
            ax1.plot(x_path, y_path, z_path, color='r', label='particle_' + str(idx) + ' Path')
            ax1.set_xlabel('X', fontsize=10, labelpad=15)
            ax1.set_ylabel('Y', fontsize=10, labelpad=15)
            ax1.set_zlabel('Z', fontsize=10, labelpad=15)
            ax1.set_title('3D Space-Time Grid', fontsize=10)
            ax1.legend(fontsize=10)

            # Plot Time vs Radius (Polar)
            ax2 = fig.add_subplot(142, projection='polar')
            r, theta1, theta2, theta3 = self.get_time_space_grid()
            r_path, theta1_path, theta2_path = self.spatial_to_timodal(x_path, y_path, z_path, t_path)
            ax2.plot(theta1_path, r_path, color='r', label='particle_' + str(idx) + ' Path')
            ax2.plot(self.Theta1[self.end_time // 2, :, :, :], r[self.end_time // 2, :, :, :], color='b')
            ax2.set_xlabel('Theta1', fontsize=10, labelpad=15)
            ax2.set_ylabel('Radius', fontsize=10, labelpad=15)
            ax2.set_title('Time-Space Grid (Theta1-R)', fontsize=10)
            ax2.legend(fontsize=10)

            # Plot Time vs Theta2 (Polar)
            ax3 = fig.add_subplot(143, projection='polar')
            ax3.plot(theta2_path, r_path, color='r', label='particle_' + str(idx) + ' Path')
            ax3.plot(self.Theta2[:, :, self.end_time // 2], r[:, :, self.end_time // 2], color='b')
            ax3.set_xlabel('Theta2', fontsize=10, labelpad=15)
            ax3.set_ylabel('Radius', fontsize=10, labelpad=15)
            ax3.set_title('Time-Space Grid (Theta2-R)', fontsize=10)
            ax3.legend(fontsize=10)

            # Plot Time vs Theta3 (Polar)
            ax4 = fig.add_subplot(144, projection='polar')
            ax4.plot(theta3_path, phi_path, color='r', label='particle_' + str(idx) + ' Path')
            ax4.plot(self.Theta3[:, self.end_time // 2, :], phi[:, self.end_time // 2, :], color='b')
            ax4.set_xlabel('Theta3', fontsize=10, labelpad=15)
            ax4.set_ylabel('Phi', fontsize=10, labelpad=15)
            ax4.set_title('Time-Space Grid (Theta3-Phi)', fontsize=10)
            ax4.legend(fontsize=10)

            plt.tight_layout()
            plt.savefig('plot_system.pdf', bbox_inches='tight')
            plt.show()

            print("Particle linear velocity:", particle.linear_v)
            print("Particle angular velocity:", particle.angular_v)
            print("Particle spin states velocity:", particle.spin_states)

# Font settings and sizes
plt.rc('font', size=8)
plt.rc('axes', titlesize=8)
plt.rc('legend', fontsize=8)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams["savefig.format"] = 'pdf'
