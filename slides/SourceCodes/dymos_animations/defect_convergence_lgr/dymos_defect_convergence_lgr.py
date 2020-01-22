import numpy as np
import matplotlib.pyplot as plt

import openmdao.api as om


def make_defect_convergence_animation():

    cr = om.CaseReader('min_time_climb_solution_radau-ps.sql')

    # for key in cr.system_metadata['traj.phases.phase0']:
    #     print(key)
    #
    # print(cr.system_metadata['traj.phases.phase0']['component_options']['transcription'])
    # exit(0)

    transcription = cr.system_metadata['traj.phases.phase0']['component_options']['transcription']
    gd = transcription.grid_data
    idxs_disc = gd.subset_node_indices['state_disc']
    idxs_col = gd.subset_node_indices['col']

    state = 'gam'

    for i, case_name in enumerate(cr.list_cases()):
        fig, ax = plt.subplots(1, 1, figsize=(8, 3.5))
        ax.set_xlim(-50, 450)
        ax.set_ylim(-20, 50)
        plt.text(350, 30, f'iteration: {i}')

        case = cr.get_case(case_name)
        case.list_outputs(out_stream=None)

        # Plot the high-density interpolated solution
        ax.plot(case.get_val('traj.phase0.timeseries2.time'),
                case.get_val(f'traj.phase0.timeseries2.states:{state}', units='deg'),
                color='lightgray',
                linestyle=':')

        # Plot the discretization nodes
        ax.plot(case.get_val('traj.phase0.timeseries.time')[idxs_disc, ...],
                case.get_val(f'traj.phase0.timeseries.states:{state}', units='deg')[idxs_disc, ...], 'ko')

        # Plot the collocation nodes
        ax.plot(case.get_val('traj.phase0.timeseries.time')[idxs_col, ...],
                case.get_val(f'traj.phase0.timeseries.states:{state}', units='deg')[idxs_col, ...], 'k^')

        # Plot the evaluated state rates
        dgam_dt = case.get_val(f'traj.phase0.timeseries.state_rates:{state}', units='deg/s')[idxs_col, ...].ravel()

        dt = np.ones_like(dgam_dt)
        s = 3
        angles = 'xy'
        units='inches'
        scale_units='inches'
        w = 0.03

        ax.quiver(case.get_val('traj.phase0.timeseries.time')[idxs_col, ...],
                  case.get_val(f'traj.phase0.timeseries.states:{state}', units='deg')[idxs_col, ...],
                  dt, dgam_dt,
                  units=units, angles=angles, scale=s,
                  scale_units=scale_units, color='r', width=w)

        # Plot the interpolated state rates
        dgam_dt = case.get_val(f'traj.phase0.state_interp.staterate_col:{state}', units='deg/s').ravel()

        ax.quiver(case.get_val('traj.phase0.timeseries.time')[idxs_col, ...],
                  case.get_val(f'traj.phase0.timeseries.states:{state}', units='deg')[idxs_col, ...],
                  dt, dgam_dt,
                  units=units, angles=angles, scale=s,
                  scale_units=scale_units, color='b', width=w)

        plt.savefig(f'frames/frame_{i:02d}.pdf')


    # case.list_outputs()
    #
    #
    # fig, ax = plt.subplots(1, 1)



if __name__ == '__main__':
    make_defect_convergence_animation()
