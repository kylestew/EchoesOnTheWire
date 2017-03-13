import atexit
import CHIP_IO.GPIO as GPIO
from OSC import OSCClient, OSCMessage, OSCServer
import time
import logging

import socket
socket.gethostbyname(socket.gethostname())

# pin definitions
LED = "XIO-P0"
HANDSET = "XIO-P1"
ROT_ENGAGED = "XIO-P2"
ROT_PULSE = "XIO-P3"

class SpookyPhone(object):
	def __init__(self, udpHost, udpServer):
		self.client = OSCClient()
		self.client.connect((udpHost, 6448))
		self.pulseCount = 0

		# LED can be controlled from external OSC source
		self.server = OSCServer((udpServer, 6558))
		self.server.addMsgHandler("/led", self.set_led)

	def run(self):
		# GPIO.toggle_debug()

		try:
			# led
			GPIO.setup(LED, GPIO.OUT)
			GPIO.output(LED, GPIO.LOW)

			# handset
			GPIO.setup(HANDSET, GPIO.IN, pull_up_down=GPIO.PUD_UP, initial=1)
			GPIO.add_event_detect(HANDSET, GPIO.BOTH, self.off_hook)

			# rotary dial
			GPIO.setup(ROT_ENGAGED, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			GPIO.add_event_detect(ROT_ENGAGED, GPIO.BOTH, self.rotary_engaged)
			GPIO.setup(ROT_PULSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			GPIO.add_event_detect(ROT_PULSE, GPIO.FALLING, self.count_pulse)
		except Exception as e:
		    logging.exception("exception encountered")

		# busy loop
		while True:
			self.server.handle_request()
			time.sleep(0.02)
			logging.debug("ping")
			time.sleep(1)

	def stop(self):
		print("shutting down IO")
		logging.debug('SHUTTING DOWN IO')
		GPIO.cleanup()

	def set_led(self, path, tags, args, source):
		print(tags, args, source)
		if len(args) > 0:
			ledState = args[0]
			GPIO.output(LED, GPIO.HIGH if ledState else GPIO.LOW)

	def off_hook(self, channel):
		# handset off hook == 0 (closed)
		state = GPIO.input(channel)
		print("handset is:", state)
		logging.debug('handset is:', state)
		msg = OSCMessage("/handset")
		msg.append(GPIO.input(channel))
		self.client.send(msg)

	def rotary_engaged(self, channel):
		if GPIO.input(channel):
			# high = disengaged
			print("rotary dis-engaged")
			number = self.pulseCount
			if number == 10:
				number = 0
			print("number dialed:", number)
			logging.debug('number dialed', number)
			msg = OSCMessage("/dialed")
			msg.append(number)
			self.client.send(msg)
		else:
			# low = engaged
			print("rotary engaged")
			self.pulseCount = 0;

	def count_pulse(self, channel):
		self.pulseCount += 1


if __name__ == "__main__":
	logging.basicConfig(filename='/home/chip/io.log',level=logging.DEBUG)
	logging.debug('PHONE IO STARTING UP...')
	phone = SpookyPhone("localhost", "localhost")
	def exit_handler():
		phone.stop()
	atexit.register(exit_handler)
	phone.run()
