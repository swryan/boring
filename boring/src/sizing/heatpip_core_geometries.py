from __future__ import absolute_import
import numpy as np
from math import pi

import openmdao.api as om

class CoreGeometries(om.ExplicitComponent):

    def initialize(self):
        self.options.declare('num_nodes', types=int)

    def setup(self):
        nn=self.options['num_nodes']

        self.add_input('D_od', 1, units='m', desc='')
        self.add_input('t_w', 1, units='m', desc='')
        self.add_input('D_v', 1, units='m', desc='')
        self.add_input('L_cond', 1, units='m', desc='')
        self.add_input('L_evap', 1, units='m', desc='')

        self.add_output('A_w', 1, units='m', desc='')
        self.add_output('A_wk', 1, units='m', desc='')
        self.add_output('A_interc', 1, units='m', desc='')
        self.add_output('A_intere', 1, units='m', desc='')

        self.declare_partials('A_w', ['D_od', 't_w'])
        self.declare_partials('A_wk', ['D_od', 't_w', 'D_v'])
        self.declare_partials('A_interc', ['D_v', 'L_cond'])
        self.declare_partials('A_intere', ['L_evap'])

    def compute(self, inputs, outputs):

        D_od = inputs['D_od']
        t_w = inputs['t_w']
        D_v = inputs['D_v']
        L_cond = inputs['L_cond']
        L_evap = inputs['L_evap']


        outputs['A_w'] =  np.pi*((D_od/2)**2-(D_od/2-t_w)**2)
        outputs['A_wk'] = np.pi*((D_od/2-t_w)**2-(D_v/2)**2)
        outputs['A_interc'] = np.pi*D_v*L_cond
        outputs['A_intere'] = np.pi*D_v*L_evap

    def compute_partials(self, inputs, J):
        D_od = inputs['D_od']
        t_w = inputs['t_w']
        D_v = inputs['D_v']
        L_cond = inputs['L_cond']
        L_evap = inputs['L_evap']

        J['A_w', 'D_od'] = np.pi*D_od*(0.5 + t_w)
        J['A_w', 't_w'] = -np.pi*2*(D_od/2 - t_w)
        J['A_wk', 'D_od'] = 