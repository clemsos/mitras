#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv,os
import json
from time import time
import networkx as nx
import pylab as plt
from collections import Counter
import community


# get meme_names
results_path="/home/clemsos/Dev/mitras/results/"
meme_names=[ meme for meme in os.listdir(results_path) if meme[-3:] != "csv"]
# meme_names=["biaoge"]

meme_names.sort()

t0=time()

for meme_name in meme_names:
    print "-"*30
    tstart=time()
    print "Processing meme '%s'"%meme_name

    meme_path=results_path+"/"+meme_name

    # source file
    meme_graph_csv=meme_path+"/"+meme_name+"_edges.csv"

    # destination file
    json_file=meme_path+"/"+meme_name+"_graph_info.json"
    d3_file=meme_path+"/"+meme_name+"_d3graph.json"

    jsondata={}
    # parse graph data into network x object
    with open(meme_graph_csv, 'rb') as edgefile:
        edgefile.next() # skip headers
        edgecsv=csv.reader(edgefile)
        
        edges=[(e[0], e[1]) for e in edgecsv]
        edges_weighted=[str(p[0][0]+" "+p[0][1]+" "+str(p[1])) for p in Counter(edges).most_common()] # if p[1] > 1]
            
        print "Edges (raw files) : %d edges"%len(edges)
        print "Weighted edges %d"%len(edges_weighted)

    jsondata["graph"]={}
    jsondata["graph"]["total_raw_edges"]=len(edges)
    # jsondata["graph"]["single_edges"]=len(edges_weighted)

    G = nx.read_weighted_edgelist(edges_weighted, nodetype=str, delimiter=" ",create_using=nx.DiGraph())

    N,K = G.order(), G.size()
    print "Nodes: ", N
    print "Edges: ", K

    jsondata["graph"]["total_nodes"]=N
    jsondata["graph"]["total_edges"]=K

    # init nodes
    d3nodes={}
    for n in G.nodes(data=True) : 
        d3nodes[ n[0] ]=n[1]
        d3nodes[ n[0]]["name"]=n[0]


    # Clustering and degree coeficient
    #################################

    avg_deg = float(K)/N
    print "Average degree: ", avg_deg
    jsondata["graph"]["average_degree"]=avg_deg

    # Clustering coefficient of all nodes (in a dictionary)
    ccs = nx.clustering(G.to_undirected())

    # Average clustering coefficient
    avg_clust_coef = sum(ccs.values()) / len(ccs) # also : nx.algorithms.cluster.average_clustering(G.to_undirected())
    print "Average clustering coeficient: %f"%avg_clust_coef
    jsondata["graph"]["average_clustering_coeficient"]=avg_clust_coef


    # In/Out Degrees 
    #################################

    jsondata["in_degrees"]={}
    in_degrees = G.in_degree() # dictionary node:degree

    # distribution
    jsondata["in_degrees"]["distribution"]=[{"number_of_nodes":deg[1], "in_degree":deg[0] } for deg in  Counter(in_degrees.values()).most_common() ] #if v[0] > 2] 

    # highest values
    jsondata["in_degrees"]["top_nodes"]=[]
    for i,deg in enumerate(sorted(in_degrees.values(),reverse=True)[0:5]):
        print "Highest in-degree value for node %s : %d "% (i,deg)
        jsondata["in_degrees"]["top_nodes"].append({ "index":i, "degree":deg })

    jsondata["out_degrees"]={}
    out_degrees = G.out_degree() # dictionary node:degree

    # distribution
    jsondata["out_degrees"]["distribution"]=in_deg_dist=[{"number_of_nodes":deg[1], "out_degree":deg[0] } for deg in  Counter(out_degrees.values()).most_common() ] #if v[0] > 2] 

    # highest values
    jsondata["out_degrees"]["top_nodes"]=[]
    for i,deg in enumerate(sorted(out_degrees.values(),reverse=True)[0:5]):
        print "Highest in-degree value for node %s : %d "% (i,deg)
        jsondata["out_degrees"]["top_nodes"].append({ "index":i, "degree":deg})


    #add values to node
    for node in in_degrees: d3nodes[node]["in_degree"]=str(in_degrees[node])
    for node in out_degrees: d3nodes[node]["out_degree"]=str(out_degrees[node])

    # Cliques
    #################################

    jsondata["cliques"]={}

    cliques=[c for c in nx.find_cliques(G.to_undirected())]
    cliques_length=[len(c) for c in nx.find_cliques(G.to_undirected())]

    average_clique_length=sum([float(c) for c in cliques_length])/len(cliques_length)

    print "total cliques: %d"%len(cliques_length)
    print "max clique length: %d"%max(cliques_length)
    print "average clique length: %f"%average_clique_length

    jsondata["cliques"]["number_of_cliques"]=len(cliques_length)
    jsondata["cliques"]["longest_clique"]=max(cliques_length)
    jsondata["cliques"]["average_clique_length"]=average_clique_length

    jsondata["cliques"]["distribution"]=[ {"value" : c[1], "count":c[0]} for c in Counter(cliques_length).most_common() ]


    # Components
    #################################

    G_components = nx.connected_component_subgraphs(G.to_undirected())
    print "Number of components: %d"% len(G_components) #nx.number_connected_components(G.to_undirected())

    jsondata["connected_components"]={}
    jsondata["connected_components"]["number_connected_components"]=len(G_components)
    jsondata["connected_components"]["main_components"]=[]

    components_distribution=[]
    components_avg_shortest_path=[]

    print "computing components_distribution and average_short_path..."
    for i,g in enumerate(G_components): 
        comp_per_total=(float(g.number_of_nodes())/G.number_of_nodes())*100
        components_distribution.append(g.number_of_nodes());
        
        for node in g.nodes(): d3nodes[node]["component"]=i

        if len(g) > 1: avg_shortest_path=nx.average_shortest_path_length(g)
        else : avg_shortest_path=0.0
        
        components_avg_shortest_path.append(avg_shortest_path)
        for node in g.nodes(): d3nodes[node]["component_"+str(i)+"_avg_shortest_path"]=avg_shortest_path

        if i<10 : 
            jsondata["connected_components"]["main_components"].append({"index": i, "percent_total":comp_per_total, "number_of_nodes" : g.number_of_nodes(), "average_short_path" : nx.average_shortest_path_length(g) })
            # (i,comp_per_total)
            # print "cluster %i : %.3f %% "%(i,comp_per_total)

    jsondata["connected_components"]["components_distribution"]=[ {"number_of_nodes":count[0], "count":count[1] }for count in Counter(components_distribution).most_common()]

    jsondata["connected_components"]["average_short_path_total"]=sum(components_avg_shortest_path)/len(components_avg_shortest_path)

    jsondata["connected_components"]["average_short_path_distribution"]=[ {"average_short_path":count[0], "number_of_components":count[1] }for count in Counter(components_avg_shortest_path).most_common()]


    # write GraphML file with the main component only
    G_mc = G_components[0]
    G_mc_per_total= (float(G_mc.number_of_nodes())/G.number_of_nodes())*100
    print "Biggest connected component is %.2f %% of the graph" % G_mc_per_total
    nx.write_graphml(G_mc, meme_path+"/"+meme_name+"_main_component.graphml")


    # Communities
    # from http://perso.crans.org/aynaud/communities/ 
    ##################################################################

    jsondata["communities"]={}

    # Best partition
    best_partition = community.best_partition(G.to_undirected()) 
    modularity=community.modularity(best_partition,G.to_undirected())
    print "Modularity of the best partition: %f"%modularity
    print "Number of nodes in the best partition : ", len(set(best_partition.values())) 

    jsondata["communities"]={}
    jsondata["communities"]={}
    jsondata["communities"]["modularity"]=modularity
    jsondata["communities"]["number_of_communities"]=len(set(best_partition.values()))

    # write best partition graph to GraphML file
    # G_ok=community.induced_graph(best_partition,G.to_undirected())
    # nx.write_graphml(G_ok, meme_path+"/"+meme_name+"_best_partition.graphml")

    for node in best_partition:
        d3nodes[node]["community"]=best_partition[node]

    # CENTRALITIES 
    # http://toreopsahl.com/tnet/weighted-networks/node-centrality/
    #################################

    # Betweeness centrality
    jsondata["betweeness_centrality"]={}
    # Create ordered tuple of centrality data
    print "computing betweeness_centrality... (this may take some time)"
    cent_dict=nx.betweenness_centrality (G.to_undirected())
    cent_items=[(b,a) for (a,b) in cent_dict.iteritems()]

    # add value to nodes
    for node in cent_dict: d3nodes[node]["btw_cent"]=cent_dict[node]

    # Sort in descending order 
    cent_items.sort() 
    cent_items.reverse() 

    # Highest centrality 
    jsondata["betweeness_centrality"]["top"]=[]
    for j,c in enumerate(cent_items[0:5]):
        print "Highest betweeness centrality :%.3f"%c[0]
        jsondata["betweeness_centrality"]["top"].append({"index": j, "value" :"%.3f"%c[0], "id" : c[1] })

    # Collect discretized distribution of centralities
    btw_cent_dist=[{"value":c[0],"count" :c[1] } for c in Counter(["%.3f"%c[0] for c in cent_items]).most_common()]

    jsondata["betweeness_centrality"]["distribution"]=btw_cent_dist
    jsondata["graph"]["average_betweeness_centrality"]=sum([c[0] for c in cent_items])/len(cent_items)

    # Closeness centrality
    # print "Computing closeness_centrality..."
    # clo_cen = nx.closeness_centrality(G.to_undirected())
    # for node in clo_cen: d3nodes[node]["closeness_cent"]=clo_cen[node] # add value to nodes

    # # Eigenvector centrality
    # print "Computing Eigenvector centrality..."
    # eig_cen = nx.eigenvector_centrality(G.to_undirected())
    # for node in eig_cen: d3nodes[node]["eigenvector_cent"]=eig_cen[node] # add value to nodes


    # OUTPUT STATS
    # write data to file
    #################################
    with open(json_file, 'w') as outfile:
        json.dump(jsondata, outfile)
        print "json data have been saved to %s"%(json_file)

    # OUTPUT D3 GRAPH
    ################################

    min_weight=2


    # d3data["nodes"]=[d3nodes[node] for node in d3nodes ]
    # d3data["edges"]=[ {"source":edge[0],"target":edge[1],"weight":edge[2]["weight"] } for edge in G.edges(data=True)]

    d3data={}
    d3data["nodes"]=[]
    d3data["edges"]=[ {"source":edge[0],"target":edge[1],"weight":edge[2]["weight"] } for edge in G.edges(data=True) if edge[2]["weight"] >= min_weight]
    d3_nodes_done=[]
    for edge in d3data["edges"]:
        if edge["source"] not in d3_nodes_done:
            d3_nodes_done.append(edge["source"])
            d3data["nodes"].append(d3nodes[edge["source"]])
        if edge["target"] not in d3_nodes_done:
            d3_nodes_done.append(edge["target"])
            d3data["nodes"].append(d3nodes[edge["target"]])

    # write d3js annotated graph
    with open(d3_file, 'w') as outfile:
        json.dump(d3data, outfile)
        print "json data have been saved to %s"%(d3_file)

    print "done in %.3fs"%(time()-tstart)

print "Everything done in %.3fs"%(time()-t0)
