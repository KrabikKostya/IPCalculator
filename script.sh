cd /home/krabik/Projects/Лабораторные/Python/project/networks/logs
ip addr >> net_config.txt
#net share не працює, оскільки використовую ос Linux
arp -a >> arp_table.txt
ip a | grep ether | gawk "{print $2}" >> mac_list.txt
