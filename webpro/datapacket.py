import scapy
from scapy.all import *
from scapy.utils import PcapReader
import  random
conf.verb=0
random_port=(100,200,300,400)
payload = "Hello World! "  # 数据包内容
payload2="hi world"
for i in range(1,5000):
    packet = IP(src="10.0.0."+str(random.randint(1,4)), dst="10.0.0."+str(random.randint(1,4)))/TCP(sport=random.choice(random_port),dport=random.choice(random_port)) / Raw(load=payload) 
    send(packet)
print('send1 ok')

for i in range(1,5000):
    packet = IP(src="10.0.0."+str(random.randint(1,4)),dst="10.0.0."+str(random.randint(1,4)))/fuzz(UDP()/NTP(version=4))/Raw(load=payload2)
    send(packet)
print('send2 ok')

