import openmdao.api as om
import dymos as dm

from donner_sub_ode import DonnerSubODE

# Create the problem
p = om.Problem(model=om.Group())

# Add the trajectory (optional for single phase problems)
traj = dm.Trajectory()

# Create the phase
phase = dm.Phase(ode_class=DonnerSubODE,
                 transcription=dm.GaussLobatto(num_segments=20, order=3, compressed=False))

# Add the phase to the trajectory, and the trajectory to the model
traj.add_phase('phase0', phase=phase)
p.model.add_subsystem('traj', traj)

#
# Configure the phase
#
phase.set_time_options(units=None, targets=['threat_comp.time'], fix_initial=True, duration_bounds=(0.1, 100))
phase.add_state('x', rate_source='eom_comp.dx_dt', targets=['nav_comp.x'], fix_initial=True, fix_final=True)
phase.add_state('y', rate_source='eom_comp.dy_dt', targets=['nav_comp.y'], fix_initial=True, fix_final=True)

phase.add_design_parameter('v', targets=['eom_comp.v'], opt=True, upper=5, lower=0.1)
phase.add_control('phi', targets=['eom_comp.phi'], units='rad')

phase.add_path_constraint('threat_comp.sub_range', lower=0)

phase.add_objective(name='v', loc='initial')

#
# Set up the driver
#
p.driver = om.pyOptSparseDriver()
p.driver.options['optimizer'] = 'SNOPT'
p.driver.opt_settings['iSumm'] = 6

p.driver.add_recorder(om.SqliteRecorder("donner_sub_solution.sql"))
p.driver.recording_options['includes'] = ['*timeseries*']
p.driver.recording_options['record_objectives'] = True
p.driver.recording_options['record_constraints'] = True
p.driver.recording_options['record_desvars'] = True

p.setup()

#
# Set our initial guesses for the solution
# Hint, one of the following might be giving us trouble.
#
p.set_val('traj.phase0.t_initial', value=0)
p.set_val('traj.phase0.t_duration', value=1.0)
p.set_val('traj.phase0.states:y', value=phase.interpolate(ys=[0, 0], nodes='state_input'))
p.set_val('traj.phase0.states:x', value=phase.interpolate(ys=[-1, 1], nodes='state_input'))
p.set_val('traj.phase0.controls:phi',
          value=phase.interpolate(ys=[80, 100], nodes='control_input'),
          units='deg')
p.set_val('traj.phase0.design_parameters:v', value=2.0)

#
# Solve the problem
#
p.run_driver()
