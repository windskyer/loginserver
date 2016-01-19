#!/usr/bin/expect -f
set timeout 5
set ip [ lindex $argv 0 ]
set user [ lindex $argv 1 ]
set passwd [ lindex $argv 2 ]
set port [ lindex $argv 3 ]
#spawn ssh -i /root/.ssh/id_rsa.bak.login_server leidong@${ip} -o ConnectTimeout=3
spawn ssh  ${user}@${ip} -p ${port} -o ConnectTimeout=3
#spawn ssh  ${user}@${ip} -p ${port}
expect {
	"*yes/no" { send "yes\r"; exp_continue }
#	"*/root/.ssh/id_rsa.bak.login_server" { send "flftuu\r" }
#	"Enter passphrase for key *" { send "flftuu\r" }
	"Enter passphrase for key '/root/.ssh/id_rsa.bak.login_server':" {send "${passwd}\r"}
    "*password:" {send "${passwd}\r"}
}
#expect "*~]$"
#send "sudo su -\r"
expect "*~]#"
send "clear\r"
interact
