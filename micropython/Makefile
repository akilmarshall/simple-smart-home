reset: /dev/ttyUSB0
	esptool.py --port /dev/ttyUSB0 -b 115200 erase_flash
	esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 /home/akil/Desktop/micropython/firmware/esp32-20220618-v1.19.1.bin

clear: /dev/ttyUSB0
	rshell -p /dev/ttyUSB0 -b 115200 rm /pyboard/*

web: /dev/ttyUSB0
	rshell -p /dev/ttyUSB0 -b 115200 cp /home/akil/Desktop/micropython/web-sensor/* /pyboard
	@echo 'Do a hard reset'

update: /dev/ttyUSB0
	rshell -p /dev/ttyUSB0 -b 115200 cp /home/akil/Desktop/micropython/web-sensor/boot.py /pyboard
	@echo 'Do a hard reset'

repl: /dev/ttyUSB0
	rshell -p /dev/ttyUSB0 -b 115200 repl

connect: /dev/ttyUSB0
	rshell -p /dev/ttyUSB0

