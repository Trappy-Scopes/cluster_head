# Cluster Head



A `NodeRoll`is a collection of `Node` objects. Each node represents a device that is connected through SSH.



## `Node`

`node.exec(cmd)` : Execute single command and close shell on the node.

 `node.shell(cmd)` : Execute commands in a single interactive shell. This function is compatible with bash and python interactive terminal.



## Schematics

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



The 



## TODO

