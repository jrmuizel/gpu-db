import re
import collections
lines = []
lines += open("r600_pci_ids.h").readlines()
#lines += open("radeonsi_pci_ids.h").readlines()
lines += open("r200_pci_ids.h").readlines()
lines += open("r300_pci_ids.h").readlines()
cards = collections.defaultdict(list)
for l in lines:
    k = re.match("CHIPSET\((0x[0-9A-Fa-f]*),.*, *(.*)\)", l)
    if k:
        cards[k.group(2)] += [format(int(k.group(1), 16), 'x')]
    else:
        # radeonsi_pci_ids.h has only two parameters to CHIPSET so handle it
        # separately
        k = re.match("CHIPSET\((0x[0-9A-Fa-f]*), (.*)\)", l)
        if k:
            cards[k.group(2)] += [format(int(k.group(1), 16), 'x')]

import urllib2
response = urllib2.urlopen('https://cgit.freedesktop.org/drm/drm/plain/drivers/gpu/drm/amd/amdgpu/amdgpu_drv.c')
html = response.read()
for line in html.splitlines():
     if re.match(".*PCI_ANY_ID,.*", line):
         separated = re.split("[ ,{}\t|]", line)
         separated = list(filter(None, separated))
         #print separated[1], separated[6][len("CHIP_"):]
         device_id = format(int(separated[1], 16), 'x')
         device_name = separated[6][len("CHIP_"):]
         if device_id not in cards[device_name]:
             cards[device_name] += [device_id]


chips = """
    case CHIP_R300:
    case CHIP_R350:
    case CHIP_RV350:
    case CHIP_RV370:
    case CHIP_RV380:
    case CHIP_RS400:
    case CHIP_RC410:
    case CHIP_RS480:
        ws->info.chip_class = R300;
        break;
    case CHIP_R420:     /* R4xx-based cores. */
    case CHIP_R423:
    case CHIP_R430:
    case CHIP_R480:
    case CHIP_R481:
    case CHIP_RV410:
    case CHIP_RS600:
    case CHIP_RS690:
    case CHIP_RS740:
        ws->info.chip_class = R400;
        break;
    case CHIP_RV515:    /* R5xx-based cores. */
    case CHIP_R520:
    case CHIP_RV530:
    case CHIP_R580:
    case CHIP_RV560:
    case CHIP_RV570:
        ws->info.chip_class = R500;
        break;
    case CHIP_R600:
    case CHIP_RV610:
    case CHIP_RV630:
    case CHIP_RV670:
    case CHIP_RV620:
    case CHIP_RV635:
    case CHIP_RS780:
    case CHIP_RS880:
        ws->info.chip_class = R600;
        break;
    case CHIP_RV770:
    case CHIP_RV730:
    case CHIP_RV710:
    case CHIP_RV740:
        ws->info.chip_class = R700;
        break;
    case CHIP_CEDAR:
    case CHIP_REDWOOD:
    case CHIP_JUNIPER:
    case CHIP_CYPRESS:
    case CHIP_HEMLOCK:
    case CHIP_PALM:
    case CHIP_SUMO:
    case CHIP_SUMO2:
    case CHIP_BARTS:
    case CHIP_TURKS:
    case CHIP_CAICOS:
        ws->info.chip_class = EVERGREEN;
        break;
    case CHIP_CAYMAN:
    case CHIP_ARUBA:
        ws->info.chip_class = CAYMAN;
        break;
    case CHIP_TAHITI:
    case CHIP_PITCAIRN:
    case CHIP_VERDE:
    case CHIP_OLAND:
    case CHIP_HAINAN:
        ws->info.chip_class = SI;
        break;
    case CHIP_BONAIRE:
    case CHIP_KAVERI:
    case CHIP_KABINI:
    case CHIP_HAWAII:
    case CHIP_MULLINS:
        ws->info.chip_class = CIK;
        break;
    }
"""
import sys
chip = collections.OrderedDict()
chip['RAGE'] = collections.OrderedDict()
chip['RAGE']['RAGE'] = ['4742','4744','4749','474d','474f','4750','4752','4753','4754','4755','4757','4757','4759','475a','4c4d','4c52','5046','5050','5052','5245','5246','524b','524c','5346','534d','5446','5452']
chip['R100'] = collections.OrderedDict()
# 515e is ES 1000
chip['R100']['R100'] = ['4336','4337','4c57','4c58','4c59','5157','5144','5159','515a','515e']
chip['R200'] = collections.OrderedDict()
for i in ('R200', 'RV250', 'RV280', 'RS300'):
    chip['R200'][i] =  cards[i]
    del cards[i]
chip_group = []
for l in chips.split('\n'):
    m = re.search("CHIP_([A-Z0-9]*):", l)
    if m:
        chip_group += [m.group(1)]
    else:
        m = re.search("class = ([A-Z0-9]*);", l)
        if m:
            chip[m.group(1)] = collections.OrderedDict()
            for g in chip_group:
                chip[m.group(1)][g] = cards[g]
                del cards[g]
            chip_group = []
chip['CARRIZO'] = collections.OrderedDict()

for i in ('CARRIZO',):
    chip['CARRIZO'][i] =  cards[i]
    del cards[i]
chip['VI'] = collections.OrderedDict()
for i in ('TONGA','TOPAZ', 'FIJI', 'STONEY', 'POLARIS10', 'POLARIS11', 'POLARIS12', 'VEGAM'):
    chip['VI'][i] =  cards[i]
    del cards[i]
chip['GFX9'] = collections.OrderedDict()
for i in ('VEGA10','VEGA12', 'VEGA20', 'RAVEN', 'RENOIR', 'ARCTURUS', 'ALDEBARAN'):
    chip['GFX9'][i] =  cards[i]
    del cards[i]
chip['GFX10'] = collections.OrderedDict()
for i in ('NAVI10','NAVI12', 'NAVI14'):
    chip['GFX10'][i] =  cards[i]
    del cards[i]
chip['GFX10_3'] = collections.OrderedDict()
for i in ('SIENNA_CICHLID','NAVY_FLOUNDER', 'VANGOGH', 'DIMGREY_CAVEFISH', 'BEIGE_GOBY', 'YELLOW_CARP', 'CYAN_SKILLFISH'):
    chip['GFX10_3'][i] = cards[i]
    del cards[i]
chip['GFX11'] = collections.OrderedDict()
if len(cards) != 0:
    print cards
    assert len(cards) == 0

lines = open("amd-pci.ids").readlines()
for l in lines:
    if re.match("\t\t", l):
        # we don't need subsys
        continue
    m = re.match("\t([0-9a-f]+)  ([A-Za-z0-9 ]+)", l)
    if m:
        chipset = m.group(2)
        
        #gen = generation(chip)
        if chipset == "Navi 31 ":
            chip['GFX11']['NAVI31'] = m.group(1)
        #print m.group(1), chip
import json
print json.dumps({'1002': chip},indent=4, separators=(',', ': '))
#print cards

