from pyxdsm.XDSM import XDSM

#
opt = 'Optimization'
solver = 'MDA'
comp = 'Analysis'
group = 'Metamodel'
func = 'Function'

x = XDSM()

x.add_system('EOM', comp, r'EOM')
x.add_system('nav', comp, r'nav')
x.add_system('threat', func, r'threat')


# x.connect('opt', 'EOM', r'x, z')
# x.connect('opt', 'nav', r'z')
# x.connect('opt', 'F', r'x, z')
# x.connect('solver', 'EOM', r'y_2')
# x.connect('solver', 'nav', r'y_1')
x.connect('nav', 'threat', r'r_{ship}')
# x.connect('solver', 'F', r'y_1, y_2')
# x.connect('solver', 'G', r'y_1, y_2')

x.add_input('EOM', r'v, \phi')
x.add_input('nav', r'x, y')
x.add_input('threat', r'time')

# x.add_output('opt', r'x^*, z^*', side='left')
x.add_output('EOM', r'\dot{x}, \dot{y}', side='right')
x.add_output('threat', r'range_{sub}', side='right')
x.write('donner_sub_ode_xdsm')
