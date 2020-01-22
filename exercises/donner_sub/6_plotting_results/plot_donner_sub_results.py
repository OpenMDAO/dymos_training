import openmdao.api as om
import matplotlib.pyplot as plt

cr_sol = om.CaseReader('donner_sub_solution.sql')
sol = cr_sol.get_case(-1)

cr_sim = om.CaseReader('donner_sub_simulation.sql')
sim = cr_sim.get_case(-1)

speed = sol.get_val('traj.phase0.timeseries.design_parameters:v')[0, 0]

t = sol.get_val('traj.phase0.timeseries.time')
lat = sol.get_val('traj.phase0.timeseries.states:y')
lon = sol.get_val('traj.phase0.timeseries.states:x')
sub_range = sol.get_val('traj.phase0.timeseries.sub_range')

t_sim = sim.get_val('traj.phase0.timeseries.time')
lat_sim = sim.get_val('traj.phase0.timeseries.states:y')
lon_sim = sim.get_val('traj.phase0.timeseries.states:x')
sub_range_sim = sim.get_val('traj.phase0.timeseries.sub_range')

fig, ax = plt.subplots(1, 1)
ax.set_aspect('equal')
ax.plot(lon, lat, 'ro', label='solution')
ax.plot(lon_sim, lat_sim, 'k-', label='simulation')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-0.25, 0.75)
ax.text(0.5, 0.6, f'speed = {speed:6.4f}')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend(loc='upper left')

plt.savefig('solution_vs_simulation.pdf')

fig, ax = plt.subplots(1, 1)
ax.plot(t, sub_range, 'ro', label='solution')
ax.plot(t_sim, sub_range_sim, 'k-', label='simulation')
ax.set_xlabel('time')
ax.set_ylabel('sub_range')
ax.legend(loc='upper right')

plt.savefig('sub_range_vs_time.pdf')

plt.show()
