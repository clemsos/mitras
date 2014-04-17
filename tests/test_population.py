#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv,os,json


results_path="/home/clemsos/Dev/mitras/results/"
population_file=results_path+"ChineseProvincesPopulation2010Census.csv"
gdp_file=results_path+"ChineseProvincesGDP_PPP.csv"

provinces_data_file=results_path+"ChineseProvincesInfo.json"

provinces=["Gansu","Qinghai","Guangxi","Guizhou","Chongqing","Beijing","Fujian","Anhui","Guangdong","Xizang","Xinjiang","Hainan","Ningxia","Shaanxi","Shanxi","Hubei","Hunan","Sichuan","Yunnan","Hebei","Henan","Liaoning","Shandong","Tianjin","Jiangxi","Jiangsu","Shanghai","Zhejiang","Jilin","Inner Mongol","Heilongjiang","Taiwan","Xianggang","Aomen"]

# parse data
pop={}
with open(population_file, 'rb') as csvpopulation:

    poplist=csv.reader(csvpopulation, delimiter=";")
    poplist.next() # skip headers

    for p in poplist : pop[p[0]]=p[1]

gdp={}
with open(gdp_file, 'rb') as csvgdp:

    gdplist=csv.reader(csvgdp, delimiter=";")
    gdplist.next() # skip headers

    for p in gdplist : gdp[p[0]]=p[1] 

# print pop
# print gdp
data=[]
for province in provinces:
 
    if province not in pop : raise KeyError(province) 
    if province not in gdp : raise KeyError(province) 

    p=province

    if province=="Xianggang"  : p="Hong Kong"
    elif province=="Aomen" : p="Macau"
    elif province=="Inner Mongol" : p="Inner Mongolia"

    data.append({"name":province, "clean_name": p, "gdp":gdp[province],"population":pop[province]})
    
print data
# write d3js annotated graph
with open(provinces_data_file, 'w') as outfile:
    json.dump(data, outfile)
    print "json data have been saved to %s"%(provinces_data_file)