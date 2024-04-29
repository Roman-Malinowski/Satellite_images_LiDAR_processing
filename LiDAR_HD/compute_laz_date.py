from datetime import datetime, timedelta
import os
import sys

import numpy as np
import pandas as pd
import laspy

root = sys.argv[1]
laz_file = sys.argv[2]

source_time = datetime(2011, 9, 14, 0, 0, 0)

df = pd.DataFrame(columns=["laz_file", "point_count", "min_time", "max_time", "med_time", "med_x", "med_y", "min_x", "min_y", "max_x", "max_y"])

laz = laspy.read(os.path.join(root, laz_file))
# list(laz_1.point_format.dimension_names)
pc = laz.header.point_count

min_delta = np.min(laz['gps_time'])
max_delta = np.max(laz['gps_time'])
med_delta = np.median(laz['gps_time'])

min_time = source_time + timedelta(seconds=np.floor(min_delta))
max_time = source_time + timedelta(seconds=np.ceil(max_delta))
med_time = source_time + timedelta(seconds=np.ceil(med_delta))


min_x = np.min(laz['X'])
max_x = np.max(laz['X'])
med_x = np.median(laz['X'])


min_y = np.min(laz['Y'])
max_y = np.max(laz['Y'])
med_y = np.median(laz['Y'])

df.loc[0, ["laz_file", "point_count", "min_time", "max_time", "med_time",  "med_x", "med_y", "min_x", "min_y", "max_x", "max_y"]] = [laz_file, pc, min_time, max_time, med_time, med_x, med_y, min_x, min_y, max_x, max_y]

df.to_csv(os.path.join(root, "csv_data", laz_file + ".csv"))