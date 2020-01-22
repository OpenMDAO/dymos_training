import numpy as np
import openmdao.api as om


class ShipEOMComp(om.ExplicitComponent):

    def initialize(self):
        self.options.declare('num_nodes', types=int)

    def setup(self):
        nn = self.options['num_nodes']

        self.add_input('v', shape=(nn,), units=None)
        self.add_input('phi', shape=(nn,), units='rad')
        self.add_output('dx_dt', shape=(nn,), units=None)
        self.add_output('dy_dt', shape=(nn,), units=None)

        ar = np.arange(nn, dtype=int)
        self.declare_partials(of='dx_dt', wrt='v', rows=ar, cols=ar)
        self.declare_partials(of='dx_dt', wrt='phi', rows=ar, cols=ar)
        self.declare_partials(of='dy_dt', wrt='v', rows=ar, cols=ar)
        self.declare_partials(of='dy_dt', wrt='phi', rows=ar, cols=ar)

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        v = inputs['v']
        phi = inputs['phi']

        outputs['dx_dt'] = v * np.sin(phi)
        outputs['dy_dt'] = v * np.cos(phi)

    def compute_partials(self, inputs, partials, discrete_inputs=None):
        v = inputs['v']
        phi = inputs['phi']
        partials['dx_dt', 'v'] = np.sin(phi)
        partials['dx_dt', 'phi'] = v * np.cos(phi)
        partials['dy_dt', 'v'] = np.cos(phi)
        partials['dy_dt', 'phi'] = -v * np.sin(phi)


