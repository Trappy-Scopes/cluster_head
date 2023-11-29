import paramiko
from colorama import Fore, Style
import shlex
import socket
import time

class Node:
	"""
	Represents a node device that can execute commands remotely.
	"""

	def __init__(self, name, ip, password, connect=True):

		self.ssh = paramiko.SSHClient()
		self.username = "trappyscope"
		self.ip = ip
		self.name = name

		hostname = socket.gethostname()
		self.headnode_ip = socket.gethostbyname(hostname)
		self.channel = None
		self.is_connected = False
		if connect:
			self.connect(password)
		

	def __del__(self):
		if self.is_connected:
			self.disconnect()

	def connect(self, password):
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			# Connect to the Raspberry Pi
			self.ssh.connect(self.ip, username=self.username, password=password)
			self.is_connected = True
			print(f"{self.name}: {self.ip} : Connected.")

			### --------  Open shell
			time.sleep(.1)
			self.channel = self.ssh.invoke_shell()
			buff = ''
			while (not buff.endswith(':~# ')) and (not buff.endswith(':~$ ')):				
				resp = self.channel.recv(9999)
				resp = resp.decode()
				buff += resp
			print(f"{self.name}: interactive shell open.")
			### --------
		except:
			print("Some kind of exception!")
		# 	raise e 

	def disconnect(self):
		print(f"{self.name}: {self.ip} : Closed.")
		self.ssh.close()
		self.is_connected = False

	def python(self, *args):
		self.shell("python")

	def exec(self, *args):
		print(f" {Style.DIM}{'-'*50}{Fore.RESET}")
	    ## --

		try:
		    # Execute the command
		    command = shlex.join(args)
		    print(f"{self.name} : {Fore.BLUE}{self.ip} {Style.RESET_ALL} :: {command}")
		    stdin, stdout, stderr = self.ssh.exec_command(command)

		    # Print the output
		    print(f"{self.name} : {Fore.BLUE}{self.ip}{Style.RESET_ALL} :: ")
		    print(stdout.read().decode('utf-8'))
		except:
			print("Execution failed!")

		## --
		print(f" {Style.DIM}{'-'*50}{Fore.RESET}")

	def shell(self, *args):
		
		print(f"{self.name} {Fore.YELLOW}{'-'*50}{Style.RESET_ALL}")
		## --
		
		### --------  Clear any residual text
		self.channel.send("\n")
		buff = ''
		while (not buff.endswith(':~# ')) and (not buff.endswith(':~$ ')) and (not buff.endswith(">>> ")):
		    resp = self.channel.recv(9999)
		    resp = resp.decode()
		    buff += resp
		    print(resp)
		### --------  


		### Send the command ----------
		command = shlex.join(args)
		if not command.endswith("\n"):
			command += "\n"
		print(f"{self.name} : {Fore.BLUE}{self.ip} {Fore.RESET} >> {command}")
		self.channel.send(command)
		### -----------

		time.sleep(0.1)

		### Receive the output -----------
		print(f"{self.name} : {Fore.BLUE}{self.ip}{Fore.RESET} >> ")
		output = ""
		while True:
		    if self.channel.recv_ready():
		        chunk = self.channel.recv(1024)
		        chunk = chunk.decode()
		        output += chunk
		        print(chunk)
		        continue
		    if (output.endswith(':~# ')) or (output.endswith(':~$ ')):
		    	break

		    if output.endswith(">>> "):
		    	print("Python!")
		    	break
		    if self.channel.exit_status_ready():
		        exit_status = self.channel.recv_exit_status()
		        break
		    if self.channel.closed or self.channel.eof_received or not self.channel.active:
		        break
		    if "--More-- or (q)uit" in output:
		        print("Pagination enabled. Exiting")
		        break
		    #if time.time() > timeout:
		    #    break
		    time.sleep(.1)


		
		
		#recvd = ""
		#while "\n" in recvd:
		#print(self.channel.recv(1024).decode('utf-8'))
		
		## --
		print(f" {Fore.YELLOW}{'-'*50}{Fore.RESET}")

	def __call__(self, *args):
		self.shell(args)

	def deploy(filename):
		## TODO
		self.shell(f'scp -r {filename} trappyscope@{self.ip}:{remote_app_directory}')


class NodeRoll:

	
	def __init__(self):
		pass

	
	# Common Resources
	roll = {}

	def __get_item__(self, key):
		return NodeRoll.roll[key]


	def status():
	    """
	    Check the status of all nodes in the Raspberry Pi cluster.
	    """
	    for node in NodeRoll.roll:
	        NodeRoll.roll[node].shell('pi', 'hostname && uptime')


	def run_all(*args):
		"""
		Execute the same commnad on all nodes.
		"""
		for node in roll:
		    NodeRoll.roll[node](*args)

	def run_all_seq(command, delay_s=0):
		"""
		Execute command on all but one after the other.
		delay_s: Amount of delay added in seconds between executions.
		"""
		pass

