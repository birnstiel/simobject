from simobject import Quantity, Simulation, DataUpdater

import numpy as np


def test_simulation():
    """run a toy simulation

    set up a dummy simulation to check if the values update as we expect.
    """
    sim = Simulation()

    yinit = 2.0
    zinit = 3.0

    sim.addQuantity('nx', Quantity(100, 'size of x', constant=True))
    sim.addQuantity('x', Quantity(np.linspace(0, 1, sim.nx), info='x grid'))
    sim.addQuantity('y', Quantity(yinit * np.ones_like(sim.x), info='y value', constant=False))
    sim.addQuantity('z', Quantity(zinit * np.ones_like(sim.x), info='z value', constant=False))

    sim.addQuantity('time', Quantity(0.0, 'simulation time [s]'))
    sim.addQuantity('dt', Quantity(1.0, 'time step [s]'))

    def timeupdate(time):
        time += time.owner.dt

    def dummyupdate(y):
        y *= 2

    sim.time.updater = timeupdate
    sim.y.updater = dummyupdate
    sim.z.updater = dummyupdate

    sim.diastoler = DataUpdater(['time', 'y', 'z'])

    for a, b in zip(['nx', 'x', 'y', 'z', 'time', 'dt'], sim.diastole_order):
        assert a == b

    sim.update()

    # check if timem and values were updated

    assert sim.time == sim.dt
    assert sim.y[0] == yinit * 2.0
    assert sim.z[1] == zinit * 2.0

    assert sim.data['y'].shape[0] == 1
    assert sim.data['y'].shape[1] == sim.nx

    sim.update()

    assert sim.time == 2.0 * sim.dt
    assert sim.y[-2] == yinit * 4.0
    assert sim.z[-1] == zinit * 4.0

    assert sim.data['z'].shape[0] == 2
    assert sim.data['z'].shape[1] == sim.nx
