import tctrack as rsmc
import tctrack_jtwc as jtwc

#tracks = [x for x in rsmc.get_tracks('bst_2017_july.txt')] + \
#         [x for x in jtwc.get_tracks('jtwc_2017.txt')]

tracks = list(rsmc.get_tracks('tracks_2023.txt'))

for i, track in enumerate(tracks):
    content = ','.join(['name', 'ts', 'lat', 'lon', 'ws', 'src']) + '\n'
    for name, ts, lat, lon, ws, src in track.data:
        if ws:
            content += ','.join(map(str, [name, ts, lat, lon, int(ws), src])) + '\n'
        else:
            content += ','.join(map(str, [name, ts, lat, lon, 999, src])) + '\n'
        with open(str(i+1) + '_' + name + '.csv', 'w') as f:
            f.write(content)
