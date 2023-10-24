import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import shapely.geometry as sgeom

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

#from tctrack import get_random_track, get_tracks
import tctrack as rsmc
import tctrack_jtwc as jtwc

import random

import re

def get_random_color():
    return '#' + ''.join([random.choice('0123456789abcdef') for _ in range(6)])


def get_geometries(attr, attr_param, ax):
    """Get Hi-Res geometries of countries defined by attr and attr_param."""
    shp = shpreader.Reader(shpreader.natural_earth(resolution='50m',
                                                   category='cultural',
                                                   name='admin_0_countries'))

    def attr_filter(c):
        return c.attributes[attr] == attr_param

    return [c.geometry for c in filter(attr_filter, shp.records())], \
        ccrs.PlateCarree()._as_mpl_transform(ax)


def offset_coord(coord, pcoord, amnt):
    if pcoord - coord > 0:
        return pcoord + amnt
    else:
        return pcoord - amnt

def offset_text(coord, pcoord):
    if pcoord - coord > 0:
        return 'left'
    else:
        return 'right'


def is_inside(lon, lat, lonmin, lonmax, latmin, latmax):
    return (lonmin < lon < lonmax) & (latmin < lat < latmax)

def generate_tctrack(tctrack):
    plt.figure(figsize=(16, 16), dpi=92)

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([90, 145, -15, 35], ccrs.Geodetic())
    ax.gridlines()
    ax.set_xticks([90, 105, 120, 135], crs=ccrs.PlateCarree())
    ax.set_yticks([-15, 0, 15, 30], crs=ccrs.PlateCarree())

    #world, transform = get_geometries('featurecla', 'Admin-0 country', ax)
    #for c in world:
    #    ax.add_geometries([c], ccrs.PlateCarree(), facecolor='none',
    #                      edgecolor='black', linewidth=0.5)

    ax.coastlines(resolution='50m', color='black', linewidth=1.0)

    lonlat = [(lon, lat) for n, t, lat, lon, ws, src  in tctrack.data]
    track = sgeom.LineString(lonlat)

    ax.add_geometries([track], ccrs.PlateCarree(), facecolor='none',
                      edgecolor='teal', linewidth=1.5)

    for i, (n, t, lat, lon, ws, src) in enumerate(tctrack.data):
        if i == 0:
            plt.plot(lon, lat, 'wD', transform=ccrs.Geodetic())

        elif i == 1:
            if is_inside(plon, plat, 90, 143, -15, 35):
                plt.text(offset_coord(lon, plon, 1),
                         offset_coord(lat, plat, 1),
                         tctrack.name,
                         fontsize=8,
                         horizontalalignment=offset_text(lon, plon),
                         bbox={'facecolor':'white', 'pad':3},
                         transform=ccrs.Geodetic())
                plt.text(offset_coord(lon, plon, 1),
                         offset_coord(lat, plat, 2),
                         tctrack.start.strftime('%d/%b'),
                         fontsize=8,
                         ha=offset_text(lon, plon),
                         transform=ccrs.Geodetic())
            else:
                plt.text(145.5, plat,
                         tctrack.name,
                         fontsize=8,
                         bbox={'facecolor':'white', 'pad':3},
                         transform=ccrs.Geodetic())
                plt.text(145.5,
                         offset_coord(lat, plat, 1.25),
                         tctrack.start.strftime('%d/%b'),
                         fontsize=8,
                         transform=ccrs.Geodetic())


        elif i == len(tctrack.data) - 1:
            plt.plot(lon, lat, 'kx', transform=ccrs.Geodetic())
            if is_inside(lon, lat, 90, 143, -15, 35):
                plt.text(offset_coord(plon, lon, 1),
                         offset_coord(plat, lat, 1),
                         tctrack.end.strftime('%d/%b'),
                         fontsize=8,
                         ha=offset_text(lon, plon),
                         transform=ccrs.Geodetic())

        else:
            if t.hour == 0:
                plt.plot(lon, lat, 'wo', transform=ccrs.Geodetic())
                if is_inside(lon, lat, 90, 143, -15, 35):
                    if t.day == 1:
                        plt.text(lon,
                                 offset_coord(plat, lat, 1),
                                 t.strftime('%d/%b'),
                                 fontsize=5,
                                 ha='center',
                                 transform=ccrs.Geodetic())
                    else:
                        plt.text(lon,
                                 offset_coord(plat, lat, 1),
                                 t.strftime('%d/'),
                                 fontsize=5,
                                 ha='center',
                                 transform=ccrs.Geodetic())

            elif t.hour == 12:
                plt.plot(lon, lat, 's', color='teal', transform=ccrs.Geodetic())

        plon, plat = lon, lat

    plt.text(0.0225, 0.975, ' '.join(['Tropical Cyclone',
             re.sub(r'_', r' ', tctrack.fullname)]),
             fontsize=12, va='top',
             bbox={'facecolor':'white', 'pad':5},
             transform=ax.transAxes)

    plt.text(0.0225, 0.0225, '{} - {}'.format(
             tctrack.start.strftime('%d %b %Y %Hz'),
             tctrack.end.strftime('%d %b %Y %Hz')),
             fontsize=12, va='bottom',
             bbox={'facecolor':'white', 'pad':5},
             transform=ax.transAxes)

    plt.text(0.90, 0.0225, 'PLOT: PAGASA\nDATA: JMA',
             fontsize=8, va='bottom',
             bbox={'facecolor':'white', 'pad':3},
             transform=ax.transAxes)


    plt.savefig(''.join((re.sub(r'/', r'-', tctrack.fullname), '.png')), bbox_inches='tight')
    #plt.show()

    plt.close()


