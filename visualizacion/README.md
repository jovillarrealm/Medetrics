# Proyecto 1

En cada máquina se puede clonar el repositorio https://github.com/jovillarrealm/jovillarrealm-st0263 donde se encuentra la carpeta p1. En esta carpeta se encuentra el código de dataNodes y nameNodes. (hay 4 subcarpetas: 2 de dataNodes, 2 nameNodes. Esto para facilitar la clonación y configuración pero el código es el mismo entre nameNodes y entre dataNodes).

# Configuración

En cada subcarpeta hay un .env a modificar.
## dataNodes
Bajo las máquinas en las que se presenta este proyecto en cada dataNode es necesario configurar individualmente la nueva IP pública cada vez en la variable PUBLIC_SERVER_IP.

```env
BACKUP = 172.31.92.71 # cada dataNode tiene un servidor que servirá de backup para el manejo de archivos
SHARED_DIR = shared
PUBLIC_SERVER_IP = 3.91.204.37 #dirección pública por la que flask estará escuchando
GRPC_SERVER_IP = 172.31.84.214 #dirección por la cual los nameNodes listan archivos y los dataNodes hacen replicación
```


## nameNodes
En cada máquina hay que configurar cada IP Pública de los dataNodes en el mismo orden de las IPs privadas en el GRPC_DATANODES.
```env
DATANODES = 3.91.204.37:50051,3.84.219.149:50051,100.24.2.51:50051 #direcciones publicas
NAME_NODE=172.31.85.253 # direccion privada del nameNode, que si está funcionando, este servirá de respaldo
SELF_IP=172.31.91.33 #direccion privada del servidor actual
GRPC_DATANODES = 172.31.84.214:50051,172.31.92.71:50051,172.31.92.126:50051 #direcciones privadas de datanodes
```