import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

data = pd.read_csv('cfs-2012-pumf-csv/cfs_2012_pumf_csv.txt')
coords = pd.read_csv('cities_with_lat_lng.csv')
coords['MA_ID'] = np.arange(len(coords))

filt = (data["MODE"] == 3) | (data["MODE"] == 4) | (data["MODE"] == 5)
d1 = data[filt]
d2 = data.groupby(["ORIG_MA", "DEST_MA"])["SHIPMT_VALUE"].sum()
d3 = pd.DataFrame(d2).reset_index()

# merge eliminates 9999 and 0000 codes
d4 = pd.merge(d3, coords, left_on = 'ORIG_MA', right_on = 'code')
d5 = pd.merge(d4, coords, left_on = 'DEST_MA', right_on = 'code')
d5.rename(columns = {'lat_x' : 'lat_orig', 'lng_x' : 'lng_orig', 'lat_y' : 'lat_dest', 'lng_y' : 'lng_dest', 'MA_ID_y' : 'MA_ID_dest'}, inplace = True)
d6 = d5.filter(['ORIG_MA', 'DEST_MA', 'SHIPMT_VALUE', 'lat_orig', 'lng_orig', 'lat_dest', 'lng_dest', 'MA_ID_dest'])

d7 = d6[d6['ORIG_MA'] != d6['DEST_MA']]
d8 = d7.sort_values("SHIPMT_VALUE")
d8['VAL_M'] = d8["SHIPMT_VALUE"] / 1000000
d9 = d8.round({'VAL_M': 0})
d10 = d9[d9['VAL_M'] >= 1]

nframes = 1000
d10['frame_int'] = np.ceil(nframes / d10['VAL_M'])

#frames = np.zeros(nframes)

frames = []
for b in np.arange(nframes):
    frames.append([])
    
for index, row in d10.iterrows():
    rand_start = np.random.randint(0,row['frame_int'])
    for a in np.arange(nframes):
        if (a + rand_start) % row['frame_int'] == 0:
            frames[a].append([row["lat_orig"],
                              row["lng_orig"],
                              row["lat_dest"],
                              row["lng_dest"],
                              row["lat_orig"], # curr lat
                              row["lng_orig"], # curr lng
                              0,
                              row["MA_ID_dest"]])
            

aframes = []
active = []
n = 0
for f in np.arange(len(frames) + 100):
    n += 1
    # delete
    for (a,b) in enumerate(active):
        if b[6] >= 1:
            #print(active[a])
            ###### DOUBLE CHECK THIS BEHAVIOR
            active.pop(a)
            #active[a] = [0,0,0,0,0,0,0]
            #print(a)
            pass
        else:
            active[a][4] = active[a][6]*(active[a][2] - active[a][0]) + active[a][0]
            active[a][5] = active[a][6]*(active[a][3] - active[a][1]) + active[a][1]
            active[a][6] += 0.01
    # advance
    # add new
    if f < len(frames) and frames[f] != []:
        for ff in frames[f]:
            active.append(ff)
    np_arr = np.array(active)
    aframes.append([np_arr[:,5],np_arr[:,4],np_arr[:,7]])
    # if n == 700:
    #     break

# np_arr = np.array(active)
# plt.scatter(np_arr[:,4],np_arr[:,5])
# plt.show()
    


#from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from random_cmap import rand_cmap



## TODO
## RANDOMIZE START TIMES
## ADD 10 EXTRA FRAMES TO THE END TO LET ALL POINTS ARRIVE
## DELETE HONOLULU
## REPLACE BACKGROUND IMAGE

img = plt.imread("background_map.png")

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

#rcp = rand_cmap(69, type='bright', first_color_black=False, last_color_black=False)

fig, ax = plt.subplots(figsize=(30,15))
plt.subplots_adjust(left=0.03,right=0.97,bottom=0.03,top=0.97)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

ax.imshow(img, extent=(-130, -69, 24, 50))
xdata, ydata = [], []
ln = plt.scatter([], [])
#init()

def init():
    ax.set_ylim(24, 50)
    ax.set_xlim(-130, -69)   
    return ln,

#init(img)

def update(frame_id, all_frames):
    #xdata.append(frame)
    #ydata.append(np.sin(frame))
    print(frame_id)
    plt.cla()
    
    ax.set_ylim(24, 50)
    ax.set_xlim(-130, -69)
    ax.imshow(img, extent=(-130, -69, 24, 50))  
    #ln.set_data(40+ frame_id,-100)
    #ln.set_data(all_frames[frame_id][0], all_frames[frame_id][1])
    ln = plt.scatter(all_frames[frame_id][0],
                   all_frames[frame_id][1],
                   c=all_frames[frame_id][2],
                   vmin=0,
                   vmax=69,
                   cmap = 'tab20',
                   linewidths=1,
                   edgecolors='black') 
    #ln.set_set_label(all_frames[frame_id][0])
    return ln


ani = animation.FuncAnimation(fig, update, frames=np.arange(nframes + 100), fargs=(aframes,), init_func=init)
#plt.show()
    
#ani.save('transport_1.gif', writer="ffmpeg")

#ani.FFMpegWriter(fps=5, codec=None, bitrate=None, extra_args=None, metadata=None)
ani.save('im.mp4', writer=writer)    

# https://matplotlib.org/3.2.1/api/animation_api.html

#d3 = data.groupby(["ORIG_CFS_AREA"])["SHIPMT_VALUE"].sum()

# for orig, dest in d2.index:
#     print(orig, dest)
    
