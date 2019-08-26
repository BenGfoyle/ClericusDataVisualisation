#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thursday 18-July-2019

@author: BenGfoyle - github.com/bengfoyle
Overview: This program will retrieve data from a file and construct several
plots based on the files contents.
"""
import numpy as np#for mathematical functions
import plotly.graph_objects as go
from plotly.graph_objs import *
import plotly.tools as tls
import plotly.io as plio
import chart_studio.plotly as py
import pandas as pd #csv handler
import networkx as nx #network graphs
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from plotly.offline import plot, iplot
import geopandas as gpd
from collections import Counter

#==============================================================================
def fileRead(file):
    """
    Overview: This function reads the text file and passes two
    lists back to the main method
    """

    #define lists and and file name, ISO-8859-1 for Irish characters
    name, ext = file.split(".")
    clerics = pd.DataFrame()
    if ext == "csv":
        clerics = pd.read_csv(file, encoding='ISO-8859-1')
    elif ext == "json":
        clerics = pd.read_json(file, encoding='ISO-8859-1')
        clerics = clerics.transpose()
    else:
        print("Error: Unsupported File Type ", ext)

    clerics.replace('', np.nan, inplace=True)
    clerics = clerics.dropna(axis = 0, how = 'any', thresh = None, subset = None,
                inplace = False)

    return clerics
#==============================================================================

#==============================================================================
def enteredAndOrdained(ax):
    """
    Overview: This function will create a 2 traces based on the number of
    entrances/ordinations per year.
    """

    fig = go.Figure([go.Scattergl()])
    #create dataframes based on ordinations and entrants
    entered = ax.groupby(["YearEntered"]).size().reset_index(name = "Frequency Year")
    ordained = ax.groupby(["YearOrdained"]).size().reset_index(name = "Frequency Year")
    fig.add_trace(go.Scatter( x = entered["YearEntered"],
                y = entered["Frequency Year"], mode = 'lines+markers'))
    fig.add_trace(go.Scatter( x = ordained["YearOrdained"],
                y = ordained["Frequency Year"], mode = 'lines+markers'))
    fig.show()
#==============================================================================

#==============================================================================
def dioceseTime(ax,diocese):
    """
    Overview: This function takes in a list of dicoese and plots a series of
    bar charts according to entrants per year
    """

    fig = go.Figure([go.Scattergl()])
    dicoese = diocese.split(",")
    #extract needed sections of ax and add a frequency column
    ax = ax.groupby(["YearEntered", "Diocese"]).size().reset_index(name="Diocese Frequency")

    #create a new trace for each dicoese
    for i in range(0,len(dicoese)):
        dio = ax.where(ax["Diocese"] == dicoese[i])
        year = dio["YearEntered"]
        freq = dio["Diocese Frequency"]
        fig.add_trace(go.Bar( x = year, y = freq, name = dicoese[i]))

        # Add range slider
        fig.update_layout(
            xaxis=go.layout.XAxis(
                rangeselector=dict(
                    buttons=list([
                        dict(count=100,
                             label="100y",
                             step="year",
                             stepmode="backward"),
                        dict(count=50,
                             label="50y",
                             step="year",
                             stepmode="backward"),
                        dict(count=20,
                             label="20y",
                             step="year",
                             stepmode="backward"),
                        dict(count=10,
                             label="10y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

    fig.show()
#==============================================================================

#==============================================================================
def nodeGraph(ax,c1,c2,wantToSee):
    """
    Overview: This function will plot a node graph based on a dataframe.
    Enter datframe column name 1 and 2, followed by the attributes of column 1
    you would like to see.
    """
    col1 = ax[c1].dropna(axis = 0, how = 'any', inplace = False).values.tolist()
    col2 = ax[c2].dropna(axis = 0, how = 'any', inplace = False).values.tolist()
    edgeList = list(zip(col1,col2))
    combined = []

    #option for user to easily inout "All" for all columns
    if wantToSee == "All":
        wantToSee = col1

    edgeListCol = [x[0] for x in edgeList]
    for i in range(0,len(edgeList)):
        if edgeListCol[i] in wantToSee:
            combined.append(edgeList[i])

    combined = set(combined)

    c1Filter, c2Filter = list(set(zip(*combined)))

    #constuct graph of filtered nodes
    filter = c1Filter + c2Filter
    G = nx.Graph()
    N = len(filter)
    labels = filter
    G.add_nodes_from(c1Filter)
    G.add_nodes_from(c2Filter)
    G.add_edges_from(combined)

    #position layout styles left here for convinience of swapping
    pos = nx.circular_layout(G)
    #pos = nx.bipartite_layout(G)
    #pos = nx.kamada_kawai_layout(G)
    #pos = nx.random_layout(G)
    #pos = nx.rescale_layout(G)
    #pos = nx.shell_layout(G)
    #pos = nx.spring_layout(G)
    #pos = nx.spectral_layout(G)

    #define edges and verticies
    Xv1=[pos[c1Filter[k]][0] for k in range(len(c1Filter))]
    Yv1=[pos[c1Filter[k]][1] for k in range(len(c1Filter))]

    Xv2=[pos[c2Filter[k]][0] for k in range(len(c2Filter))]
    Yv2=[pos[c2Filter[k]][1] for k in range(len(c2Filter))]

    Xed=[]
    Yed=[]

    for edge in combined:
        Xed+=[pos[edge[0]][0],pos[edge[1]][0], None]
        Yed+=[pos[edge[0]][1],pos[edge[1]][1], None]

    #trace layout
    trace1=Scatter(x=Xed,
                   y=Yed,
                   mode='lines',
                   line=dict(color='#cc1da3', width=0.25),
                   hoverinfo='none'
                   )

    trace2=Scatter(x=Xv1,
                   y=Yv1,
                   name = c1,
                   mode='markers',
                   marker=dict(symbol='circle-dot',
                                 size=5,
                                 color='#cc311d',
                                 line=dict(color='#cc311d', width=2)
                                 ),
                   text=c1Filter,
                   textposition="top center",
                   hoverinfo='text'
                   )

    trace3=Scatter(x=Xv2,
                   y=Yv2,
                   name = c2,
                   mode='markers',
                   marker=dict(symbol='circle-dot',
                                 size=5,
                                 color='#4ccc1d',
                                 line=dict(color='#4ccc1d', width=5)
                                 ),
                   text=c2Filter,
                   textposition="top center",
                   hoverinfo='text'
                   )


    data1=[trace1, trace2, trace3]
    fig1=Figure(data=data1)
    plio.write_html(fig1, "nodeGraph.html", include_plotlyjs = True)

    iplot(fig1)
#==============================================================================

#==============================================================================
def map(diocese):
    """
    Overview: Create a Ireland heatmap based on the number of clerics that were
    sent to that diocese upon becoming ordained.
    """
    #Create a frequency list/count of each diocese in the given dataframe
    count = Counter(diocese)
    freqDiocese = list(count.items())
    freqDiocese.sort()

    #read in the map shapefile and sort by diocese name
    geoMap = gpd.read_file("Census2011_Dioceses_generalised/Census2011_Dioceses_generalised/Census2011_Dioceses_generalised.shp")
    geoMap.sort_values("NAME", inplace = True)
    geoMapDiocese = list(set(geoMap["NAME"]))
    dioList = [x[0] for x in freqDiocese]

    #create a frequecy table based on diocese in the inpout dataframe that are also
    #part of the diocese in the shapefile
    freqFilter = []
    for i in range(0,len(dioList)):
        if dioList[i] in geoMapDiocese:
            freqFilter.append(freqDiocese[i])


    for i in range(0,len(geoMapDiocese)):
        if geoMapDiocese[i] not in [x[0] for x in freqFilter]:
            freqFilter.append((geoMapDiocese[i],0))
    freqFilter.sort()

    #seperate frequency from the freqfilter 2d list
    freq = [x[1] for x in freqFilter]
    geoMap["Frequency"] = freq
    #plot the data
    geoMap.plot(column = "Frequency", legend = True)
    plt.axis('off')
    plt.show()

#==============================================================================
