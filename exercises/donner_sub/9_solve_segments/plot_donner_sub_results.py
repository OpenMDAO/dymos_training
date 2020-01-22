import openmdao.api as om
import matplotlib.pyplot as plt

#
# Load the cases for the solution and the simulation results
#
cr_sol = om.CaseReader('donner_sub_solution.sql')
sol = cr_sol.get_case(-1)

cr_sim = om.CaseReader('donner_sub_simulation.sql')
sim = cr_sim.get_case(-1)

speed = sol.get_val('traj.phase0.timeseries.input_parameters:v')[0, 0]

fig0, ax0 = plt.subplots(1, 1)
fig1, ax1 = plt.subplots(1, 1)
fig2, ax2 = plt.subplots(1, 1)

for i in range(2):
    t_sol = sol.get_val(f'traj.phase{i}.timeseries.time')
    y_sol = sol.get_val(f'traj.phase{i}.timeseries.states:y')
    x_sol = sol.get_val(f'traj.phase{i}.timeseries.states:x')
    phi_sol = sol.get_val(f'traj.phase{i}.timeseries.controls:phi', units='deg')
    sub_range_sol = sol.get_val(f'traj.phase{i}.timeseries.sub_range')
    
    t_sim = sim.get_val(f'traj.phase{i}.timeseries.time')
    y_sim = sim.get_val(f'traj.phase{i}.timeseries.states:y')
    x_sim = sim.get_val(f'traj.phase{i}.timeseries.states:x')
    phi_sim = sim.get_val(f'traj.phase{i}.timeseries.controls:phi', units='deg')
    sub_range_sim = sim.get_val(f'traj.phase{i}.timeseries.sub_range')
    
    #
    # Plot 1: y vs x
    #
    ax0.set_aspect('equal')
    ax0.plot(x_sol, y_sol, 'ro')
    ax0.plot(x_sim, y_sim, 'k-')
    ax0.set_xlim(-1.5, 1.5)
    ax0.set_ylim(-1.5, 1.5)
    ax0.text(0.5, 1.2, f'speed = {speed:6.4f}')
    
    #
    # Plot 2: sub_range vs time
    #
    ax1.plot(t_sol, sub_range_sol, 'ro')
    ax1.plot(t_sim, sub_range_sim, 'k-')
    ax1.set_xlabel('time')
    ax1.set_ylabel('sub range')
    
    #
    # Plot 3: heading vs time
    #
    ax2.plot(t_sol, phi_sol, 'ro')
    ax2.plot(t_sim, phi_sim, 'k-')
    ax2.set_xlabel('time')
    ax2.set_ylabel('heading angle')

plt.show()