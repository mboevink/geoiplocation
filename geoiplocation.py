import os

"""

Project idea from: http://chir.ag/projects/geoiploc/
Database: http://software77.net/geo-ip/history/

"""

last_modified = 0
geoipaddrfrom = []
geoipaddrupto = []

geoipcntryid = []
geoipcntryfull = {}
geocachelogger = {}


def load_ip_data(csv):
    global last_modified
    csv = csv if csv.endswith('.csv') else csv + '.csv'
    modification = os.path.getmtime(csv)
    if last_modified >= modification:
        return

    geoipaddrfrom.clear()
    geoipaddrupto.clear()
    geoipcntryid.clear()
    geoipcntryfull.clear()
    geocachelogger.clear()

    with open(csv, encoding='ISO-8859-1') as F:
        for l in F.readlines():
            if l.startswith('#'):
                continue

            start, finish, *_, code, __, country = l.replace('"', '').split(',')
            geoipaddrfrom.append(int(start))
            geoipaddrupto.append(int(finish))
            geoipcntryid.append(code)
            geoipcntryfull[code] = country.strip()

    last_modified = modification


def get_country(ip: str, full: bool = False, csv: str = 'countries.csv'):
    load_ip_data(csv)

    a, b, c, d = list(map(int, ip.split('.')))[::-1]
    ip = (a + (b * 256) + (c * 256 * 256) + (d * 256 * 256 * 256))
    if ip in geocachelogger:
        return geoipcntryfull[geocachelogger[ip]] if full else geocachelogger[ip]

    ct = 'ZZ'
    start = 0
    finish = len(geoipaddrupto)

    while finish > start:
        idx = start + ((finish - start) // 2)
        loip = geoipaddrfrom[idx]
        hiip = geoipaddrupto[idx]

        if loip <= ip and hiip >= ip:
            ct = geoipcntryid[idx]
            break

        elif loip > ip:
            if finish == idx:
                break
            finish = idx

        elif hiip < ip:
            if start == idx:
                break
            start = idx

    geocachelogger[ip] = ct
    return geoipcntryfull[ct] if full else ct
