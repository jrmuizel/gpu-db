import json
nv = open("amd.json").read()
from collections import OrderedDict
nv = json.loads(nv, object_pairs_hook=OrderedDict)
devices = []
for ven in nv.iteritems():
    gen_devices = set()
    for gen in ven[1].iteritems():
        for chip in gen[1].iteritems():
            for dev in chip[1]:
                idev = int(dev, base=16)
                devices.append([idev, gen[0], chip[0]])
for d in sorted(devices):
    up = d[0] >> 8
    good = False
    """
    if d[0] >= 0x6600 and d[0] < 0x66b0:
        good = True
    if d[0] >= 0x6700 and d[0] < 0x6720:
        good = True
    if d[0] >= 0x6780 and d[0] < 0x6840:
        good = True
    if d[0] >= 0x6860 and d[0] < 0x6880:
        good = True
    if d[0] >= 0x6900 and d[0] < 0x6a00:
        good = True
    if d[0] == 0x7300:
        good = True
    if d[0] == 0x684c:
        good = True
    if d[0] >= 0x9830 and d[0] < 0x9870:
        good = True
    if d[0] >= 0x9900 and d[0] < 0x9a00:
        good = True
    """
    # Evergreen
    if d[0] >= 0x6840 and d[0] <= 0x684b:
        good = True
    if d[0] >= 0x6850 and d[0] <= 0x685f:
        good = True
    if d[0] >= 0x6880 and d[0] <= 0x68ff:
        good = True
    if d[0] >= 0x9800 and d[0] <= 0x980a:
        good = True
    if d[0] >= 0x9640 and d[0] <= 0x964f:
        good = True
    if d[0] >= 0x6720 and d[0] <= 0x677f:
        good = True

    if not good:
        print hex(d[0]), d[1], d[2]
