import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

import matplotlib.animation as animation
# from random_cmap import rand_cmap

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

data = pd.read_csv('cfs-2012-pumf-csv/cfs_2012_pumf_csv.txt')
coords = pd.read_csv('cities_with_lat_lng.csv')
coords = coords[coords['code'] != 46520]
coords['MA_ID'] = np.arange(len(coords))



points = pd.read_csv("points_every_p1_deg.csv")

coords['node_id'] = 0
for i1,row1 in coords.iterrows():
    dist_curr = 9999
    nit = -1
    for i2, row2 in points.iterrows():
        dist_new = np.sqrt(pow(row1['lat']-row2['lat'],2) + pow(row1['lng']-row2['long'],2))
        if dist_new < dist_curr:
            dist_curr = dist_new
            nit = row2['node_id']
    coords.loc[i1,'node_id'] = int(nit)

filt = (data["MODE"] == 3) | (data["MODE"] == 4) | (data["ORIG_MA"] != 46520) | (data["DEST_MA"] != 46520)
d1 = data[filt]
d2 = data.groupby(["ORIG_MA", "DEST_MA"])["SHIPMT_VALUE"].sum()
d3 = pd.DataFrame(d2).reset_index()




d4 = pd.merge(d3, coords, left_on = 'ORIG_MA', right_on = 'code')
d5 = pd.merge(d4, coords, left_on = 'DEST_MA', right_on = 'code')
d5.rename(columns = {'lat_x' : 'lat_orig',
                     'lng_x' : 'lng_orig',
                     'lat_y' : 'lat_dest',
                     'lng_y' : 'lng_dest',
                     'MA_ID_y' : 'MA_ID_dest'}, inplace = True)
d6 = d5.filter(['ORIG_MA',
                'DEST_MA',
                'SHIPMT_VALUE',
                'lat_orig',
                'lng_orig',
                'lat_dest',
                'lng_dest',
                'node_id_x',
                'node_id_y',
                'MA_ID_dest'])

# create graph from points and edges
G=nx.Graph()
G.add_nodes_from(points["node_id"])
dfe = pd.read_csv('edges_output.csv')            
G.add_weighted_edges_from(dfe[['0','1','2']].to_numpy())

# calculate dictionary of shortest paths
points.set_index('node_id', inplace = True)
paths = {}
for i,row in d6.iterrows():
    path =  nx.dijkstra_path(G,row['node_id_x'],row['node_id_y'])
    # the key of each path is the "origin-destination"
    p = str(int(row['node_id_x'])) + '-' + str(int(row['node_id_y']))
    pc = []
    for c in path:
        pc.append([points.loc[c,'lat'],points.loc[c,'long']])
    paths[p] = pc
    
    
    
d7 = d6[d6['ORIG_MA'] != d6['DEST_MA']]
d8 = d7.sort_values("SHIPMT_VALUE")
d8['VAL_M'] = d8["SHIPMT_VALUE"] / 1000000
d9 = d8.round({'VAL_M': 0})
d10 = d9[d9['VAL_M'] >= 1]

nframes = 1000
d10['frame_int'] = np.ceil(nframes / d10['VAL_M'])

# initialize frames
frames = []
for b in np.arange(nframes):
    frames.append([])
 
# populate frames, used for spawning new points
for index, row in d10.iterrows():
    rand_start = np.random.randint(0,row['frame_int'])
    for a in np.arange(nframes):
        if (a + rand_start) % row['frame_int'] == 0:
            frames[a].append([row["node_id_x"], # origin
                              row["node_id_y"], # destination
                              0, # lat
                              0, # lon
                              1, # pos
                              row["MA_ID_dest"]])
            
n_end_frames = 250
aframes = []
active = []
# establish movement of points
for f in np.arange(len(frames) + n_end_frames):
    for (a,b) in enumerate(active):
        path_id = str(int(b[0])) + '-' + str(int(b[1]))       
        if b[4] >= len(paths[path_id]):
            # delete points that have arrived at their destination
            active.pop(a)
            pass
        else:
            # advance points in their path
            active[a][2] = paths[path_id][active[a][4]][0]
            active[a][3] = paths[path_id][active[a][4]][1]
            active[a][4] += 1
    # spawn new points
    if f < len(frames) and frames[f] != []:
        for ff in frames[f]:
            active.append(ff)
    # take snapshot of points
    # continue until there are no more active points
    if active != []:
        np_arr = np.array(active)
        aframes.append([np_arr[:,2],np_arr[:,3],np_arr[:,5]])
    else:
        break
        
        



# set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

# initialize plot
fig, ax = plt.subplots(figsize=(30,15))
plt.subplots_adjust(left=0.03,right=0.97,bottom=0.03,top=0.97)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

# plot background image
img = plt.imread("us_with_borders.png")
ax.imshow(img, extent=(-127, -65, 24, 51))
xdata, ydata = [], []
ln = plt.scatter([], [])

def init():
    ax.set_ylim(24, 51)
    ax.set_xlim(-127, -65)   
    return ln,

def update(frame_id, all_frames):
    plt.cla()   
    ax.set_ylim(24, 51)
    ax.set_xlim(-127, -65) 
    ax.imshow(img, extent=(-127, -65, 24, 51))
    ln = plt.scatter(all_frames[frame_id][1],
                   all_frames[frame_id][0],
                   c=all_frames[frame_id][2],
                   vmin=0,
                   vmax=69,
                   cmap = 'tab20',
                   linewidths=1,
                   edgecolors='black') 
    return ln

# animate and save
ani = animation.FuncAnimation(fig, update, frames=np.arange(len(aframes)), fargs=(aframes,), init_func=init)
ani.save('im_with_roads_v2.mp4', writer=writer)   
    

