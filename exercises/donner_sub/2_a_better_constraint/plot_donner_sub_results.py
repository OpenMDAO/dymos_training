import openmdao.api as om
import matplotlib.pyplot as plt

cr_sol = om.CaseReader('donner_sub_solution.sql')
sol = cr_sol.get_case(-1)

cr_sim = om.CaseReader('donner_sub_simulation.sql')
sim = cr_sim.get_case(-1)

speed = sol.get_val('traj.phase0.timeseries.design_parameters:v')[0, 0]

lat = sol.get_val('traj.phase0.timeseries.states:y')
lon = sol.get_val('traj.phase0.timeseries.states:x')

lat_x = sim.get_val('traj.phase0.timeseries.states:y')
lon_x = sim.get_val('traj.phase0.timeseries.states:x')

fig, ax = plt.subplots(1, 1)
ax.set_aspect('equal')
ax.plot(lon, lat, 'ro')
ax.plot(lon_x, lat_x, 'k-')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.text(0.5, 1.2, f'speed = {speed:6.4f}')
plt.show()
