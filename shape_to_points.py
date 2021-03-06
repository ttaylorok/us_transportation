import shapefile
import pandas as pd
import networkx as nx
import numpy as np


sf = shapefile.Reader("tl_2016_us_primaryroads/tl_2016_us_primaryroads.shp")
#w = shapefile.Writer('tl_2017_us_state_modified')
fout = open("points.csv",'w')

# convert shapefile to points
points = []
for shaperec in sf.iterShapeRecords():
    shp = shaperec.shape.points
    for p in shp:
        points.append([np.round(p[0],1),np.round(p[1],1)])
    
df = pd.DataFrame(points, columns = ["long","lat"])
df.drop_duplicates(inplace = True)
df['node_id'] = np.arange(len(df.index))
df.to_csv("points_every_p1_deg.csv")

# create edges by finding nearby points
edges = []
for i1,row1 in df.iterrows():
    for i2,row2 in df.iterrows():
        dist = np.sqrt(pow(row1['lat']-row2['lat'],2) + pow(row1['long']-row2['long'],2))
        if dist <= 0.3:
            edges.append((row1['node_id'],row2['node_id'],dist))
            
G=nx.Graph()

G.add_nodes_from(df["node_id"])

dfe = pd.DataFrame(edges)
dfe.to_csv('edges_output.csv')
            
G.add_weighted_edges_from(edges)

d = nx.dijkstra_path(G,32,5267)

d2 = np.array(d).astype('int')

df2 = pd.DataFrame(d2, columns = ['node_id'])

df3 = pd.merge(df2, df, on = 'node_id')

df3.to_csv('shortest_path.csv')
    





#FG.add_weighted_edges_from([(1,2,0.125),(1,3,0.75),(2,4,1.2),(3,4,0.375)])


    
              


