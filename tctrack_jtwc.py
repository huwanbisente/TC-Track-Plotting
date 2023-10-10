import re
from datetime import datetime

date_re = re.compile(r'.+\s([0-9]{4})')
typ_re = re.compile(r'([a-zA-Z0-9\- ]+)\s([a-zA-Z0-9\-]+)')
header_re = re.compile(r'ADV\s+LAT\s+LON\s+TIME\s+WIND\s+PR\s+STAT')
data_re = re.compile(r'\s+[0-9]+\s+([0-9]+\.[0-9]+)\s+([0-9]+.[0-9]+)\s+' \
                     r'([0-9]{2})/([0-9]{2})/([0-9]{2})Z\s+([0-9]{2})')
#data_re = re.compile(r'([0-9]{2})\/([0-9]{2})\/([0-9]{2})Z')



def timestamp(t):
    dt = datetime.strptime(t, "%Y%m%d%H")
    return dt


class TCTrack_JTWC(object):
    '''Tropical Cyclone Track Class JTWC.'''
    def __init__(self, jtwc_fmt):
        self.parse(jtwc_fmt)


    def parse(self, jtwc_fmt):
        jtwc_fmt = [l for l in jtwc_fmt.split('\n') if l]
        date_line = re.match(date_re, jtwc_fmt[0])
        if date_line:
            self.year = date_line.group(1)
            jtwc_fmt.pop(0)
            typ = re.match(typ_re, jtwc_fmt[0])
            self.name = typ.group(2)
            jtwc_fmt.pop(0)
            jtwc_fmt.pop(0)
            self.data = [(self.name,
                        timestamp(''.join([self.year, re.match(data_re, m).group(3),
                                  re.match(data_re, m).group(4),
                                  re.match(data_re, m).group(5)])),
                        float(re.match(data_re, m).group(1)),
                        float(re.match(data_re, m).group(2)),
                        int(re.match(data_re, m).group(6)),
                        'jtwc')
                       for m in jtwc_fmt if re.match(data_re, m)]
            self.start = self.data[0][0]
            self.end = self.data[-1][0]



def test():
    a = '''
Date: 20-26 DEC 2017
Typhoon-1 TEMBIN
ADV  LAT    LON      TIME     WIND  PR  STAT
  1   8.30  131.00 12/20/18Z   25     - TROPICAL DEPRESSION
  2   8.60  129.50 12/21/14Z    -     - TROPICAL DEPRESSION
  3   8.50  128.40 12/21/06Z   35     - TROPICAL STORM
  4   8.40  127.60 12/21/12Z   40     - TROPICAL STORM
  5   7.90  126.70 12/21/18Z   50     - TROPICAL STORM
  6   7.80  125.60 12/22/00Z   45     - TROPICAL STORM
  7   7.80  123.60 12/22/06Z   45     - TROPICAL STORM
  8   8.00  122.10 12/22/12Z   45     - TROPICAL STORM
  9   7.90  121.40 12/22/18Z   50     - TROPICAL STORM
 10   7.70  120.40 12/23/00Z   55     - TROPICAL STORM
 11   7.70  119.30 12/23/06Z   55     - TROPICAL STORM
 12   7.70  117.40 12/23/12Z   60     - TROPICAL STORM
 13   7.90  115.80 12/23/18Z   65     - TYPHOON-1
 14   8.20  114.30 12/24/00Z   75     - TYPHOON-1
 15   8.30  113.20 12/24/06Z   80     - TYPHOON-1
 16   8.50  111.80 12/24/12Z   80     - TYPHOON-1
 17   8.60  110.20 12/24/18Z   80     - TYPHOON-1
 18   8.00  109.90 12/25/00Z   65     - TYPHOON-1
 19   8.10  108.90 12/25/06Z   50     - TROPICAL STORM
 20   8.50  107.50 12/25/12Z   45     - TROPICAL STORM
 21   8.40  106.10 12/25/18Z   40     - TROPICAL STORM
 22   8.50  104.90 12/26/00Z   30     - TROPICAL DEPRESSION
 23   8.40  104.40 12/26/06Z   25     - TROPICAL DEPRESSION
'''
    t = TCTrack_JTWC(a)
    [print(d) for d in t.data]


def get_tracks(fname):
    with open(fname, 'r') as f:
        jtwc_fmt = f.readline()
        l = f.readline()
        while l:
            if not re.match(r'Date', l):
                jtwc_fmt += l
            else:
                yield TCTrack_JTWC(jtwc_fmt)
                jtwc_fmt = l
            l = f.readline()
        yield TCTrack_JTWC(jtwc_fmt)


#for x in get_tracks('jtwc_2017.txt'):
#    print(x.name)
#    for l in x.data:
#        print(l)
