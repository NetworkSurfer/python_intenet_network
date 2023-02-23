import json
from bs4 import BeautifulSoup
import ipcalc
import ipaddress
import itertools as it

next_net_address_link = u'10.0.0.0/31' ############################ Need to change for each iteration
network = ipcalc.Network(next_net_address_link)
network_addrs = (network + (i + 1) * network.size() for i in it.count())

topology_file = open("C:\\Users\\gbvaghas\\Desktop\\Python_Practice\\AI_network_design\\AI_network_design.gns3",'r')
topology_data = topology_file.read()
res = json.loads(topology_data)

nodes = {}
node_list = []
node_id_2_name_map = {}
for l in range(len(res["topology"]["nodes"])):
    #node_info = []
    node_info = {}
    #node_info.append(res["topology"]["nodes"][l]["node_id"])
    node_info["NODE_ID"] = res["topology"]["nodes"][l]["node_id"]
    #node_info.append(res["topology"]["nodes"][l]["label"]["text"])
    node_info["HOSTNAME"] = res["topology"]["nodes"][l]["label"]["text"]
    node_list.append(node_info["HOSTNAME"])
    nodes[node_info["HOSTNAME"]] = node_info
    node_id_2_name_map[node_info["NODE_ID"]] = node_info["HOSTNAME"]
#print (node_list)
#print (nodes)

for i in res["topology"]["drawings"]:
    soup = BeautifulSoup(i["svg"])
    #print (ext_data)
    #print (soup.find_all('text'))
    for a in soup.find_all('text'):
        #print (a.string)
        x = a.string.split('\n')
        for p in x:
            if p != "":
                y = p.split('-')
                #print (y)
                #nodes[y[0].strip()].append(y[1].strip())
                nodes[y[0].strip()]["ROLE"] = y[1].strip()
        #print (x)
#print (node_list)        
#print (nodes)
next_net_address_loop = u'100.0.0.0/24'
loop_net4 = ipaddress.ip_network(next_net_address_loop)
loop_ip = [str(ip) for ip in loop_net4.hosts()]
for i in range(len(node_list)):
    #nodes[node_list[i].strip()].append(loop_ip[i].strip())
    nodes[node_list[i].strip()]["LOOP_INT_IP"] = loop_ip[i].strip()
    nodes[node_list[i].strip()]["INT_IP"] = []
#print (nodes)


links = {}
links_list = []
nei_list = []        
for j in range(len(res["topology"]["links"])): # number of links
    links_list.append(res["topology"]["links"][j]["link_id"])
    #nei_list = []
    net4 = ipaddress.ip_network(next_net_address_link)
    hosts = [str(ip) for ip in net4.hosts()]
    for k in range(len(res["topology"]["links"][j]["nodes"])): # number of nodes connected to link
        #print (res["topology"]["links"][j]["nodes"][k]["node_id"])        # node
        link_info = []
        link_info.append(res["topology"]["links"][j]["nodes"][k]["node_id"])
        link_info.append(res["topology"]["links"][j]["nodes"][k]["label"]["text"])
        link_info.append(hosts[k])
        if len(res["topology"]["links"][j]["nodes"]) == 2:
            #a = 1 - k
            #print (res["topology"]["links"][j]["nodes"][1-k]["node_id"])
            link_info.append(res["topology"]["links"][j]["nodes"][1-k]["node_id"])
        nei_list.append(link_info)
    links[res["topology"]["links"][j]["link_id"]] = nei_list
    next_net_address_link = next(network_addrs)

##print (links)
#print (links_list)
#print (nei_list)


for m in nei_list:
    #nodes[n]["INT_IP"] = []
    for n in node_list:
        #if m[0] == nodes[n][0]:
        #print (m[0])
        #print (nodes[n]["HOSTNAME"])
        if m[0] == nodes[n]["NODE_ID"]:
            #nodes[n].append([m[1],m[2]])
            #nodes[n]["INT_IP"].append([m[1],m[2],m[3]])
            nodes[n]["INT_IP"].append([m[1],m[2],node_id_2_name_map[m[3]],nodes[node_id_2_name_map[m[3]]]["ROLE"]])
           
           
           
print (nodes)
##print (nei_list)
#
def node_config(RTR):
    print("hostname " + RTR["HOSTNAME"])
    print("interface loopback 1")
    print(" ip address " + RTR["LOOP_INT_IP"])
    for i in range(len(RTR["INT_IP"])):
        print ("interface " + RTR["INT_IP"][i][0])
        print (" ip address " + RTR["INT_IP"][i][1] + " 255.255.255.254")
        print (" no shutdown")
    if "CE" not in RTR["ROLE"]:
        print ("router ospf 1")
        print (" network " + RTR["LOOP_INT_IP"] + " 0.0.0.0")
        for i in range(len(RTR["INT_IP"])):
            if "CE" not in RTR["INT_IP"][i][3]:
                print (" network " + RTR["INT_IP"][i][1] + " 0.0.0.0")
    if "PE" in RTR["ROLE"]:
        print ("router bgp 100")
        for i in node_list:
            if "RR" in nodes[i]["ROLE"]:
                #print (nodes[i])
                print ("neighbor " + nodes[i]["LOOP_INT_IP"] + " remote-as 100")
        for i in RTR["INT_IP"]:
            for j in nodes[i[2]]["INT_IP"]:
                if j[2] == RTR["HOSTNAME"]:# and "CE" in nodes[i[2]]["ROLE"]:
                    #print (nodes[i[2]]["HOSTNAME"])
                    print ("neighbor " + j[1] + " remote-as 65000")
    elif "RR" in RTR["ROLE"]:
        print ("router bgp 100")
        for i in node_list:
            if "PE" in nodes[i]["ROLE"]:
                #print (nodes[i])
                print ("neighbor " + nodes[i]["LOOP_INT_IP"] + " remote-as 100")
                print ("neighbor " + nodes[i]["LOOP_INT_IP"] + " route-reflector-client")                
    elif "CE" in RTR["ROLE"]:
        print ("router bgp 65000")
        for i in RTR["INT_IP"]:
            for j in nodes[i[2]]["INT_IP"]:
                if j[2] == RTR["HOSTNAME"]:
                    print ("neighbor " + j[1] + " remote-as 100")
                   
    else:
        print ("router bgp 65000")
    print ("!!!")
#
for i in node_list:
    node_config(nodes[i])
#print (links_list)
