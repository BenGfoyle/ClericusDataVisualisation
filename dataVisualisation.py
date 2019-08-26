#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thursday 18-July-2019

@author: BenGfoyle - github.com/bengfoyle
Overview: This program will retrieve data from a file and calculate
the mean, mode, median, and standard deviaiton.
Data plots will be included with a printed summary of data.
"""
import numpy as np#for mathematical functions
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import *
import pandas as pd #csv handler
import networkx as nx #network graphs
import matplotlib.pyplot as plt
from plotly.offline import plot, iplot
import os, sys

OPTIONS = '''
1. Read in New File
2. Make Network Graph
3. Make Graph of Ordinations Over Year
4. Make Graph of Diocese Over Time
5. Exit
'''

file = ""

#==============================================================================
def fileRead():
    """
    Overview: This function reads the text file and passes two
    lists back to the main method
    """
    file = input("Please enter the file you would like to read: ")
    #define lists and and file name, ISO-8859-1 for Irish characters
    file = pd.read_json(file, encoding='ISO-8859-1')
    file = file.transpose()
    # file.replace('', np.nan, inplace=True)
    # file = file.dropna(fileis = 0, how = 'any', thresh = None, subset = None,
    #             inplace = False)

    return file
#==============================================================================

#==============================================================================
def enteredAndOrdained():
    """
    Overview: This function will create a stacked chart based on the diocese
    entrances/ordinations per year.
    """

    fig = go.Figure([go.Scattergl()])
    #create dataframes based on ordinations and entrants
    entered = file.groupby(["YearEntered"]).size().reset_index(name = "Frequency Year")
    ordained = file.groupby(["YearOrdained"]).size().reset_index(name = "Frequency Year")
    fig.add_trace(go.Scatter( x = entered["YearEntered"],
                y = entered["Frequency Year"], mode = 'lines+markers'))
    fig.add_trace(go.Scatter( x = ordained["YearOrdained"],
                y = ordained["Frequency Year"], mode = 'lines+markers'))
    fig.show()
#==============================================================================

#==============================================================================
def dioceseTime():
    """
    Overview: This function takes in a list of dicoese and plots a series of
    bar charts according to entrants per year
    """

    diocese = input("Enter the diocese you would like to see seperated by commas.(Tuam,Dublin,Cork)")
    fig = go.Figure([go.Scattergl()])
    dicoese = diocese.split(",")
    print(len(diocese))
    #extract needed sections of file and add a frequency column
    file = file.groupby(["YearEntered", "Diocese"]).size().reset_index(name="Diocese Frequency")

    #create a new trace for each dicoese
    for i in range(0,len(dicoese)):
        dio = file.where(file["Diocese"] == dicoese[i])
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
def yearPlot():
    """
    Overview: This function takes in a list of dicoese and plots a series of
    bar charts according to entrants per year
    """

    year = input("Enter the year you would like to view.")
    fig = go.Figure([go.Scattergl()])
    #extract needed sections of file and add a frequency column
    fileFiltered = file.drop().where(file["YearEntered"] == year)
    #create a new trace for each dicoese
    for i in range(0,len(fileFiltered)):
        fig.add_trace(go.Bar( x = fileFiltered["Diocese"]))
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
def nodeGraph():
    """
    Overview: This function will plot a node graph based on a dataframe.
    """
    cols = input("Enter the columns you would like to see seperated by commas. (Name, Diocese)")
    cols = cols.split(",")
    wantToSee = input("What range of values from the first column would you like to see. (Tuam, Mayo, Dublin) ")
    col1 = [cols[0]].dropna(axis = 0, how = 'any', inplace = False).values.tolist()
    col2 = [cols[2]].dropna(axis = 0, how = 'any', inplace = False).values.tolist()
    edgeList = list(zip(col1,col2))
    combined = []

    if wantToSee == "All":
        wantToSee = col2

    for i in range(0,len(edgeList)):
        if edgeList[i][0] in wantToSee:
            combined.append(edgeList[i])

    # combined = set(combined)
    # c1Filter, c2Filter = list(set(zip(*combined)))

    c1Filter, c2Filter = list(zip(*combined))

    print(combined)
    filter = c1Filter + c2Filter

    G = nx.Graph()
    N = len(filter)
    labels = filter
    G.add_nodes_from(c1Filter)
    G.add_nodes_from(c2Filter)
    G.add_edges_from(combined)
    pos=nx.fruchterman_reingold_layout(G)

    Xv1=[pos[c1Filter[k]][0] for k in range(len(c1Filter))]
    Yv1=[pos[c1Filter[k]][1] for k in range(len(c1Filter))]

    Xv2=[pos[c2Filter[k]][0] for k in range(len(c2Filter))]
    Yv2=[pos[c2Filter[k]][1] for k in range(len(c2Filter))]

    Xed=[]
    Yed=[]
    for edge in combined:
        Xed+=[pos[edge[0]][0],pos[edge[1]][0], None]
        Yed+=[pos[edge[0]][1],pos[edge[1]][1], None]

    trace3=Scatter(x=Xed,
                   y=Yed,
                   mode='lines',
                   line=dict(color='#cc1da3', width=0.25),
                   hoverinfo='none'
                   )

    trace4=Scatter(x=Xv1,
                   y=Yv1,
                   name = c1,
                   mode='markers',
                   marker=dict(symbol='circle-dot',
                                 size=5,
                                 color='#cc311d',
                                 line=dict(color='#cc311d', width=5)
                                 ),
                   text=c1Filter,
                   textposition="top center",
                   hoverinfo='text'
                   )

    trace5=Scatter(x=Xv2,
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

    data1=[trace3, trace4, trace5]
    fig1=Figure(data=data1)
    iplot(fig1)
#==============================================================================

cmds = {
	"1" : fileRead,
	"2" : nodeGraph,
	"3" : yearPlot,
	"4" : dioceseTime,
	"5" : lambda: sys.exit(0)
}

#==============================================================================
def main():
    os.system('cls')
    try:
        while True:
            choice = input("\n%s" % OPTIONS)
            if choice not in cmds:
                print ('[!] Invalid Choice')
                continue
            elif choice == "1":
                file = cmds.get(choice)()
            else:
                cmds.get(choice)()
    except KeyboardInterrupt:
        print ('[!] Ctrl + C detected\n[!] Exiting')
        sys.exit(0)
    except EOFError:
        print ('[!] Ctrl + D detected\n[!] Exiting')
        sys.exit(0)

    #
    # fileName = input("Enter file name:")
    # clerics = fileRead(fileName)
    # i = 1
    # while(True):
    #     try:
    #         colIn = input("Enter columns you would like to view seperated by commas (Column1, Column2)")
    #         col = colIn.split(",")
    #         print(col)
    #         nodeGraph(clerics, col[0], col[1],"All")
    #         #dioceseTime(clerics,"Tuam,Meath,Dublin,Mayo,Letterkenny")
    #         enteredAndOrdained(clerics)
    #         #yearPlot(clerics,"1987")
    #     except:
    #         pass

#==============================================================================
if __name__ == '__main__':
    main()
