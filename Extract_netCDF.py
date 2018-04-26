## This script is based on python 2.7
## Primary objective of this script was to extract daily rainfall data
## ..for a particular catchment area in Australia from AWAP rainfall
## ..dataset (in netCDF) that contains gridded rainfall data for 
## ..entire Australia at 5km-daily resolution.
## It can be used to extract timeseries data for a rectangular area
## ..by inputting lat-lon of four coordinates of the area.

## Caution: After extracting data for one site, the extracted file should be
## ..removed from the current directory before extracting for another site. 

import numpy as np
import netCDF4 as nc

#### === User-inputs ====#####
one = nc.Dataset('pre.1950.nc') ##load one of your nc datafiles
print one.variables ## Check variables names, say my variable names are lat, lon, pre

## Name of the variables
lat_name = 'lat'
lon_name = 'lon'
time_name = 'time'
data_name = 'pre'

## Select spatial range for which data to be extracted
mylat1 = -33.1628952
mylat2 = -31.43701935
mylon1 = 150.46339417
mylon2 = 152.37350464

##Give a name of your extracted datafile and define units
newfilename = 'Extracted_Data' 
time_unit = 'day'
lat_unit = 'degrees_south'
lon_unit = 'degrees_east'
data_unit = 'mm'


#### ======= Rest of the Code is Automated ========######

##Find pixel-range based on the provided lat-lon
lat = one.variables[lat_name][:]
lon = one.variables[lon_name][:]

ver_pix = []
for i in xrange(0, len(lat)):
    if lat[i] >= mylat1 and lat[i] <= mylat2:
        ver_pix.append(i)

y_min = min(ver_pix)
y_max = max(ver_pix)
print lat[min(ver_pix):max(ver_pix)]


hor_pix = []
for j in xrange(0,len(lon)):
    if lon[j] >= mylon1 and lon[j] <= mylon2:
        hor_pix.append(j)

x_min = min(hor_pix)
x_max = max(hor_pix)
print lon[min(hor_pix):max(hor_pix)]

check_range = one.variables[data_name][:,y_min:y_max,x_min:x_max]  ##pre:lat:lon = time,y,x
#print check_range
print check_range.shape


## Load all nc files in the directory from which data to be extracted
## ..for the selected area
f = nc.MFDataset('*.nc') 
alldata = f.variables[data_name][:,y_min:y_max,x_min:x_max]
lat1 = one.variables[lat_name][y_min:y_max]
lon1 = one.variables[lon_name][x_min:x_max]
#time = one.variables[time_name][:]

ncfile = nc.Dataset(''+str(newfilename)+'.nc','w')

ncfile.createDimension(time_name,len(alldata))
ncfile.createDimension(lat_name,len(lat1))
ncfile.createDimension(lon_name,len(lon1))

time = ncfile.createVariable(time_name,np.dtype('float32').char,(time_name,))
lats = ncfile.createVariable(lat_name,np.dtype('float32').char,(lat_name,))
lons = ncfile.createVariable(lon_name,np.dtype('float32').char,(lon_name,))

time.units = time_unit
lats.units = lat_unit
lons.units = lon_unit
time[:] = np.linspace(1,len(alldata),len(alldata))
lats[:] = lat1
lons[:] = lon1

newdata = ncfile.createVariable(data_name,np.dtype('float32').char,(time_name,lat_name,lon_name))
newdata.units = data_unit 
newdata[:] = alldata[:]


ncfile.close()
