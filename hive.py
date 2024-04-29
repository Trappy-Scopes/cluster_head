import ipaddress


from rich import print
from rich.panel import Panel


from node import Node

class Hive:
	"""
	Creates a collection of devices and optionally emits them in the global space.
	"""

	def __init__(self, name, nodelist):
		"""
		initaliser. Trivial.
	
		Two kinds of devices:
			|- Linux systems -- SSH (parmiko/libmux)
			|- Micropython device - Micropython subsystem - webrepl - 

		"""
		self.name = name

		self.all_devices = yaml.load("all_devices_iplist.yaml")
		self.inv_map = {v: k for k, v in self.all_devices.items()}
		
		self.requested = nodelist
		self.nodes = {}
		self.rejected = []


		self.assemble()

	def assemble():
		"""
		Assembles the given set of devices into Node devices.
		"""
		for device in self.requested:

			# Resolve device name and ip address
			if ipaddress.ip_address(device):
				ip = device
				device = self.inv_map[device]
			else:
				ip = self.all_devices[device]

			# Attempt lock
			hlock, node = self.hivelock(device, ip)
			if hlock == True:
				self.nodes[device] = node
				print(f"[red]Hive {self.name}[default]: Node acquired: [cyan]{device} :: {ip} !")
			else:
				print(f"[red]Hive {self.name}[default]: [red]Node request rejected: [cyan]{device} :: {ip} !")
				self.rejected.append(device)

			print(Panel(f"{len(self.nodes)}/{len(self.requested)}", title=f"Hive `{self.name}` Quorum"), align="center")

	
	def hivelock(device, ip, force=False):

		## Assume linux device for now : TODO - specialise for micropython device.
		node = Node(device, ip, password="trappyscope", connect=True)
		acq = True
		if node.is_connected():

			## Force
			if force:
				node.exec("rm .hivelock")

			## 
			response = node.exec("ls .hivelock")
			if not "No such file or directory" in response:
				acq = False
		else:
			print(f"Hive.hivelock: [red] {device} Node connection failure!")
			acq = False

		if acq:
			return True, node
		else:
			node.disconnect()
			return False, None



	def emit_devices(self):
		"""
		Adds all available devices to the global variables.
		"""
		for device in self.nodes:
			golbals()[device] = self.nodes[device]