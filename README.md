# simple-smart-home

This is a specification for a "Smart Home" consisting of services over a LAN/WLAN.

A service is composed of one or more edge devices with a front end.
Edge devices may be utilized by one or more services, but a service will only have one front end.
Front end's are the primary means of interacting with edge devices however there may be additional local I/O on the edge device

- LCD read outs
- Kill switches
- etc.

It is up to the definition of a specific service to specify these additional non standard interactions.

%% album of architectures https://imgur.com/a/JgK4Pwy
<p align="center">
	<img src=https://imgur.com/EJC8GPN.png />
</p>

## Edge Device

Edge devices either serve data and/or interact with the real world.
- serve environmental data
- control a plug, motor, etc.
- self contained
- communicates over HTTP

## Front End

The front end is where the "business logic" is implemented and the user is offered an appropriate interface to realize the necessary control over the service.

- systemd as a front end:
	- minimal user interface 
	- one time actions:
		- systemd unit:
			- simple 
			- one-shot
	- regularly scheduled actions:
		- systemd unit
		- systemd timer
- script as a front end:
	- moderate user interface 
	- short lived processes offers direct control over:
		- starting
		- stopping
		- parameters
- web server as a front end:
	- maximal user interface 
	- more powerful than the systemd or script front ends
	- can offer the functionality of one or more systemd and script frontend via web control
	- easy to use

## Potential Hardware

Edge devices hosts:
- esp32
- raspberry pi
- single board computers

Frontend hosts:

Ideally able to run a linux operating system:
- SBC (single board computer)
- can be low power, more ram offers more performance
- [odroid 8gb](https://www.ebay.com/itm/284762094624?hash=item424d24bc20:g:BggAAOSwbThiVYQs&amdata=enc%3AAQAHAAAAoFrsWC4UKDlvy8McvwkGCw8OHlPJtWY%2BdDBvkkHftCG0VkjF3t6GZMMmzJfUhCtu8As8I1bSMKH1ycog8eRaPke6gJZy5rAgLf5rOBW0Luy4OIArb%2FqjcmiTIPbITeNq2ikKgfLwsPD1926bplJuCehq1SFvmtfE2GDZNDAEugPymHm%2BOr%2FzvFvRLhSYEoRLZwZ4xw697a8qKZZC4ZstEF4%3D%7Ctkp%3ABk9SR9yXtZnlYA)
