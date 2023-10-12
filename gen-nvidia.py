import re
import collections
cards = collections.OrderedDict()

# initialize some generations so the json ends up in the right order
for i in ("NV1", "NV3", "NV4", "NV10", "NV20", "NV30", "NV40", "Tesla", "Tesla2", "Fermi", "Kepler", "Maxwell", "Pascal", "Volta", "Turing"):
    cards[i] = collections.OrderedDict()

def generation(chip):
    if chip[0:2] == "GK":
        return "Kepler"
    if chip[0:4] == "GRID":
        return "Kepler"
    if chip[0:2] == "GM":
        return "Maxwell"
    if chip[0:2] == "GP":
        return "Pascal"
    if chip[0:2] == "GV":
        return "Volta"
    if chip[0:2] == "GA":
        return "Ampere"
    if chip[0:2] == "AD":
        return "Ada"
    if chip[0:2] == "GN":
        return "Ada"
    if chip[0:3] == "GT2":
        return "Tesla2"
    if re.match("MCP89", chip):
        return "Tesla2"
    if chip[0:2] == "GT":
        return "Tesla"
    if chip[0:2] == "TU":
        return "Turing"
    if re.match("G8[0-9]", chip):
        return "Tesla"
    if re.match("G9[0-9]", chip):
        return "Tesla"
    if chip == "C79" or chip == "C78" or chip == "C77" or chip == "C73" or chip == "MCP79":
        return "Tesla"
    if chip[0:2] == "GF":
        return "Fermi"
    if chip == "NV1":
        return "NV1"
    if chip == "NV3":
        return "NV3"
    if chip == "NV4":
        return "NV4"
    if chip == "NV0A":
        return "NV4"
    if chip == "NV5":
        return "NV4"
    if re.match("NV1[0-9]", chip):
        return "NV10"
    if chip == "C17":
        return "NV10"
    if re.match("NV2[0-9]", chip):
        return "NV20"
    if re.match("NV3[0-9]", chip):
        return "NV30"
    if re.match("NV4[0-9]", chip):
        return "NV40"
    if chip == "C61":
        return "NV40"
    if chip == "C51" or chip == "C51G" or chip == "C51PV":
        return "NV40"
    if chip == "C68" or chip == "C67":
        return "NV40"
    if re.match("G7[0-3]", chip):
        return "NV40"
    if re.match("G7[0-9]", chip):
        return "Tesla"
    if chip == "ION" or chip == "MCP7A":
        return "Tesla"


lines = open("pci.ids").readlines()
for l in lines:
    if re.match("\t\t", l):
        # we don't need subsys
        continue
    if re.search("MCP", l) and not re.search("GeForce", l):
        continue
    else:
        if re.search("Audio", l):
            continue
        if re.search("Ethernet", l):
            continue
        if re.search("Memory Controller", l):
            continue
        if re.search("ATA Controller", l):
            continue
        if re.search("USB.*Controller", l):
            continue
        if re.search("UCSI Controller", l):
            continue
        if re.search("Host Bridge", l):
            continue
        if re.search("ISA Bridge", l):
            continue
        if re.search("PCI Express Bridge", l):
            continue
        if re.search("CK804", l):
            continue

        #gpu = re.search("GeForce|Quadro|NV4|Tesla|Riva|NV1|NV5", l)
        #if not gpu:
        #    print l
        m = re.match("\t([0-9a-f]+)  ([A-Z0-9]+)", l)
        if m:
            chip = m.group(2)
            gen = generation(chip)

            if re.search("RTX 3070 TI Engineering Sample", l):
                gen = "Ampere"
                chip = "GA104"
            if gen:
                if not gen in cards:
                    cards[gen] = collections.OrderedDict()
                if not chip in cards[gen]:
                    cards[gen][chip] = []
                cards[gen][chip] += [m.group(1)]
            else:
                import sys
                print >> sys.stderr, m.group(2), l
        #else:
        #    print l
cards["NV10"]["NV11"] += ["01a0"] #nForce 220/420 NV11
import json
print json.dumps({'10de': cards},indent=4, separators=(',', ': '))
