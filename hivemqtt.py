import ssl
import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
from paho import mqtt
from time import sleep
import ast

from rich import print

class HiveMQTT:
	counter = 0
	def print_msg(client, userdata, message):
	    """
	        Prints a mqtt message to stdout ( used as callback for subscribe )

	        :param client: the client itself
	        :param userdata: userdata is set when initiating the client, here it is userdata=None
	        :param message: the message with topic and payload
	    """
	    print(f"{message.topic} ||>>", ast.literal_eval(message.payload.decode()))
	    HiveMQTT.counter += 1

	def loop_read():
		
		try:
			while True:
				# use TLS for secure connection with HiveMQ Cloud
				sslSettings = ssl.SSLContext(mqtt.client.ssl.PROTOCOL_TLS)

				# put in your cluster credentials and hostname
				auth = {'username': "trappyscope", 'password': "cr_in_trappy"}
				subscribe.callback(HiveMQTT.print_msg, "#", 
								   hostname="d093a1f309db470597759456d1eeefd4.s1.eu.hivemq.cloud",
								   port=8883, auth=auth,
				                   tls=sslSettings, protocol=paho.MQTTv31)
				sleep(0.5)
		except KeyboardInterrupt:
			print("Message Counter: ", counter)

if __name__ == "__main__":
	print("Exec")
	HiveMQTT.loop_read()