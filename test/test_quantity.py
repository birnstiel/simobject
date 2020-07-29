from simobject import Quantity, Updater, Simulation


def fct(field):
    field.setvalue(field * 2)


sim = Simulation()
u = Updater(func=fct)


def get_defaults():
    a = Quantity(5, info='a', updater=u, constant=True, owner=sim)
    b = Quantity(a)
    return a, b


def test_quantity_from_quantity_is_different():
    # Check that `b` is a different object from `a`
    a, b = get_defaults()
    assert id(a) != id(b)


def test_quantity_from_quantity_keeps_updater():
    "Check that the updater is the same"
    a, b = get_defaults()
    assert id(b.updater) == id(a.updater)


def test_quantity_from_quantity_keeps_owner():
    "Check that the owner is the same"
    a, b = get_defaults()
    assert id(b.owner) == id(a.owner)


def test_quantity_from_quantity_keeps_info():
    "Check that the info is the same"
    a, b = get_defaults()
    assert id(b.info) == id(a.info)


def test_quantity_from_quantity_keeps_constant():
    "check that the constant is the same"
    a, b = get_defaults()
    assert id(b.constant) == id(a.constant)


def test_quantity_calc_keeps_owner():
    "if we calculate with a quantity, does it keep owner"
    a, b = get_defaults()
    c = a / 100.
    assert c.owner is sim


def test_quantity_calc_keeps_info():
    "if we calculate with a quantity, does it keep its info"
    a, b = get_defaults()
    c = a / 100.
    assert a.info == c.info


def test_quantity_calc_keeps_constant():
    "A Quantity derived from a constant Quantity is still a constant"
    a = Quantity([5], constant=True)
    b = a / 2
    assert b.constant


def test_quantity_overwrite_constant():
    "can we overwrite the constant flag"
    a = Quantity([5, 6, 7], constant=True)
    b = Quantity(a / 2, constant=False)
    assert not b.constant


def test_quantity_default_non_constant():
    "By default a Quantity is not constant"
    e = Quantity(5)
    assert e.constant is False
