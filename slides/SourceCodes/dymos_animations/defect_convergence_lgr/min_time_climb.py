import openmdao.api as om
import dymos as dm

from dymos.examples.min_time_climb.min_time_climb_ode import MinTimeClimbODE


def min_time_climb(optimizer='SLSQP', num_seg=3, transcription='gauss-lobatto', transcription_order=3):

    p = om.Problem(model=om.Group())

    p.driver = om.pyOptSparseDriver()
    p.driver.options['optimizer'] = optimizer
    p.driver.declare_coloring()

    p.driver.add_recorder(om.SqliteRecorder(f'min_time_climb_solution_{transcription}.sql'))
    p.driver.recording_options['includes'] = ['*']
    p.driver.recording_options['record_objectives'] = True
    p.driver.recording_options['record_constraints'] = True
    p.driver.recording_options['record_desvars'] = True

    if optimizer == 'SNOPT':
        p.driver.opt_settings['Major iterations limit'] = 1000
        p.driver.opt_settings['iSumm'] = 6
        p.driver.opt_settings['Major feasibility tolerance'] = 1.0E-6
        p.driver.opt_settings['Major optimality tolerance'] = 1.0E-6
        p.driver.opt_settings['Function precision'] = 1.0E-12
        p.driver.opt_settings['Linesearch tolerance'] = 0.1
        p.driver.opt_settings['Major step limit'] = 0.5

    t = {'gauss-lobatto': dm.GaussLobatto(num_segments=num_seg, order=transcription_order),
         'radau-ps': dm.Radau(num_segments=num_seg, order=transcription_order),
         'runge-kutta': dm.RungeKutta(num_segments=num_seg)}

    traj = dm.Trajectory()

    phase = dm.Phase(ode_class=MinTimeClimbODE, transcription=t[transcription])
    traj.add_phase('phase0', phase)

    p.model.add_subsystem('traj', traj)

    phase.set_time_options(fix_initial=True, duration_bounds=(50, 400),
                           duration_ref=100.0)

    phase.add_state('r', fix_initial=True, lower=0, upper=1.0E6,
                    ref=1.0E3, defect_ref=1.0E3, units='m',
                    rate_source='flight_dynamics.r_dot')

    phase.add_state('h', fix_initial=True, lower=0, upper=20000.0,
                    ref=1.0E2, defect_ref=1.0E2, units='m',
                    rate_source='flight_dynamics.h_dot', targets=['h'])

    phase.add_state('v', fix_initial=True, lower=10.0,
                    ref=1.0E2, defect_ref=1.0E2, units='m/s',
                    rate_source='flight_dynamics.v_dot', targets=['v'])

    phase.add_state('gam', fix_initial=True, lower=-1.5, upper=1.5,
                    ref=1.0, defect_ref=1.0, units='rad',
                    rate_source='flight_dynamics.gam_dot', targets=['gam'])

    phase.add_state('m', fix_initial=True, lower=10.0, upper=1.0E5,
                    ref=1.0E3, defect_ref=1.0E3, units='kg',
                    rate_source='prop.m_dot', targets=['m'])

    phase.add_control('alpha', units='deg', lower=-8.0, upper=8.0, scaler=1.0,
                      rate_continuity=True, rate_continuity_scaler=100.0,
                      rate2_continuity=False, targets=['alpha'])

    phase.add_design_parameter('S', val=49.2386, units='m**2', opt=False, targets=['S'])
    phase.add_design_parameter('Isp', val=1600.0, units='s', opt=False, targets=['Isp'])
    phase.add_design_parameter('throttle', val=1.0, opt=False, targets=['throttle'])

    phase.add_boundary_constraint('h', loc='final', equals=20000, scaler=1.0E-3, units='m')
    phase.add_boundary_constraint('aero.mach', loc='final', equals=1.0)
    phase.add_boundary_constraint('gam', loc='final', equals=0.0, units='rad')

    phase.add_path_constraint(name='h', lower=100.0, upper=20000, ref=20000)
    phase.add_path_constraint(name='aero.mach', lower=0.1, upper=1.8)

    phase.add_timeseries('timeseries2', transcription=dm.GaussLobatto(num_segments=50, order=3))

    # Minimize time at the end of the phase
    phase.add_objective('time', loc='final', ref=1.0)

    p.model.linear_solver = om.DirectSolver()

    p.setup()

    p['traj.phase0.t_initial'] = 0.0
    p['traj.phase0.t_duration'] = 300.0

    p['traj.phase0.states:r'] = phase.interpolate(ys=[0.0, 111319.54], nodes='state_input')
    p['traj.phase0.states:h'] = phase.interpolate(ys=[100.0, 20000.0], nodes='state_input')
    p['traj.phase0.states:v'] = phase.interpolate(ys=[135.964, 283.159], nodes='state_input')
    p['traj.phase0.states:gam'] = phase.interpolate(ys=[0.0, 0.0], nodes='state_input')
    p['traj.phase0.states:m'] = phase.interpolate(ys=[19030.468, 16841.431], nodes='state_input')
    p['traj.phase0.controls:alpha'] = phase.interpolate(ys=[0.0, 0.0], nodes='control_input')

    p.run_driver()

    traj.simulate(record_file=f'min_time_climb_simulation_{transcription}.sql')

    return p


if __name__ == '__main__':
    min_time_climb(optimizer='SNOPT', num_seg=10, transcription='radau-ps', transcription_order=3)
