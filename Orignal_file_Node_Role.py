import json
from bs4 import BeautifulSoup

topology_file = open("C:\\Users\\gbvaghas\\Desktop\\Python_Practice\\AI_network_design\\AI_network_design.gns3",'r')
topology_data = topology_file.read()
res = json.loads(topology_data)

for i in res["topology"]["drawings"]:
    soup = BeautifulSoup(i["svg"])
    #print (ext_data)
    #print (soup.find_all('text'))
    for a in soup.find_all('text'):
        print (a.string)