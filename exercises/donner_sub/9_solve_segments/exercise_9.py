import openmdao.api as om
import dymos as dm

from donner_sub_ode import DonnerSubODE

# Create the problem
p = om.Problem(model=om.Group())

# Add the trajectory (optional for single phase problems)
traj = dm.Trajectory()

# Create the phases
phase0 = dm.Phase(ode_class=DonnerSubODE,
                  transcription=dm.GaussLobatto(num_segments=10, order=3, compressed=True, ???))

phase1 = dm.Phase(ode_class=DonnerSubODE,
                  transcription=dm.Radau(num_segments=10, order=3, compressed=True, ???))

# Add the phase to the trajectory, and the trajectory to the model
traj.add_phase('phase0', phase=phase0)
traj.add_phase('phase1', phase=phase1)
traj.link_phases(phases=['phase0', 'phase1'], vars=['time', 'x', 'y', 'phi'])
p.model.add_subsystem('traj', traj)

#
# Configure the first phase
#
phase0.set_time_options(units=None, targets=['threat_comp.time'], fix_initial=True, duration_bounds=(0.1, 100))
phase0.add_state('x', rate_source='eom_comp.dx_dt', targets=['nav_comp.x'], fix_initial=True, fix_final=False)
phase0.add_state('y', rate_source='eom_comp.dy_dt', targets=['nav_comp.y'], fix_initial=True, fix_final=False)

# phase0.add_input_parameter('v', targets=['eom_comp.v'])
phase0.add_control('phi', targets=['eom_comp.phi'], units='rad')

phase0.add_boundary_constraint('eom_comp.dy_dt', loc='final', equals=0, shape=(1,))

phase0.add_path_constraint('threat_comp.sub_range', lower=0)
phase0.add_path_constraint('eom_comp.dy_dt', lower=0)

phase0.add_timeseries_output('nav_comp.r_ship2', shape=(1,))
phase0.add_timeseries_output('threat_comp.sub_range', shape=(1,))

#
# Configure the second phase
#
phase1.set_time_options(units=None, targets=['threat_comp.time'], fix_initial=False, duration_bounds=(0.1, 100))
phase1.add_state('x', rate_source='eom_comp.dx_dt', targets=['nav_comp.x'], fix_initial=False, fix_final=True)
phase1.add_state('y', rate_source='eom_comp.dy_dt', targets=['nav_comp.y'], fix_initial=False, fix_final=True)

phase1.add_control('phi', targets=['eom_comp.phi'], units='rad')

phase1.add_path_constraint('threat_comp.sub_range', lower=0)
phase1.add_path_constraint('eom_comp.dy_dt', upper=0)

phase1.add_timeseries_output('nav_comp.r_ship2', shape=(1,))
phase1.add_timeseries_output('threat_comp.sub_range', shape=(1,))

# Add a design parameter to the trajectory
traj.add_design_parameter('v', custom_targets={'phase0': ['eom_comp.v'], 'phase1': ['eom_comp.v']}, units=None, opt=True, upper=5, lower=0.1)
traj.add_objective('design_parameters:v')

#
# Set up the driver
#
p.driver = om.pyOptSparseDriver()
p.driver.options['optimizer'] = 'SNOPT'
p.driver.opt_settings['iSumm'] = 6
p.driver.declare_coloring()

p.driver.add_recorder(om.SqliteRecorder("donner_sub_solution.sql"))
p.driver.recording_options['includes'] = ['*timeseries*']
p.driver.recording_options['record_objectives'] = True
p.driver.recording_options['record_constraints'] = True
p.driver.recording_options['record_desvars'] = True

p.setup()

#
# Set our initial guesses for the solution
#
p.set_val('traj.phase0.t_initial', value=0)
p.set_val('traj.phase0.t_duration', value=1.0)
p.set_val('traj.phase0.states:y', value=phase0.interpolate(ys=[0, 0], nodes='state_input'))
p.set_val('traj.phase0.states:x', value=phase0.interpolate(ys=[-1, 0], nodes='state_input'))
p.set_val('traj.phase0.controls:phi',
          value=phase0.interpolate(ys=[80, 90], nodes='control_input'),
          units='deg')

p.set_val('traj.phase1.t_initial', value=1.0)
p.set_val('traj.phase1.t_duration', value=1.0)
p.set_val('traj.phase1.states:y', value=phase1.interpolate(ys=[0, 0], nodes='state_input'))
p.set_val('traj.phase1.states:x', value=phase1.interpolate(ys=[0, 1], nodes='state_input'))
p.set_val('traj.phase1.controls:phi',
          value=phase1.interpolate(ys=[90, 100], nodes='control_input'),
          units='deg')

p.set_val('traj.design_parameters:v', value=2.0)

#
# Solve the problem
#
phase0.refine_options['refine'] = True
phase0.refine_options['tolerance'] = 1.0E-6
phase0.refine_options['max_order'] = 11

dm.run_problem(p, refine=False)

#
# Simulate the problem using the optimized control time history
#
exp_out = traj.simulate(record_file='donner_sub_simulation.sql')

print('Max y:', p.get_val('traj.phase0.timeseries.states:y').ravel()[-1])
