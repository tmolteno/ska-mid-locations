#
# Example plotting of the SKA co-ordinates from the CSV file
#
# Author. Tim Molteno tim@physics.otago.ac.nz 
#
# (c) GPL v3
#
import csv
import numpy as np
import matplotlib.pyplot as plt


import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.img_tiles import Stamen
from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter,
                                LatitudeLocator, LongitudeLocator)


def read_positions(fname = 'ska1-mid.csv'):
    '''
        Load the wgs84 coordinates from the CSV file
    '''
    positions = []
    names = []

    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                name, lat, lon = row
                positions.append([lat, lon])
                names.append(name)
            else:
                print(f"Headers: {row}")
            line_count += 1
    positions = np.array(positions, dtype=np.float64)

    lon = positions.T[1]
    lat = positions.T[0]

    return lat, lon 


def plot_ska(lonmin, lonmax, latmin, latmax, plot_terrain=False):
    '''
        Plot the positions on a map bounded by the lon and lat limits specified.
    '''
    fig = plt.figure(dpi=100)
    
    ax = fig.add_subplot(1, 1, 1, 
                         projection=ccrs.LambertAzimuthalEqualArea(
                                                    central_longitude=np.mean(lon), 
                                                    central_latitude=np.mean(lat)))
    ax.set_title('SKA1-mid antenna locations')
    
    
    ax.set_extent([lonmin, lonmax, latmin, latmax], crs=ccrs.PlateCarree())

    gl = ax.gridlines(crs=ccrs.PlateCarree(), 
                      draw_labels=True,
                      linewidth=1, color='gray', alpha=0.5, 
                      linestyle='--')


    ax.plot(lon, lat, '.',
            color='blue', linewidth=1, alpha=0.5,
            markersize=4,
            transform=ccrs.Geodetic())

    if plot_terrain:
        tiler = Stamen('terrain-background')
        mercator = tiler.crs
        ax.add_image(tiler, 6)
    #ax.add_feature(cfeature.LAND)
    #ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

if __name__=="__main__":
    lat, lon = read_positions()
    plot_ska(-20, 55, 40, -37)
    plt.savefig('ska1_mid_africa.pdf')
    print("Plot saved as: ska1_mid_africa.pdf")
