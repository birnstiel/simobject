from simobject import HeartbeatObject, Updater

import pytest


def test_heartbeatobject():
    h = HeartbeatObject()

    def f(obj):
        return

    u = Updater(func=f)

    h.systoler = u
    h.updater = u
    h.diastoler = u

    assert h.systoler is u
    assert h.updater is u
    assert h.diastoler is u

    h.systole()
    h.update()
    h.diastole()

    with pytest.raises(TypeError):
        h.updater = 5
