import numpy as np
import openmdao.api as om


class NavComp(om.ExplicitComponent):
    def initialize(self):
        self.options.declare('num_nodes', types=int)
        self.options.declare('sub_index', types=int, default=0)
        self.options.declare('sub_origin', types=tuple, default=(0, 0))

    def setup(self):
        nn = self.options['num_nodes']

        self.add_input('y', shape=(nn,), units=None)
        self.add_input('x', shape=(nn,), units=None)
        self.add_output('r_ship', shape=(nn,), units=None)

        ar = np.arange(nn, dtype=int)
        self.declare_partials(of='r_ship', wrt='y', rows=ar, cols=ar)
        self.declare_partials(of='r_ship', wrt='x', rows=ar, cols=ar)

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        y = inputs['y']
        x = inputs['x']
        sub_origin = self.options['sub_origin']

        outputs['r_ship'] = np.sqrt((y - sub_origin[1])**2 + (x - sub_origin[0])**2)

    def compute_partials(self, inputs, partials, discrete_inputs=None):
        y = inputs['y']
        x = inputs['x']
        sub_origin = self.options['sub_origin']

        r_ship = np.sqrt((y - sub_origin[1])**2 + (x - sub_origin[0])**2)

        partials['r_ship', 'y'] = y / r_ship
        partials['r_ship', 'x'] = x / r_ship
