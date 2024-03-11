from colorama import Fore



class Hive:
	"""
	Creates a roll of devices and optionally emits them in the global space.
	"""

	def __init__(self):
		"""
		initaliser. Trivial.
	
		Two kinds of devices:
			|- Rpi - Linux systems -- SSH (parmiko/libmux)
			|- RPi pico device - Micropython subsystem - webrepl - 

		"""
		self.devlist = {}
		self.roll = {}

		self.all_devices = yaml.load("all_devices_iplist.yaml")

	def assemble(device_list):
		"""
		Assembles the given set of ip addresses into Node devices.
		"""
		for device in device_list:
			if device in self.all_devices:
				self.roll[device] = Node(device, all_devices_iplist[device])
			else:
				print(f"{Fore.RED}Device not found: {device}!{Fore.RESET}")
		print(f"{Fore.BLUE} Total device init: {len(self.roll)} .")

	def emit_devices(self):
		"""
		Adds all available devices to the global variables.
		"""
		for device in self.roll:
			golbals()[device] = self.roll[device]