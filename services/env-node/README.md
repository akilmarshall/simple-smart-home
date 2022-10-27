# env-node

Environmental sensing node. 

## back-end

- hardware:
	- esp32 wesmos with built in lcd
	- aht20 temp & humidity sensor:
- software:
	- micropython
	- microdot:
		- web server
		- data at root
		- data described at described at /headers
		- 
## front-end

- script:
	- n-samples.py:
		- alpha prototype 
		- outputs data to STDIO
		- parameters:
			- samples: number of samples
			- delay: delay in seconds between samples

### systemd unit/timer

env-logger

Defined as a python script. Each systemd unit associates with 1 env node.

usage: env-logger.py <ip> <location> [--log path/to/directory]

- <ip> address of the env-node
- <location> of the env node:
	- logs file associate to location, two process given the same location and log directory will write to the same file. 
	- best practice to give a unique location to each process
- <--log>:
	- default /var/env-log/
	- the process (if privileged) will create the directory if it does not exist

#### Installation

- create/install a new service/timer pair for each env-node:
	- several services can use the same unit, (instructions needed)
- it should have a unique location parameter defined in the unit file
- the same location should be appended to the unit's name, suppose location = living-room:
	- env-logger-living-room.service
	- env-logger.py <ip> living-room
- /etc/systemd/system/
- a systemd-timer is used to control sampling frequency
- if the service or timer is edited you must run:
	- # systemctl daemon-reload
