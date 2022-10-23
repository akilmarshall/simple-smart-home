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
	- TODO implement sensor:
		- currently outputs fake data upon GET request
	

## front-end

- script:
	- n-samples.py:
		- currently outputs data to STDIO
