import dbus


bus = dbus.SystemBus()
systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')

def disable(unit:str):
    """Disable unit file. """
    manager.DisableUnitFiles([unit], False)
    manager.Reload()

def enable(unit:str):
    """Enable and start unit. """
    manager.EnableUnitFiles([unit], False, True)
    manager.Reload()
    manager.RestartUnit(unit, 'fail')

def status(unit:str):
    """Check the status of a unit file. [disabled, enabled]. """
    return manager.GetUnitFileState(unit)
