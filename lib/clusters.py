#!/usr/bin/env python
# -*- coding: utf-8 -*-


from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list

def get_linkage_matrix(matrix_data):
    print " calculate matrix w average linkage algorithm"
    linkage_matrix=linkage(matrix_data, method='average')
    print " clusters: n_samples: %d, n_features: %d" % linkage_matrix.shape
    return linkage_matrix

def explain_linkage_clusters(clusters, labels):
    for row in clusters:
        i=int(row[0])
        value1="cluster"
        if i in range(0,len(clusters)):
            value1=labels[i]    

        j=int(row[0])
        value2="cluster"
        if j in range(0,len(clusters)):
            value2=labels[j]

        print row
        print "---> [",value1,value2, row[2],"]"

def create_d3js_heatmap_data_file(ordered_data_matrix, labels):

    # prepare data for visualization in a browser with javascript/d3.js
    matrixOutput = []
    row = 0
    for rowData in ordered_data_matrix:
        col = 0
        rowOutput = []
        for colData in rowData:
            rowOutput.append([colData, row, col])
            col += 1
        matrixOutput.append(rowOutput)
        row += 1


    # Export to js vars for visualization with d3.js
    jsfile=""
    jsfile+='var maxData = ' + str( np.amax(protomemes) ) + ";"
    jsfile+='\n\n'
    jsfile+= 'var minData = ' + str(np.amin(protomemes)) + ";"
    jsfile+='\n\n'
    jsfile+= 'var data = ' + str(matrixOutput) + ";"
    jsfile+='\n\n'
    jsfile+= 'var cols = ' + str(labels) + ";"
    jsfile+='\n\n'
    jsfile+= 'var rows = ' + str([x for x in ordered_row_headers]) + ";"

    with open('../ui/data/data.js', 'w') as myFile:
        myFile.write(jsfile)

