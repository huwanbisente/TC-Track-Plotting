import re
import random
from datetime import datetime

header_re = re.compile(r'[0-9]{5}\s+' \
                       r'([0-9]{4})\s+' \
                       r'[0-9]{1,3}\s+' \
                       r'[0-9]{0,4}\s+' \
                       r'[0-9]{4}\s+' \
                       r'[0-9]{1}\s+' \
                       r'[0-9]{1}\s+' \
                       r'([A-Z\-/]{0,20})\s+' \
                       r'[0-9]{8}')

data_re = re.compile(r'^([0-9]{8})\s+' \
                     r'[0-9]{3}\s+' \
                     r'[0-9]{1}\s+' \
                     r'([0-9]{2,3})\s+' \
                     r'([0-9]{3,4})\s+' \
                     r'[0-9]{3,4}\s+' \
                     r'([0-9]{0,4})')

def timestamp(t):
    dt = datetime.strptime(t, "%y%m%d%H")
    if dt.year >= 2050:
        dt = dt.replace(year=dt.year-100)
    return dt

class TCTrack(object):
    '''Tropical Cyclone Track Class.'''
    def __init__(self, rsmc_fmt):
        self.parse(rsmc_fmt)


    def parse(self, rsmc_fmt):
        rsmc_fmt = [l for l in rsmc_fmt.split('\n') if l]
        header = re.match(header_re, rsmc_fmt[0])
        if header:
            self.id = header.group(1)
            self.name = header.group(1)
            if header.group(2):
                self.name = header.group(2)
            self.fullname = '_'.join(filter(lambda x: x, [header.group(1),
                                  header.group(2)]))
            rsmc_fmt.pop(0)
            self.data = [(self.name,                                   # name
                          timestamp(re.match(data_re, m).group(1)),    # ts
                          float(re.match(data_re, m).group(2))/10,     # lat
                          float(re.match(data_re, m).group(3))/10,     # lon
                          re.match(data_re, m).group(4),               # ws in kt
                          'jma')                                       # src
                         for m in rsmc_fmt if re.match(data_re, m)]
            self.start = self.data[0][1]
            self.end = self.data[-1][1]


def test():
    a = '''
66666 1701  027 0004 1701 0 6                MUIFA              20170609
17042218 002 2 086 1439 1006     000
17042300 002 2 092 1432 1006     000
17042306 002 2 099 1424 1006     000
17042312 002 2 106 1417 1006     000
17042318 002 2 112 1408 1006     000
17042400 002 2 118 1397 1006     000
17042406 002 2 121 1388 1004     000
17042412 002 2 124 1382 1004     000
17042418 002 2 125 1375 1004     000
17042500 002 2 127 1370 1004     000
17042506 002 2 128 1366 1004     000
17042512 002 2 129 1364 1004     000
17042518 002 3 131 1360 1002     035     00000 0000 20120 0090
17042600 002 3 132 1357 1002     035     00000 0000 20120 0090
17042606 002 3 136 1348 1002     035     00000 0000 20120 0090
17042612 002 3 140 1344 1002     035     00000 0000 20120 0090
17042618 002 3 144 1344 1002     035     00000 0000 20120 0090
17042700 002 3 148 1344 1002     035     00000 0000 20120 0090
17042706 002 2 159 1347 1004     000
17042712 002 2 170 1347 1006     000
17042718 002 2 178 1348 1006     000
17042800 002 2 184 1355 1008     000
17042806 002 2 190 1363 1008     000
17042812 002 2 199 1377 1008     000
17042818 002 2 208 1390 1008     000
17042900 002 2 215 1402 1008     000
17042906 002 2 227 1418 1008     000
'''
    t = TCTrack(a)
    [print(d) for d in t.data]


def get_tracks(fname):
    with open(fname, 'r') as f:
        rsmc_fmt = f.readline()
        l = f.readline()
        while l:
            if not re.match(r'66666', l):
                rsmc_fmt += l
            else:
                yield TCTrack(rsmc_fmt)
                rsmc_fmt = l
            l = f.readline()
        yield TCTrack(rsmc_fmt)


def get_random_track(fname):
    with open(fname, 'r') as f:
        rsmc_fmt = f.readline()
        l = f.readline()
        counter = 0
        target = random.randrange(1000)
        while l:
            if not re.match(r'66666', l):
                rsmc_fmt += l
            else:
                if counter == target:
                    return TCTrack(rsmc_fmt)
                counter += 1
                rsmc_fmt = l
            l = f.readline()



if __name__ == '__main__':
#    for t in get_tracks('bst_all.txt'):
#        print("{} - {}".format(t.start, t.end))
    t = get_random_track('tracks_2023.txt')
    print(','.join(['name', 'ts', 'lat', 'lon', 'ws', 'src']))
    for name, date, lat, lon, ws, src in t.data:
        if ws:
            print(','.join(map(str, [name, date, lat, lon, int(ws), src])))
        else:
            print(','.join(map(str, [name, date, lat, lon, 999, src])))
