# plotter service

This service plots data files created by services like the env-node service.

## parameters

mandatory:

- data file path
- schedule
	- at what frequency is the data file read and a plot written out 
- out
	- path to directory/file name to write out
	- if directory use default name
	- if path write out directly
optional:
- last _filter_
	- where filter is a string describing a period of time
	- H -> hour
	- D -> day
	- W -> week
	- M -> month
	- Y -> year
	- i.e. --last 3D, plot the last 3 days of data
