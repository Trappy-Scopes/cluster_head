from abc import abstractmethod


class AbstractNetDevice:

	##1
	@abstractmethod
	def __init__(self, name, addr, username=None, password=None, connect=False):
		pass

	##2
	@abstractmethod
	def __del__(self):
		pass

	##3
	@abstractmethod
	def connect(self, login=None, password=None):
		pass

	##4
	@abstractmethod
	def disconnect(self):
		pass

	##5
	@abstractmethod
	def is_connected(self):
		pass

	##6
	@abstractmethod
	def defshell(self, *args, **kwargs):
		pass

	##7
	@abstractmethod
	def exec(self, *args, **kwargs):
		pass

	##8
	@abstractmethod
	def __shell__(self, *args, **kwargs):
		pass

	##9
	@abstractmethod
	def __get_item__(self, *args, **kwargs):
		pass

	##10
	@abstractmethod
	def __call__(self, *args, **kwargs):
		pass

	##11
	@abstractmethod
	def deploy(self, file):
		pass

	##12
	@abstractmethod
	def SubDevice(self, devname):
		pass

	##13
	@abstractmethod
	def status(self):
		pass

	##14
	@abstractmethod
	def __repr__(self):
		pass

	##15
	@abstractmethod
	def cartoon(self):
		pass