def generate_tctracks(tctracks):
#    plt.figure(figsize=(16, 16), dpi=92)
#    ax = plt.axes(projection=ccrs.PlateCarree())#central_longitude=120.0))
#    ax.set_extent([90, 145, -15, 35], ccrs.Geodetic())
#    ax.gridlines()
    plt.figure(figsize=(8, 8), dpi=180)

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([90, 145, -15, 35], ccrs.Geodetic())
    ax.gridlines()
    ax.set_xticks([90, 105, 120, 135], crs=ccrs.PlateCarree())
    ax.set_yticks([-15, 0, 15, 30], crs=ccrs.PlateCarree())



    world, transform = get_geometries('featurecla', 'Admin-0 country', ax)
    for c in world:
        ax.add_geometries([c], ccrs.PlateCarree(), facecolor='yellowgreen',
                          edgecolor='black', linewidth=1.0)

    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'ocean', '50m', facecolor='skyblue'))

    for idx, tctrack in enumerate(tctracks):
        print(tctrack.data)
        lonlat = [(x, y) for _, _, y, x, _, _  in tctrack.data]
        track = sgeom.LineString(lonlat)
        track_color = get_random_color()


        plt.text(-0.28, 0.99 - 0.035*idx, str(idx+1), fontsize=8, va='top', ha='right',
                 bbox={'facecolor':'none', 'pad':2},
                 transform=ax.transAxes)


        plt.text(-0.27, 0.99 - 0.035*idx, tctrack.name + ' ' +
                 tctrack.start.strftime('%d/%b') + ' - ' +
                 tctrack.end.strftime('%d/%b'),
                 fontsize=8, va='top', color=track_color,
                 bbox={'facecolor':'none', 'edgecolor':'none','pad':2},
                 transform=ax.transAxes)


        ax.add_geometries([track], ccrs.PlateCarree(), facecolor='none',
                          edgecolor=track_color, linewidth=1.5)

        for i, (n, t, lat, lon, spd, src) in enumerate(tctrack.data):
            if i == 0:
#                plt.plot(lon, lat, 'wD', transform=ccrs.Geodetic())
#            elif i == 1:
#                if is_inside(plon, plat, 90, 143, -15, 35):
#                    plt.text(offset_coord(lon, plon, 1),
#                             offset_coord(lat, plat, 1),
#                             str(idx),
#                             fontsize=8,
#                             horizontalalignment=offset_text(lon, plon),
#                             bbox={'facecolor':'white', 'pad':3},
#                             transform=ccrs.Geodetic())
                if is_inside(lon, lat, 90, 144, -15, 35):
                    if idx != 15:
                        plt.text(lon, lat, str(idx+1), fontsize=8, bbox={'facecolor':'white', 'pad':3},
                                 transform=ccrs.Geodetic())
                    else:
                        plt.text(lon, lat-1, str(idx+1), fontsize=8, bbox={'facecolor':'white', 'pad':3},
                                 transform=ccrs.Geodetic())

                else:
                    plt.text(145.5, lat,
                             str(idx+1),
                             fontsize=8,
                             bbox={'facecolor':'white', 'pad':3},
                             transform=ccrs.Geodetic())


            elif i == len(tctrack.data) - 1:
                plt.plot(lon, lat, 'kx', transform=ccrs.Geodetic())
            plon, plat = lon, lat


    #ax.background_patch.set_visible(False)
    #ax.outline_patch.set_visible(False)

    plt.text(0.0225, 0.975, 'Tropical Cyclone Tracks Jul - Dec 2018',
             fontsize=12, va='top',
             bbox={'facecolor':'white', 'pad':5},
             transform=ax.transAxes)

    plt.text(0.8, 0.035, 'PLOT: PAGASA\nDATA: JMA',
             fontsize=8, va='bottom',
             bbox={'facecolor':'white', 'pad':3},
             transform=ax.transAxes)


    plt.savefig(''.join(('2018_1H_tracks', '.png')), bbox_inches='tight')

    plt.close()


#generate_tctrack(rsmc.get_random_track('bst_all.txt'))

#for tctrack in rsmc.get_tracks('bst_2018.txt'):
#    generate_tctrack(tctrack)

generate_tctracks(list(rsmc.get_tracks('tracks_2023.txt')))
#generate_tctracks([x for x in rsmc.get_tracks('bst_2017_july.txt')] + [x for x in jtwc.get_tracks('jtwc_2017.txt')])
