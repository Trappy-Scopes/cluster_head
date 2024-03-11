import libtmux


from node import AbstractNetDevice

class SSHNetDevice(AbstractNetDevice):

	##1
	@abstractmethod
	def __init__(self, name, addr, username=None, password=None, connect=False):
		

		self.hostname = name
		self.username = username
		self.password = password
		self.addr = addr

		self.server = None

		# Create a new session or attach to an existing one
		self.session_name = self.hostname
		self.session = None

		if connect:
			self.connect(username=self.username, password=self.password)


	##2
	@abstractmethod
	def __del__(self):
		pass

	##3
	@abstractmethod
	def connect(self, username=None, password=None):
		self.session = self.server.find_where({'session_name': session_name})
		
		# Attach to the session
		#if self.session:
		self.server = libtmux.Server(hostname=self.hostname, 
									 user=self.username, 
									 ssh_password=self.password)
		self.session.attach_session()
		#else:
		#print("Couldn't find session!")

	##4
	@abstractmethod
	def disconnect(self):
		pass

	##5
	@abstractmethod
	def is_connected(self):
		if self.server:
			return self.server.has_session
		else:
			return False

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


