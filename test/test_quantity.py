from simobject import Quantity, Updater, Simulation

import numpy as np
import pytest


def fct(field):
    field.setvalue(field * 2)


sim = Simulation()
u = Updater(func=fct)


def get_defaults():
    a = Quantity(5, info='a', updater=u, constant=True, owner=sim)
    b = Quantity(a)
    return a, b


def test_quantity_copy():
    "test if the memory is not copied by default, but that we can force it"
    a = np.arange(3)
    b = Quantity(a)

    assert b.base is a

    b = Quantity(a, copy=True)

    assert b.base is not a


def test_quantity_updates():
    "test if a quantity updates with above function"
    a = Quantity(5, info='a', updater=u)

    assert a == 5
    a.update()

    assert a == 10


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


def test_quantity_setvalue():
    "run some tests on setvalue"

    a = Quantity(5)
    a.setvalue(6)
    assert a == 6

    a = Quantity([1., 2., 3.])
    a.setvalue(5)
    assert np.all(a == 5)

    a = Quantity(0, constant=True)
    with pytest.raises(TypeError):
        a.setvalue(5)


def test_quantity_repr():
    "check the string representation"
    a = Quantity([5])
    assert a.__repr__() == 'Quantity([5])'

    a = Quantity([1, 2, 3], info='density')
    assert a.__repr__() == 'density\n([1, 2, 3])'

    a = Quantity(0, constant=True)
    assert a.__repr__() == 'Constant Quantity(0)'
