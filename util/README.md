# Service Management

CLI utilities for managing services.

- list all services:
	- both active and inactive
- create new services:
- remove services:
- toggle (activate/deactivate) services
- configure existing services:
	- more powerful than toggle, able to modifies a services parameters 

## Usage

When run with no sub argument what is the behavior? print the help?

### Sub commands

Most of the functionality is in the subcommands

#### list

list all (label active/inactive).

```bash
$ ssh-manage.py list 
```

list only active

```bash
$ ssh-manage.py list active
```

list only inactive

```bash
$ ssh-manage.py list inactive
```

#### create

```bash
$ ssh-manage.py create <service-name>
```

#### remove

```bash
$ ssh-manage.py remove <service-name>
```

#### toggle

```bash
$ ssh-manage.py toggle <service-name>
```

#### configure 

```bash
$ ssh-manage.py configure <service-name>
```

## Configuration

Looks for configuration in the following directory by default
- /etc/simple-smart-home


## systemd dbus python api

- https://pi3g.com/2020/08/01/enabling-and-disabling-a-systemd-service-in-python-using-dbus/
- https://trstringer.com/python-systemd-dbus/
