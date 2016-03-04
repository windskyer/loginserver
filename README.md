loginserver
===

loginserver is a ssh to remote sshd server but we don't input 
'ssh -l root 10.0.0.1 -p 22' and don't input 'yes' , 'password'.

This means you can fast login youself a or more sshd server in one terminal windows

https://github.com/windskyer/Loginserver/

Usage
====

```
$ source run.sh
$ loginserver vm22
ssh -l root -p 2222 www.vm22.com
```


```
$ source run.sh
$ loginserver vm23
ssh -l root -p 22 192.168.122.23
```

```
$ source run.sh
$ loginserver vm23
ssh -l root -p 22 -i ~/.ssh/id_ras_24 192.168.122.23
```
Config File
===
```
[DEFAULT]
ip = 1.1.1.1
port = 22
username = root
password = toor
is_key = False
key_file = id_ras

[vm22]
hostname = www.vm22.com
ip = 192.168.122.22
port = 2222
username = root
password = toor

[vm23]
ip = 192.168.122.23
password = toor

[vm24]
ip = 192.168.122.24
is_key = True
key_file = id_ras_24
```
Download
===
Download [loginserver](http://wwww.flftuu.com/rpm/loginserver/ "loginserver") rpm 
