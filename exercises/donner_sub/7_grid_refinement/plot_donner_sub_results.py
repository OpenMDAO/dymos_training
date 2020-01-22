import openmdao.api as om
import matplotlib.pyplot as plt

#
# Load the cases for the solution and the simulation results
#
cr_sol = om.CaseReader('donner_sub_solution.sql')
sol = cr_sol.get_case(-1)

cr_sim = om.CaseReader('donner_sub_simulation.sql')
sim = cr_sim.get_case(-1)

speed = sol.get_val('traj.phase0.timeseries.design_parameters:v')[0, 0]

t_sol = sol.get_val('traj.phase0.timeseries.time')
y_sol = sol.get_val('traj.phase0.timeseries.states:y')
x_sol = sol.get_val('traj.phase0.timeseries.states:x')
phi_sol = sol.get_val('traj.phase0.timeseries.controls:phi', units='deg')
sub_range_sol = sol.get_val('traj.phase0.timeseries.sub_range')

t_sim = sim.get_val('traj.phase0.timeseries.time')
y_sim = sim.get_val('traj.phase0.timeseries.states:y')
x_sim = sim.get_val('traj.phase0.timeseries.states:x')
phi_sim = sim.get_val('traj.phase0.timeseries.controls:phi', units='deg')
sub_range_sim = sim.get_val('traj.phase0.timeseries.sub_range')

#
# Plot 1: y vs x
#
fig, ax = plt.subplots(1, 1)
ax.set_aspect('equal')
ax.plot(x_sol, y_sol, 'ro')
ax.plot(x_sim, y_sim, 'k-')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.text(0.5, 1.2, f'speed = {speed:6.4f}')

#
# Plot 2: sub_range vs time
#
fig, ax = plt.subplots(1, 1)
ax.plot(t_sol, sub_range_sol, 'ro')
ax.plot(t_sim, sub_range_sim, 'k-')
ax.set_xlabel('time')
ax.set_ylabel('sub range')

#
# Plot 3: heading vs time
#
fig, ax = plt.subplots(1, 1)
ax.plot(t_sol, phi_sol, 'ro')
ax.plot(t_sim, phi_sim, 'k-')
ax.set_xlabel('time')
ax.set_ylabel('heading angle')

plt.show()