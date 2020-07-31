from simobject import Quantity, Updater, Simulation


def fct(field):
    field.setvalue(field * 2)


def get_defaults():
    u = Updater(func=fct)
    sim = Simulation()
    a = Quantity(5, info='a', updater=u, constant=True)
    b = Quantity(a)

    sim.addQuantity('a', a, info='newinfo')
    return sim, a, b, u


def test_simulation_update():
    sim, a, b, u = get_defaults()

    # test if adding a constant quantity keeps it constant
    sim.addQuantity('a', a)

    assert sim.a.constant

    # test if that can be overwritten

    sim.addQuantity('a', a, constant=False)

    assert not sim.a.constant

    assert a == 5
    sim.update()
    assert a == 10


def test_assign_quantity():
    "check if assigning quantities works as desired"

    sim = Simulation()
    a = Quantity(5)
    b = Quantity(6)
    sim.a = a
    assert sim.a == a

    sim.a = b
    assert sim.a == b

    sim.a = 7
    assert sim.a == 7


def test_sim_add_quantity_is_different():
    "We added the a quantity to the simulation, should now be different object"
    sim, a, b, u = get_defaults()
    assert id(sim.a) != id(a)


def test_sim_add_quantity_overwrite_info():
    "This also overwrote the info"
    sim, a, b, u = get_defaults()
    assert sim.a.info == 'newinfo'


def test_sim_add_quantity_keep_info():
    "without keyword, does it keep the info"
    sim, a, b, u = get_defaults()
    sim.addQuantity('a', a)
    assert sim.a.info == 'a'


def test_sim_add_quantity_old_info_stays():
    "the old `a` should still have it's original info"
    sim, a, b, u = get_defaults()
    assert a.info == 'a'


def test_sim_add_quantity_updates_owner():
    "the owner of `sim.a` is now `sim`"
    sim, a, b, u = get_defaults()
    assert id(sim.a.owner) == id(sim)


def test_sim_add_quantity_keeps_owner():
    "the owner of the original a is still none"
    sim, a, b, u = get_defaults()
    assert a.owner is None


def test_sim_add_quantity_updater_identical():
    "the updater object is the same"
    sim, a, b, u = get_defaults()
    assert a.updater is sim.a.updater


def test_sim_add_quantity_overwrite_updater():
    "we add `a` again, but pass a new Updater"
    sim, a, b, u = get_defaults()
    u2 = Updater(fct)
    sim.addQuantity('a', a, updater=u2)
    assert a.updater is not sim.a.updater
