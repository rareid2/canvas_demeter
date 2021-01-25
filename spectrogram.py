
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import datetime as dt

from readDEMETER import find_files, get_data_from_parsed

datapath = '/home/rileyannereid/workspace/canvas_demeter/data/all_data'
parsed_files = find_files(datapath)

for fo in parsed_files:
    data = get_data_from_parsed(fo) # change this to be all files w .DATp

entime = dt.datetime.now()
print(entime - sttime)

# now let's make a spectrogram!
# we only need data between 21:04:40 and 21:05:10 -- 30 seconds

# going to need a full time array 

#def combine_packets(data_dict):  

#combine_packets(data)
fs = 40000.
tds = int(1e6/fs) # microseconds
T_array = []
E_array = []

for i in range(int(len(data))):
    packetn = 'packet ' + str(i)
    time = data[packetn]['time']
    
    for m in range(int(len(data[packetn]['Edata']))):
        T_array.append(time + dt.timedelta(microseconds=tds)) 
        E_array.append(data[packetn]['Edata'][m])

T_array = np.array(T_array)
T_stamp = [(t - dt.datetime(1970,1,1)) for t in T_array]
T_stamp = np.array(T_stamp)

# find data in region of interest
st_date = dt.datetime(2005, 8, 4, 20, 3, 50, 0)
en_date = dt. datetime(2005, 8, 4, 20, 4, 20, 0)

st_date1 = (st_date - dt.datetime(1970, 1, 1))
en_date1 = (en_date - dt.datetime(1970, 1, 1))

st_idx = (np.abs(T_stamp - st_date1)).argmin()
en_idx = (np.abs(T_stamp - en_date1)).argmin()
print(st_idx,en_idx)
T_array = np.array(T_array[st_idx:en_idx+1])
E_array = np.array(E_array[st_idx:en_idx+1])


overlap = 0.5
nfft = 8192
window = 'hanning'

ff, tt, FE = scipy.signal.spectrogram(E_array, fs=fs, window=window,
                                    nperseg=nfft, mode='psd', scaling='density')
E_mag = np.log10(FE)
pcm = plt.pcolormesh(tt, ff/1e3, E_mag, cmap='jet', vmin=-3.5, vmax=1.5)
cbar = plt.colorbar(pcm)
cbar.set_label('log(uV^2/m^2/Hz)')
plt.title('0709 Spectrogram')
plt.xlabel('seconds after ' + str(T_array[0]))
plt.ylabel('Frequency [kHz]')
plt.savefig('0709_Inan2007.png')
plt.close()


plt.plot(T_array, E_array/1e3)
plt.xlabel('time')
plt.ylabel('E amp mV/m')
plt.title('0804 Time Domain Burst')
plt.savefig('0804_timedomain.png')
plt.close()
