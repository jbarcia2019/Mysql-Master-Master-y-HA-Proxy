# Instalación de 2 nodos MySQL y HA-Proxy en Docker

## Nodos
Servidor MySQL#1 (node1)
- Ubuntu Server 24.04
- IP : 192.168.159.3
- Nombre de host : node1

Servidor MySQL#2 (node2)
- Ubuntu Server 24.04
- IP : 192.168.159.4
- Nombre de host : node2

## Instalación de MySQL Master-Slave
### Nodo1:
- sudo apt install mysql-server
- systemctl status mysql
- sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
  - bind-address = 0.0.0.0
  - server-id = 1
  - log_bin = /var/log/mysql/mysql-bin.log
- sudo systemctl restart mysql
- sudo mysql -u root -p
  - CREATE USER 'repl'@'192.168.159.4' IDENTIFIED BY 'secret';
  - GRANT REPLICATION SLAVE ON *.* TO 'repl'@'192.168.159.4';
  - SHOW MASTER STATUS \G -- De aquí conseguimos el nombre del log file y el log pos para el nodo2

### Nodo2:
- sudo apt install mysql-server
- systemctl status mysql
- sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
  - bind-address = 0.0.0.0
  - server-id = 2
  - log_bin = /var/log/mysql/mysql-bin.log
- sudo systemctl restart mysql
- sudo mysql -u root -p
  - CHANGE REPLICATION SOURCE TO SOURCE_HOST='192.168.159.4', SOURCE_LOG_FILE='mysql-bin.000001', SOURCE_LOG_POS=946, SOURCE_SSL=1;
  - START REPLICA USER='repl' PASSWORD='secret';
  - SHOW REPLICA STATUS \G

## Instalación MySQL Master-Master
### Nodo2:
- sudo mysql -u root -p
  - CREATE USER 'repl'@'192.168.159.3' IDENTIFIED BY 'secret';
  - GRANT REPLICATION SLAVE ON *.* TO 'repl'@'192.168.159.3';
  - SHOW MASTER STATUS \G

### Nodo1:
- CHANGE REPLICATION SOURCE TO SOURCE_HOST='192.168.159.3', SOURCE_LOG_FILE='mysql-bin.000001', SOURCE_LOG_POS=904, SOURCE_SSL=1;
- START REPLICA USER='repl' password='secret';
- SHOW REPLICA STATUS \G

## Instalación de HA-Proxy en Docker para los dos nodos MySQL
- Crear haproxy.cfg y desplegar con el docker-compose.yml

## Sincronización de los nodos cuando uno cae
### Desde terminal
- sudo mysql -u root -p
  - FLUSH HOSTS;
### Desde código en python
- cursor.execute("FLUSH HOSTS")
