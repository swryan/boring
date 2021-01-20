"""
High Fidelity Baseline Model

See Wiki for Install Requirements
(https://github.com/jcchin/boring/wiki)

Author: Jeff Chin
"""

from dolfin import *
from mshr import *

import matplotlib.pyplot as plt;
from matplotlib.animation import FuncAnimation

from IPython.display import clear_output, display; import time; import dolfin.common.plotting as fenicsplot 
import time

import os, sys, shutil

# Define domain and mesh
cell_d = 1.8; # diameter of the cell
extra = 1.5;  # extra space along the diagonal
ratio = 2.;  # cell diameter/cutout diameter
n_cells = 3;  # number of cells
diagonal = (n_cells*cell_d)+((n_cells)*(cell_d/ratio))*extra;  # diagonal distance from corner to corner
side = diagonal/(2**0.5);  # square side length

XMIN, XMAX = 0, side; 
YMIN, YMAX = 0, side; 
G = [XMIN, XMAX, YMIN, YMAX];
mresolution = 30; # number of cells

# Define 2D geometry

offset = side/n_cells
holes = [Circle(Point(offset*i,offset*j), cell_d/(2*ratio)) for j in range(n_cells+1) for i in range(n_cells+1)] # nested list comprehension creates a size (n+1)*(n+1) array

domain = Rectangle(Point(G[0], G[2]), Point(G[1], G[3]))
for hole in holes:
  domain = domain - hole

offset2 = side/n_cells
batts = [Circle(Point(side/(2*n_cells)+offset2*i,side/(2*n_cells)+offset2*j), cell_d/2) for j in range(n_cells) for i in range(n_cells)]

for (i, batt) in enumerate(batts):
  domain.set_subdomain(1+i, batt) # add cells to domain as a sub-domain
mesh = generate_mesh(domain, mresolution)


#mesh = generate_mesh(Rectangle(Point(G[0], G[2]), Point(G[1], G[3])), mresolution)
#mesh = generate_mesh(Circle(Point(0.0), 2.0), mresolution)

markers = MeshFunction('size_t', mesh, 2, mesh.domains())  # size_t = non-negative integers
dx = Measure('dx', domain=mesh, subdomain_data=markers)
boundaries = MeshFunction('size_t', mesh, 1, mesh.domains())


plot(markers,"Subdomains")

plt.show()


def plot_compact(u, t, stepcounter, QQ, pl, ax): # Compact plot utility function
  if stepcounter == 0:
    pl, ax = plt.subplots(); display(pl); clear_output(); # Plotting setup
  if stepcounter % 5 == 0:
    uEuclidnorm = project(sqrt(inner(u, u)), QQ);
    #plt.clf();
    fig = plt.gcf();
    fig.set_size_inches(16, 4)
    plt.subplot(1, 2, 1); pp = plot(uEuclidnorm, cmap="coolwarm"); plt.title("Solution at t=%f" % (t)) # Plot norm of velocity
    if t == 0.: plt.axis(G); # plt.colorbar(pp, shrink=0.5); 
    plt.subplot(1, 2, 2);
    if t == 0.: plot(QQ.mesh()); plt.title("Mesh") # Plot mesh
    plt.tight_layout(); dpl = display(pl, display_id="test");
  
  return (pl, ax)

class Conductivity(UserExpression):
    def __init__(self, markers, **kwargs):
        super(Conductivity, self).__init__(**kwargs)
        self.markers = markers
    def eval_cell(self, values, x, cell):
        if self.markers[cell.index] == 0:
            values[0] = 11.4 # copper
        else:
            values[0] = 1      # aluminum


  
#k_coeff = 0.5
k_coeff = Conductivity(markers, degree=1)

# Define finite element function space
degree = 1;
V = FunctionSpace(mesh, "CG", degree);

# Finite element functions
v = TestFunction(V); 
u = Function(V);

# Time parameters
theta = 1.0 # Implicit Euler
k = 0.05; # Time step
t, T = 0., 5.; # Start and end time

# Exact solution
kappa = 1e-1
rho = 1.0;

# Boundray Conditions (Ezra)
tol = 1E-14
for f in facets(mesh):
    domains = []
    for c in cells(f):
        domains.append(markers[c])

    domains = list(set(domains))
    # Domains with [0,i] refer to each boundary within the "copper" plate
    # Domains 1-9 refer to the domains of the batteries
    if domains == [1]:
        boundaries[f] = 2

u1= Constant(298.0)
ue = Constant(325.0)
ue.t = k/10.;
u0 = u1;

Q = Constant(71000)
L_N = Q*v*dx(2)

bc_D = DirichletBC(V, ue, boundaries, 2)

# Inititalize time stepping
pl, ax = None, None; 
stepcounter = 0; 
timer0 = time.time()

# Time-stepping loop
while t < T: 
    # Time scheme
    um = theta*u + (1.0-theta)*u0 
    
    # Weak form of the heat equation in residual form
    r = (u - u0)/k*v*dx + k_coeff*inner(grad(um), grad(v))*dx 
    
    # Solve the Heat equation (one timestep)
    solve(r==0, u, bc_D)  
    
    # Plot all quantities (see implementation above)
    #plt.clf()
    pl, ax=plot_compact(u, t, stepcounter, V, pl, ax)
    #ani = FuncAnimation(plt.figure(), plot_compact, blit=True)
    #plt.show()
    # Shift to next timestep
    t += k; u0 = project(u, V); 
    ue.t = t;
    stepcounter += 1 


W = VectorFunctionSpace(mesh, 'P', degree)
flux_u = project(-k_coeff*grad(u),W)
plot(flux_u, title='Flux Field')
plt.show()
print(flux_u.vector().max())