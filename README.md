# Cluster Head



A `cluster-head`  is a terminal that is used to requisition a collecion of autonomous devices. This collection of devices is called a `Hive` of devices. By devination, a `Hive` is a collection of `Node`objects that are specialised to their respective network connection protocols and shell types. 

The `Hive` then hosts a distribution network, the network allows the following semantics:

```mermaid
graph LR
	subgraph Hive1
		M1
		M2
		M3
		M4
	end
```

```python
## Assigns the microscopes to hive1 on the current host - creates a lock object on all the microscopes.
hive1 = Hive(["m1", "m2", "m3", "m4"])

hive1.m1.set_task("Pump Calibration", script="scripts/pumptests/arbitrart_time_calib.py")
hive1.m2.set_task("Light Calibration", script="scripts/lighttests/test2.py")
hive1.m3.set_task("Long term experiment 1", script="scripts/exps/exp2.py")
hive1.m4.set_task("Long term experiment 2", script="scripts/exps/exp2.py")

aux = AuxHive() # All availble microscopes that are not assigned to another hive.
```







## Schematics

### Hive Creation

A `Hive` is a collection of autonomous devices. It establishes connections to device shells (POSIX shell or micropython REPL) using specialised `Node` objects.

```mermaid
graph LR

main.py --user-creates--> Hive
Hive -- ssh-libmux --> RPi-SoCs
Hive -- websocket --> RPi-pico-MCUs

subgraph Nodes
	RPi-SoCs
	RPi-pico-MCUs
end

```



### Linux connections

The linux connections are established via SSH to a `tmux` session that runs the control layer –  `scope-cli`. Note that the calling command `trappyscope` within `scope-cli` initialises the scrips in a `tmux` session that is named after its own `hostname`.

```mermaid
flowchart TD

subgraph host-M1
   subgraph TMUX-M1
   		Control-Layer-M1
   end
end

subgraph host-M2
   subgraph TMUX-M2
   		Control-Layer-M2
   end
end

subgraph host-M3
   subgraph TMUX-M3
   		Control-Layer-M3
   end
end

subgraph host-M4
   subgraph TMUX-M4
   		Control-Layer-M4
   end
end

 Cluster-Head --ssh--> host-M1
 Cluster-Head --ssh--> host-M2
 Cluster-Head --ssh--> host-M3
 Cluster-Head --ssh--> host-M4
```

### Micropython connections

Connections to devices running micropython are establed through `webrepl` that accesses the device through web sockets. The utility `mpfshell` is used to programatically open the connection. The connections are only successful when:

1. The RPi Pico device connects to Wifi.
2. The webrepl server has a successful startup on initalisation.



```mermaid
graph LR
	cluster_head --calls--> mpfshell --webrepl--> REPL
	
	subgraph RPi-pico
		REPL
	end
```

## `Node` Objects

A `Node`object symbolically represents a serial interface to the connected device. However, symbolically, it represents a default shell that runs the relevant `Trappy-Systems` code.

Example: `node.beacon.on()` or `node("beacon.on()")`: the `.`operator (`__getattr__` method) and `()`operator (`__call__`method) respectively,  forwards the command `beacon.on()` to a default shell:

1. On Linux-Nodes, the default shell is a shell with a tux session: `tmux new-session -s $hname`, where `hname=hostname`.
2. On Micropython-Nodes, the default shell is a websocket to the REPL of the device. It is not permitted to have more than one REPLs on this node, however, file-transfers are possible simultaneously.

### Idioms

`node.command()` or ` node("command()")`: Preferred way to execute command on the node. 

 `node.defshell(cmd)` : Execute commands in a single interactive shell. This function is compatible with bash and micropython interactive terminal.

`node.exec(cmd)` : Execute single command in a new shell and close shell on the node (only true for Linux-Nodes, on Micropython-Nodes, it is the same as `node.defshell()`).
