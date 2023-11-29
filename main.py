import paramiko
from node import Node, NodeRoll
# List of Raspberry Pi IP addresses

scopes = NodeRoll()
all_nodes = {
          "m3": '192.168.0.161',
          "m4": '192.168.0.131',
        } # directory of nodes



## Get the nodes up and running
def assemble(all_nodes):
  for scope in all_nodes:
    addr = f"{all_nodes[scope]}"
    #exec(f"{scope} = Node({scope}, {addr}, 'chlamy')", globals())
    scopes.roll[scope] = Node(scope, all_nodes[scope], 'chlamy')



def execute_command_on_node(ip, username, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the Raspberry Pi
        ssh.connect(ip, username=username)

        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)

        # Print the output
        print(f"Node {ip}:")
        print(stdout.read().decode('utf-8'))

    finally:
        # Close the SSH connection
        ssh.close()

def check_cluster_status():
    """
    Check the status of all nodes in the Raspberry Pi cluster.
    """
    for node in cluster_nodes:
        execute_command_on_node(node, 'pi', 'hostname && uptime')

def update_cluster():
    """
    Update the packages on all nodes in the Raspberry Pi cluster.
    """
    for node in cluster_nodes:
        execute_command_on_node(node, 'pi', 'sudo apt update && sudo apt upgrade -y')

# def deploy_to_cluster():
#     """
#     Deploy the application to all nodes in the Raspberry Pi cluster.
#     """
#     local_app_directory = '/path/to/your/app'
#     remote_app_directory = '~/'

#     for node in cluster_nodes:
#         execute_command_on_node(node, 'pi', f'scp -r {local_app_directory} pi@{node}:{remote_app_directory}')

# Add more functions based on your specific needs

if __name__ == "__main__":
    assemble(all_nodes)
    #deploy_to_cluster()
