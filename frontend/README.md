# Front End

This is the Front End software for the simple smart home.
Front End software is comprised of a:

- command-line interface
- web interface

The CLI and web interfaces are built using a python package simple_smart_home.

## simple_smart_home

### services file

The installed services are kept track of in the services file (default: /etc/simple-smart-home.services).
This is a hierarchical file (ini or toml) that keeps track of the names and and parameters of installed services.
This file is read and written to and acts as a class roster for services, it should only be interacted with via the api exposed in the simple_smart_home module.

## CLI

Implemented as a script using argparse, built using the simple_smart_home package to control/manage simple smart home services.

- list all services:
	- both active and inactive
- create new services:
- remove services:
- toggle (activate/deactivate) services
- configure existing services:
	- more powerful than toggle, able to modifies a services parameters 

### Usage

When run with no sub argument what is the behavior? print the help?

#### list

list all (label active/inactive).

```bash
$ ssh-manage.py list 
```

#### create

```bash
$ ssh-manage.py create-env <ip> <location> <log directory> <minute interval>
```

#### remove

```bash
$ ssh-manage.py remove <service-name>
```

#### toggle

```bash
$ ssh-manage.py toggle <service-name>
```

## Web Interface

Implemented using hug to offer a web interface for simple smart home services. Consumes the simple_smart_home package to offer control/management of simple smart home services.
