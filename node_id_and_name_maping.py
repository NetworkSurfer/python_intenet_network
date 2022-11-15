import json
from bs4 import BeautifulSoup
from pprint import pprint

topology_file = open("C:\\Users\\gbvaghas\\Desktop\\Python_Practice\\AI_network_design\\AI_network_design.gns3",'r')
topology_data = topology_file.read()
res = json.loads(topology_data)
#print (len(res["topology"]["nodes"]))
node_dict = {}
for i in range(len(res["topology"]["nodes"])):
    #soup = BeautifulSoup(i["svg"])
    #print (ext_data)
    #print (soup.find_all('text'))
    #for a in soup.find_all('text'):
    #print (res["topology"]["nodes"][i]['node_id'] + '-' + res["topology"]["nodes"][i]['name'] )
    node_dict[res["topology"]["nodes"][i]['node_id']] = res["topology"]["nodes"][i]['name']
pprint(node_dict)
    
    
#for j in range(len(res["topology"]['links'])):
    #for k in range(len(res["topology"]['links'][j]['nodes'])):
        #print(res["topology"]['links'][j]['nodes'][k])
        #print('hello')