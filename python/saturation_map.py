#!/usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from matplotlib.ticker import FormatStrFormatter, FuncFormatter, MultipleLocator
import numpy as np
from math import *

""" Omni-3-Wheel dimensions """
r = 0.048/2 # in meters
d = 0.116 # in meters
max_ang_vel = 4*pi

W_verts = max_ang_vel * np.array([[-1,-1,-1],
                                  [ 1,-1,-1],
                                  [ 1, 1,-1],
                                  [-1, 1,-1],
                                  [-1,-1, 1],
                                  [ 1,-1, 1],
                                  [ 1, 1, 1],
                                  [-1, 1, 1]])



W_faces = np.array([[W_verts[0],W_verts[1],W_verts[2],W_verts[3]],
                    [W_verts[4],W_verts[5],W_verts[6],W_verts[7]], 
                    [W_verts[0],W_verts[1],W_verts[5],W_verts[4]], 
                    [W_verts[2],W_verts[3],W_verts[7],W_verts[6]], 
                    [W_verts[1],W_verts[2],W_verts[6],W_verts[5]],
                    [W_verts[4],W_verts[7],W_verts[3],W_verts[0]]])



T_inv = (r/3) * np.array([[0, sqrt(3), -sqrt(3)],
                          [-2,      1,        1],
                          [-1/d, -1/d,     -1/d]])


V_verts = np.dot(T_inv, W_verts.T).T


V_faces = np.array([[V_verts[0],V_verts[1],V_verts[2],V_verts[3]],
                    [V_verts[4],V_verts[5],V_verts[6],V_verts[7]], 
                    [V_verts[0],V_verts[1],V_verts[5],V_verts[4]], 
                    [V_verts[2],V_verts[3],V_verts[7],V_verts[6]], 
                    [V_verts[1],V_verts[2],V_verts[6],V_verts[5]],
                    [V_verts[4],V_verts[7],V_verts[3],V_verts[0]]])


""" scale axis to multiples of pi """
scale_to_pi_multiples = pi**(-1)
W_verts_pi =  W_verts * scale_to_pi_multiples
W_faces_pi =  W_faces * scale_to_pi_multiples

V_verts_pi = np.dot(T_inv, W_verts.T).T
V_verts_pi[:,2] *= scale_to_pi_multiples

V_faces_pi = np.array([[V_verts_pi[0],V_verts_pi[1],V_verts_pi[2],V_verts_pi[3]],
                       [V_verts_pi[4],V_verts_pi[5],V_verts_pi[6],V_verts_pi[7]], 
                       [V_verts_pi[0],V_verts_pi[1],V_verts_pi[5],V_verts_pi[4]], 
                       [V_verts_pi[2],V_verts_pi[3],V_verts_pi[7],V_verts_pi[6]], 
                       [V_verts_pi[1],V_verts_pi[2],V_verts_pi[6],V_verts_pi[5]],
                       [V_verts_pi[4],V_verts_pi[7],V_verts_pi[3],V_verts_pi[0]]])




fig1 = plt.figure(num=1, figsize=(10, 5))

# fig1.subplots_adjust(left=0.1, right=0.95, wspace=0.3, hspace=0.3)
fig1.tight_layout()
# fig1.suptitle("Saturation Map", fontsize=16)


ax1 = fig1.add_subplot(121, projection='3d')
ax1.set_title("W", fontsize=15)

ax1.scatter3D(W_verts_pi[:,0], W_verts_pi[:,1], W_verts_pi[:,2])
W_polyg = Poly3DCollection(W_faces_pi, facecolor='cyan', linewidths=1, edgecolors='k', alpha=0.25)
ax1.add_collection3d(W_polyg)
# pc.set_facecolor('cyan')
ax1.set_xlim(-5, 5)
ax1.set_ylim(-5, 5)
ax1.set_zlim(-5, 5)
ax1.set_xlabel('$\omega_1\,[\dfrac{rad}{s}]$', fontsize=13)
ax1.set_ylabel('$\omega_2\,[\dfrac{rad}{s}]$', fontsize=13)
ax1.set_zlabel('$\omega_3\,[\dfrac{rad}{s}]$', fontsize=13)
# ax.set_xticks([-2, -1, 0, 1, 2])
# ax.set_yticks([-2, -1, 0, 1, 2])
# ax.set_zticks([0, 1])
ax1.xaxis.set_major_formatter(FormatStrFormatter('%g $\pi$'))
ax1.xaxis.set_major_locator(MultipleLocator(base=2.0))
ax1.yaxis.set_major_formatter(FormatStrFormatter('%g $\pi$'))
ax1.yaxis.set_major_locator(MultipleLocator(base=2.0))
ax1.zaxis.set_major_formatter(FormatStrFormatter('%g $\pi$'))
ax1.zaxis.set_major_locator(MultipleLocator(base=2.0))
ax1.minorticks_on()
ax1.set_aspect('equal')
# ax.tick_params(axis='both', which='both', bottom=True, top=False, labelbottom=True, labelsize=13, grid_linewidth=0.35, pad=0.2)
ax1.grid(True)

ax2 = fig1.add_subplot(122, projection='3d')
ax2.set_title("V", fontsize=15)
ax2.scatter3D(V_verts_pi[:,0], V_verts_pi[:,1], V_verts_pi[:,2])
V_polyg = Poly3DCollection(V_faces_pi, facecolor='cyan', linewidths=1, edgecolors='k', alpha=0.25)
ax2.add_collection3d(V_polyg)
# ax.set_xlim(-1, 1)
# ax.set_ylim(-1, 1)
ax2.set_zlim(-1, 1)
ax2.set_xlabel('$v_x\,[\dfrac{m}{s}]$', fontsize=13)
ax2.set_ylabel('$v_y\,[\dfrac{m}{s}]$', fontsize=13)
ax2.set_zlabel('$v_{\psi}\,[\dfrac{rad}{s}]$', fontsize=13)
ax2.set_xticks([-0.25,0,0.25])
ax2.set_yticks([-0.25,0,0.25])
ax2.set_zticks([-1,-0.5,0,0.5,1])
ax2.zaxis.set_major_formatter(FormatStrFormatter('%g $\pi$'))
ax2.zaxis.set_major_locator(MultipleLocator(base=1.0))
# ax2.set_zticks(np.arange(-4,5,1))
ax2.minorticks_on()
ax2.set_aspect('equal')
# ax.tick_params(axis='both', which='both', bottom=True, top=False, labelbottom=True, labelsize=13, grid_linewidth=0.35, pad=0.2)
ax2.grid(True)

fig1.savefig("saturation_map.pdf")

plt.show()