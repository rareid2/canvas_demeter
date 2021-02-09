import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

from readDEMETER import find_files, get_data_from_parsed
from plots import plot_spectrogram, plot_TD, plot_map

import cartopy.crs as ccrs

datapath = '/home/rileyannereid/workspace/canvas_demeter/data/all_data'
parsed_files = find_files(datapath)

for fo in parsed_files:
    if '1131' in fo:
        data = get_data_from_parsed(fo)

st_date = data['packet 0']['time']
en_date = st_date + dt.timedelta(seconds=30)

d_unit = 'mV/m'
# be sure to change the divide by 1e3 too!
fig = plt.figure(figsize=(6, 8))
E_TD = plt.subplot(2, 1, 1)
#E_FD = plt.subplot(3, 1, 2)

projection=ccrs.PlateCarree()
E_map = plt.subplot(2, 1, 2, projection=projection)

plot_map(E_map, projection, data, st_date, en_date)
plot_TD(E_TD, data, st_date, en_date,d_unit)
#plt.show()

fig.suptitle('DEMETER Burst Data at ' + dt.datetime.strftime(st_date, '%Y-%m-%d %H:%M:%S'))
plt.savefig('/home/rileyannereid/workspace/canvas_demeter/data/bursts_pngs/' + dt.datetime.strftime(st_date, '%Y%m%d_%H%M') + '_TD_EFIELD')

#plot_spectrogram(data, st_date, en_date, d_unit)

