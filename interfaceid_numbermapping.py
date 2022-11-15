import json
from bs4 import BeautifulSoup
from pprint import pprint

topology_file = open("C:\\Users\\gbvaghas\\Desktop\\Python_Practice\\AI_network_design\\AI_network_design.gns3",'r')
topology_data = topology_file.read()
res = json.loads(topology_data)
#print (len(res["topology"]["nodes"]))
node_dict = {}
#############This Function is to Extract the Role of Nodes and its Name############
#for i in range(len(res["topology"]["nodes"])):
    #soup = BeautifulSoup(i["svg"])
    #print (ext_data)
    #print (soup.find_all('text'))
    #for a in soup.find_all('text'):
    #print (res["topology"]["nodes"][i]['node_id'] + '-' + res["topology"]["nodes"][i]['name'] )
    #node_dict[res["topology"]["nodes"][i]['node_id']] = res["topology"]["nodes"][i]['name']
#pprint(node_dict)
    
###this function is to map Node Id and Node Name#################
#for j in range(len(res["topology"]['links'])):
    #for k in range(len(res["topology"]['links'][j]['nodes'])):
        #print(res["topology"]['links'][j]['nodes'][k])
        #print('hello')



#print(len(res['topology']['links']))#####this is to find the total number of links 
link_node_map = {}

#print(len(res['topology']['links'][0]['nodes']))#### this is to find the total number of nodes on connected on particular link
for l in range(len(res['topology']['links'])):
    a = []
    for n in range(len(res['topology']['links'][l]['nodes'])):
        a.append([])
    #print(a)
    for m in range(len(res['topology']['links'][l]['nodes'])):
        a[m].append(res['topology']['links'][l]['nodes'][m]['node_id'])
        a[m].append(res['topology']['links'][l]['nodes'][m]['label']['text'])
        #link_node_map[res['topology']['links'][l]['link_id']] 
    link_node_map[res['topology']['links'][l]['link_id']] = a
pprint(link_node_map)
    



    
