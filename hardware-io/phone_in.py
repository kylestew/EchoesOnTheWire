import atexit
import CHIP_IO.GPIO as GPIO
import CHIP_IO.Utilities as ioutil
from pythonosc import osc_message_builder
from pythonosc import udp_client
# from pythonosc import dispatcher
# from pythonosc import osc_server
import argparse
import time
import logging

# pin definitions
LED = "XIO-P0"
HANDSET = "XIO-P1"
ROT_ENGAGED = "XIO-P2"
ROT_PULSE = "XIO-P3"

class SpookyPhone(object):
	def __init__(self, udpHost, udpServer):
		self.pulseCount = 0

		# outgoing OSC
		parser = argparse.ArgumentParser()
		parser.add_argument("--ip", default=udpHost, help="The ip of the OSC server")
		parser.add_argument("--port", type=int, default=6448, help="The port the OSC server is listening on")
		args = parser.parse_args()
		self.client = udp_client.SimpleUDPClient(args.ip, args.port)
		logging.debug("Out OSC on " + udpHost)

		# incoming OSC
		# TODO: not implemented - need multi-threading
		# LED can be controlled from external OSC source
		# parser = argparse.ArgumentParser()
		# parser.add_argument("--ip", default=udpServer, help="The ip of the OSC server")
		# parser.add_argument("--port", type=int, default=6558, help="The port the OSC server is listening on")
		# args = parser.parse_args()

		# dispatch = dispatcher.Dispatcher()
		# dispatch.map("/led", self.set_led, "Volume")

		# self.server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatch)
		# logging.debug("Serving on {}".format(self.server.server_address))
		# self.server.serve_forever()

	def run(self):
		# GPIO.toggle_debug()

		try:
			# reset all
			ioutil.unexport_all()
			# GPIO.cleanup()  -- broken?

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

		GPIO.output(LED, GPIO.LOW) # signal process has started successfully

		# busy loop
		while True:
			time.sleep(0.02)

	def stop(self):
		ioutil.unexport_all()
		logging.debug('IO SHUT DOWN')

	# def set_led(unused_addr, args, volume):
	# 	print("[{0}] ~ {1}".format(args[0], volume))
	# def set_led(self, path, tags, args, source):
	# 	# print(tags, args, source)
	# 	if len(args) > 0:
	# 		ledState = args[0]
	# 		GPIO.output(LED, GPIO.HIGH if ledState else GPIO.LOW)

	def off_hook(self, channel):
		# handset off hook == 0 (closed)
		state = GPIO.input(channel)
		GPIO.output(LED, GPIO.LOW if state else GPIO.HIGH)
		logging.debug('handset is: ' + str(state))
		self.client.send_message("/handset", state)

	def rotary_engaged(self, channel):
		if GPIO.input(channel):
			# high = disengaged
			number = self.pulseCount
			if number == 10:
				number = 0
			logging.debug('number dialed: ' + str(number))
			self.client.send_message("/dialed", number)
		else:
			# low = engaged
			self.pulseCount = 0;

	def count_pulse(self, channel):
		self.pulseCount += 1


if __name__ == "__main__":
	logging.basicConfig(filename='/home/chip/io.log',level=logging.DEBUG)
	logging.getLogger().addHandler(logging.StreamHandler())
	logging.debug('PHONE IO STARTING UP...')

	phone = SpookyPhone("127.0.0.1", "127.0.0.1")
	# phone = SpookyPhone("192.168.0.12", "192.168.0.19")

	def exit_handler():
		phone.stop()
	atexit.register(exit_handler)

	phone.run()
