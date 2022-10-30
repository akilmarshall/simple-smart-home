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

```bash
# ssh-manage.py list
```

#### create

```bash
# ssh-manage.py create
```

#### toggle

```bash
# ssh-manage.py toggle
```

#### configure 

When run with only a service name enter an interactive mode to configure the services parameters.

```bash
# ssh-manage.py configure <service-name>
```

## Configuration

Looks for configuration in the following directory by default
- /etc/simple-smart-home
