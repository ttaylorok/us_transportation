import shapefile
import pandas as pd

sf = shapefile.Reader("tl_2016_us_primaryroads/tl_2016_us_primaryroads.shp")
#w = shapefile.Writer('tl_2017_us_state_modified')
fout = open("points.csv",'w')

points = []
for shaperec in sf.iterShapeRecords():
    shp = shaperec.shape.points
    for p in shp:
        points.append(p)
    
df = pd.DataFrame(points, columns = ["long","lat"])
df.to_csv("points.csv")
    
            
    
    
    



