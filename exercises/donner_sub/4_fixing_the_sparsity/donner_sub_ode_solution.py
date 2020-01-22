import openmdao.api as om

from nav_comp import NavComp
from ship_eom_comp import ShipEOMComp

class DonnerSubODE(om.Group):

    def initialize(self):
        self.options.declare('num_nodes', types=int)

    def setup(self):
        nn = self.options['num_nodes']

        self.add_subsystem('eom_comp', ShipEOMComp(num_nodes=nn))
        self.add_subsystem('nav_comp', NavComp(num_nodes=nn))

        #
        # Inform OpenMDAO that our vectorized ExecComp has a diagonal sparsity pattern
        #
        self.add_subsystem('threat_comp', om.ExecComp('sub_range = r_ship2 - time**2',
                                                      sub_range={'shape': (nn,)},
                                                      r_ship2={'shape': (nn,)},
                                                      time={'shape': (nn,)},
                                                      has_diag_partials=True))

        self.connect('nav_comp.r_ship2', 'threat_comp.r_ship2')


