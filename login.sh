#!/bin/bash

#declare gip=(172.16.64.20 172.16.64.21 172.16.64.15 172.16.64.16 172.16.60.5 172.16.60.10 172.16.60.12 172.16.60.11 172.16.61.20 172.16.61.21 172.16.61.22 \
#					172.16.61.21 172.16.61.23) 

declare vpnip=(172.30.8.10 222.128.8.203)
declare yumip=(172.30.8.9)
declare oaip=(172.16.64.21)
declare portalip=(172.16.64.15)
declare ccip=(172.30.24.22 172.16.60.5)
declare store01ip=(172.30.12.21 172.16.61.21)
declare store02ip=(172.30.12.22 172.16.61.22)
declare node01ip=(172.30.24.31 172.16.61.22)
declare node02ip=(172.30.24.32 172.16.61.23)
declare lfs=(172.30.12.105)
declare xen=(172.30.16.32)
declare cacti=(172.30.8.13)
declare cacti1=(172.31.8.13)

declare cc1=(172.31.24.22)
declare node101=(172.31.24.31)
declare node102=(172.31.24.32)
declare store101=(172.31.24.21)
declare portal101=(172.31.24.20)
declare vpn1=(172.31.8.10)
declare powervc1=(172.24.23.222)
declare powervc2=(172.24.23.129)

declare powervm1=(172.24.23.20)
declare powervm2=(172.24.23.140)
declare powervm3=(172.24.23.212)
declare paxesvm1=(172.24.23.200)
declare novavm1=(172.24.23.117)

declare masterip=(172.30.8.22)

vip=169.254.0.0

testping() {
	ping -c 1 $1 &>/dev/null
	if [ $? -eq 0 ]; then
		vip=$1
	else
		ping -c 1 $2 &>/dev/null
		if [ $? -eq 0 ]; then
			vip=$2
		else
			echo "登入不了 $3 系统!"
		fi
	fi
	return 0
}
usage() {
	printf "Usage: %s: input  < sinoi | yum | oa | portal | cc | vpn | store01 | store02 | node01 | node02 | master | lfs | cacti | node101 | node102 | store101 | portal101 | cc1 | vpn1 | powervc1 | powervc2 | powervm1 | powervm2 | powervm3 | paxesvm1 | novavm1>\n" $(basename $0)
	exit 2
}
	
case $1 in
    novavm1) vip=${novavm1[0]} ;;
    paxesvm1) vip=${paxesvm1[0]} ;;
    powervm1) vip=${powervm1[0]} ;;
    powervm2) vip=${powervm2[0]} ;;
    powervm3) vip=${powervm3[0]} ;;

    powervc1) vip=${powervc1[0]} ;;
    powervc2) vip=${powervc2[0]} ;;
    portal101) vip=${portal101[0]} ;;
    store101) vip=${store101[0]} ;;
    cc1)    vip=${cc1[0]} ;;
    node101)    vip=${node101[0]} ;;
    node102)    vip=${node102[0]} ;;
	cacti)	vip=${cacti[0]} ;;
	cacti1)	vip=${cacti1[0]} ;;
	lfs)	vip=${lfs[0]} ;;
	xen)	vip=${xen[0]} ;;
	sinoi)	vip=${vpnip[1]} ;;
	vpn) 	vip=${vpnip[0]} ;;
	vpn1) 	vip=${vpn1[0]} ;;
	master)	testping ${masterip[0]} "" "master" ;;
	yum)	testping ${yumip[0]} "" "yum" ;;
	oa)		testping ${oaip[1]} "" "oa";;
	portal)	testping ${portalip[0]} "" "portal" ;;
	cc)		testping ${ccip[0]} ${ccip[1]} "cc" ;;
	store01) testping ${store01ip[0]} ${store01ip[1]} "store01" ;;
	store02) testping ${store02ip[0]} ${store02ip[1]} "store02" ;;
	node01) testping ${node01ip[0]} ${node01ip[1]} "node01" ;;
	node02) testping ${node02ip[0]} ${node02ip[1]} "node02" ;;
	*)	usage
		exit 1 ;;
esac

#--------------服务器的ip地址-----------------------------#
#	ip=`expr $1 - 1`
#	printf "服务器的IP地址:\t%s\n" ${gip[$ip]}
if [ -z ${vip} ]; then
	printf "登入不了系统\t获取不到ip地址!\n"
else
	printf "服务器的IP地址:\t%s\n" $vip
fi
#-------------登入到服务器的------------------------------#
#	expect /root/work/login/mylogin.sh   ${gip[$ip]}
	expect /root/work/login/mylogin.sh   $vip
	clear
	if [ $? -eq 0 ] ; then
		echo "您已经退出了服务器了！"
	else
		echo "服务器链接不上！"
	fi
exit 0
