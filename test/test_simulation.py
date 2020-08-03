from simobject import Quantity, Simulation, DataUpdater

import numpy as np
import pytest


def test_simulation():
    """run a toy simulation

    set up a dummy simulation to check if the values update as we expect.
    """
    sim = Simulation()

    yinit = 2.0
    zinit = 3.0

    sim.addQuantity('nx', Quantity(100, 'size of x', constant=True))
    sim.addQuantity('x', Quantity(np.linspace(0, 1, sim.nx), info='x grid', constant=True))
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

    # check if the update order properties work as desired

    order = ['nx', 'x', 'y', 'z', 'time', 'dt']
    new_order = order[::-1]

    for _order in [sim.systole_order, sim.update_order, sim.diastole_order]:
        assert _order == order

    sim.systole_order = new_order
    sim.update_order = new_order
    sim.diastole_order = new_order

    for _order in [sim.systole_order, sim.update_order, sim.diastole_order]:
        assert _order == new_order

    # now check that things after the update are as expected

    sim.update()

    # check if time and values were updated

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


def test_simulation_repr():
    "test the string representation"
    sim = Simulation()

    sim.addQuantity('a', Quantity([1, 2, 3], info='length'))
    sim.addQuantity('dust surface density', Quantity([1, 2, 3], info='length', constant=True))
    sim.addQuantity('b', Quantity([1, 2, 3], info='length', constant=True))
    sim.addQuantity('_c', Quantity([1, 2, 3], info='length', constant=True))

    sim._quantities['d'] = 5

    string = 'Simulation\n\n           Quantity: a            (length)\n    Const. Quantity: b            (length)\n           int    : d           \n    Const. Quantity: dust surf... (length)\n'

    assert sim.__repr__() == string

    assert len(sim.__dir__()) == 53


def test_data_object():
    sim = Simulation()

    with pytest.raises(AttributeError):
        sim.data = {'a': 5}


def test_assigning_faulty_list():
    sim = Simulation()

    with pytest.raises(TypeError):
        sim.update_order = ['a', 5]

    with pytest.raises(TypeError):
        sim.update_order = 5


def test_several_steps():
    sim = Simulation()
    sim.addQuantity('time', Quantity(0, 'simulation time'))
    sim.addQuantity('dt', Quantity(1, 'time step'))

    def timeupdate(time):
        time += time.owner.dt

    sim.time.updater = timeupdate

    sim.diastoler = DataUpdater(['time'])

    sim.update()
    sim.update()
    sim.update()
    sim.update()

    assert sim.time == 4
    assert np.all(sim.data['time'][:, 0] == [1, 2, 3, 4])
