#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
import json
import time
import os
import os.path
import optparse
import sys
from datetime import date

###########################################################################


class OptionParser (optparse.OptionParser):

    def check_required(self, opt):
        option = self.get_option(opt)

        # Assumes the option's 'default' is set to None!
        if getattr(self.values, option.dest) is None:
            self.error("%s option not supplied" % option)


###########################################################################
def check_rename(tmpfile, options):

    with open(tmpfile) as f_tmp:
        try:
            tmp_data = json.load(f_tmp)
            print("Result is a text file (might come from a wrong password file)")
            print(tmp_data)
            sys.exit(-1)
        except ValueError:
            pass

    os.rename("%s" % tmpfile, "%s/%s.zip" % (options.write_dir, prod))
    print("product saved as : %s/%s.zip" % (options.write_dir, prod))

###########################################################################


def parse_catalog(search_json_file):
    # Filter catalog result
    with open(search_json_file) as data_file:
        data = json.load(data_file)

    if 'ErrorCode' in data:
        print(data['ErrorMessage'])
        sys.exit(-2)

    # Sort data
    download_dict = {}
    storage_dict = {}
    for i in range(len(data["features"])):
        prod = data["features"][i]["properties"]["productIdentifier"]
        print(prod, data["features"][i]["properties"]["storage"]["mode"])
        feature_id = data["features"][i]["id"]
        try:
            storage = data["features"][i]["properties"]["storage"]["mode"]
            platform = data["features"][i]["properties"]["platform"]
            # recup du numero d'orbite
            orbitN = data["features"][i]["properties"]["orbitNumber"]
            if platform == 'S1A':
                # calcul de l'orbite relative pour Sentinel 1A
                relativeOrbit = ((orbitN-73) % 175)+1
            elif platform == 'S1B':
                # calcul de l'orbite relative pour Sentinel 1B
                relativeOrbit = ((orbitN-27) % 175)+1

            #print data["features"][i]["properties"]["productIdentifier"],data["features"][i]["id"],data["features"][i]["properties"]["startDate"],storage

            if options.orbit != None:
                if platform.startswith('S2'):
                    if prod.find("_R%03d" % options.orbit) > 0:

                        download_dict[prod] = feature_id
                        storage_dict[prod] = storage
                elif platform.startswith('S1'):
                    if relativeOrbit == options.orbit:
                        download_dict[prod] = feature_id
                        storage_dict[prod] = storage
            else:
                download_dict[prod] = feature_id
                storage_dict[prod] = storage
        except:
            pass
    return(prod, download_dict, storage_dict)

# ===================== MAIN
# ==================
# parse command line
# ==================
if len(sys.argv) == 1:
    prog = os.path.basename(sys.argv[0])
    print('      '+sys.argv[0]+' [options]')
    print("     Aide : ", prog, " --help")
    print("        ou : ", prog, " -h")
    print("example 1 : python %s -l 'Toulouse' -a peps.txt -d 2016-12-06 -f 2017-02-01 -c S2ST" % sys.argv[0])
    print("example 2 : python %s --lon 1 --lat 44 -a peps.txt -d 2015-11-01 -f 2015-12-01 -c S2" % sys.argv[0])
    print("example 3 : python %s --lonmin 1 --lonmax 2 --latmin 43 --latmax 44 -a peps.txt -d 2015-11-01 -f 2015-12-01 -c S2" %
          sys.argv[0])
    print("example 4 : python %s -l 'Toulouse' -a peps.txt -c SpotWorldHeritage -p SPOT4 -d 2005-11-01 -f 2006-12-01" %
          sys.argv[0])
    print("example 5 : python %s -c S1 -p GRD -l 'Toulouse' -a peps.txt -d 2015-11-01 -f 2015-12-01" % sys.argv[0])
    sys.exit(-1)
else:
    usage = "usage: %prog [options] "
    parser = OptionParser(usage=usage)

    parser.add_option("-l", "--location", dest="location", action="store", type="string",
                      help="town name (pick one which is not too frequent to avoid confusions)", default=None)
    parser.add_option("-a", "--auth", dest="auth", action="store", type="string",
                      help="Peps account and password file")
    parser.add_option("-w", "--write_dir", dest="write_dir", action="store", type="string",
                      help="Path where the products should be downloaded", default='.')
    parser.add_option("-c", "--collection", dest="collection", action="store", type="choice",
                      help="Collection within theia collections", choices=['S1', 'S2', 'S2ST', 'S3'], default='S2')
    parser.add_option("-p", "--product_type", dest="product_type", action="store", type="string",
                      help="GRD, SLC, OCN (for S1) | S2MSI1C S2MSI2Ap (for S2)", default="")
    parser.add_option("-m", "--sensor_mode", dest="sensor_mode", action="store", type="string",
                      help="EW, IW , SM, WV (for S1) | INS-NOBS, INS-RAW (for S2)", default="")
    parser.add_option("-n", "--no_download", dest="no_download", action="store_true",
                      help="Do not download products, just print curl command", default=False)
    parser.add_option("-d", "--start_date", dest="start_date", action="store", type="string",
                      help="start date, fmt('2015-12-22')", default=None)
    parser.add_option("--lat", dest="lat", action="store", type="float",
                      help="latitude in decimal degrees", default=None)
    parser.add_option("--lon", dest="lon", action="store", type="float",
                      help="longitude in decimal degrees", default=None)
    parser.add_option("--latmin", dest="latmin", action="store", type="float",
                      help="min latitude in decimal degrees", default=None)
    parser.add_option("--latmax", dest="latmax", action="store", type="float",
                      help="max latitude in decimal degrees", default=None)
    parser.add_option("--lonmin", dest="lonmin", action="store", type="float",
                      help="min longitude in decimal degrees", default=None)
    parser.add_option("--lonmax", dest="lonmax", action="store", type="float",
                      help="max longitude in decimal degrees", default=None)
    parser.add_option("-o", "--orbit", dest="orbit", action="store", type="int",
                      help="Orbit Path number", default=None)
    parser.add_option("-f", "--end_date", dest="end_date", action="store", type="string",
                      help="end date, fmt('2015-12-23')", default='9999-01-01')
    parser.add_option("--json", dest="search_json_file", action="store", type="string",
                      help="Output search JSON filename", default=None)

    (options, args) = parser.parse_args()

if options.search_json_file == None or options.search_json_file == "":
    options.search_json_file = 'search.json'

if options.location is None:
    if options.lat == None or options.lon == None:
        if options.latmin == None or options.lonmin == None or options.latmax == None or options.lonmax == None:
            print("provide at least a point or rectangle")
            sys.exit(-1)
        else:
            geom = 'rectangle'
    else:
        if options.latmin == None and options.lonmin == None and options.latmax == None and options.lonmax == None:
            geom = 'point'
        else:
            print("please choose between point and rectangle, but not both")
            sys.exit(-1)

else:
    if options.latmin == None and options.lonmin == None and options.latmax == None and options.lonmax == None and options.lat == None or options.lon == None:
        geom = 'location'
    else:
        print("please choose location and coordinates, but not both")
        sys.exit(-1)

# geometric parameters of catalog request
if geom == 'point':
    query_geom = 'lat=%f\&lon=%f' % (options.lat, options.lon)
elif geom == 'rectangle':
    query_geom = 'box={lonmin},{latmin},{lonmax},{latmax}'.format(
        latmin=options.latmin, latmax=options.latmax, lonmin=options.lonmin, lonmax=options.lonmax)
elif geom == 'location':
    query_geom = "q=%s" % options.location

# date parameters of catalog request
if options.start_date != None:
    start_date = options.start_date
    if options.end_date != None:
        end_date = options.end_date
    else:
        end_date = date.today().isoformat()

# special case for Sentinel-2

if options.collection == 'S2':
    if options.start_date >= '2016-12-05':
        print("**** products after '2016-12-05' are stored in Tiled products collection")
        print("**** please use option -c S2ST")
        time.sleep(5)
    elif options.end_date >= '2016-12-05':
        print("**** products after '2016-12-05' are stored in Tiled products collection")
        print("**** please use option -c S2ST to get the products after that date")
        print("**** products before that date will be downloaded")
        time.sleep(5)

if options.collection == 'S2ST':
    if options.end_date < '2016-12-05':
        print("**** products before '2016-12-05' are stored in non-tiled products collection")
        print("**** please use option -c S2")
        time.sleep(5)
    elif options.start_date < '2016-12-05':
        print("**** products before '2016-12-05' are stored in non-tiled products collection")
        print("**** please use option -c S2 to get the products before that date")
        print("**** products after that date will be downloaded")
        time.sleep(5)

#====================
# read authentification file
#====================
try:
    f = open(options.auth)
    (email, passwd) = f.readline().split(' ')
    if passwd.endswith('\n'):
        passwd = passwd[:-1]
    f.close()
except:
    print("error with password file")
    sys.exit(-2)


if os.path.exists(options.search_json_file):
    os.remove(options.search_json_file)


#====================
# search in catalog
#====================
if (options.product_type == "") and (options.sensor_mode == ""):
    search_catalog = 'curl -k -o %s https://peps.cnes.fr/resto/api/collections/%s/search.json?%s\&startDate=%s\&completionDate=%s\&maxRecords=500' % (
        options.search_json_file, options.collection, query_geom, start_date, end_date)
else:
    search_catalog = 'curl -k -o %s https://peps.cnes.fr/resto/api/collections/%s/search.json?%s\&startDate=%s\&completionDate=%s\&maxRecords=500\&productType=%s\&sensorMode=%s' % (
        options.search_json_file, options.collection, query_geom, start_date, end_date, options.product_type, options.sensor_mode)


print(search_catalog)
os.system(search_catalog)
time.sleep(5)

prod, download_dict, storage_dict = parse_catalog(options.search_json_file)

#====================
# Download
#====================


if len(download_dict) == 0:
    print("No product matches the criteria")
else:
    # first try for the products on tape
    if options.write_dir == None:
        options.write_dir = os.getcwd()

    for prod in list(download_dict.keys()):
        file_exists = os.path.exists(("%s/%s.SAFE") % (options.write_dir, prod)
                                     ) or os.path.exists(("%s/%s.zip") % (options.write_dir, prod))
        if (not(options.no_download) and not(file_exists)):
            if storage_dict[prod] == "tape":
                tmticks = time.time()
                tmpfile = ("%s/tmp_%s.tmp") % (options.write_dir, tmticks)
                print("\nStage tape product: %s" % prod)
                get_product = 'curl -o %s -k -u %s:%s https://peps.cnes.fr/resto/collections/%s/%s/download/?issuerId=peps &>/dev/null' % (
                    tmpfile, email, passwd, options.collection, download_dict[prod])
                os.system(get_product)

    NbProdsToDownload = len(list(download_dict.keys()))
    print("##########################")
    print("%d  products to download" % NbProdsToDownload)
    print("##########################")
    while (NbProdsToDownload > 0):
       # redo catalog search to update disk/tape status
        if (options.product_type == "") and (options.sensor_mode == ""):
            search_catalog = 'curl -k -o %s https://peps.cnes.fr/resto/api/collections/%s/search.json?%s\&startDate=%s\&completionDate=%s\&maxRecords=500' % (
                options.search_json_file, options.collection, query_geom, start_date, end_date)
        else:
            search_catalog = 'curl -k -o %s https://peps.cnes.fr/resto/api/collections/%s/search.json?%s\&startDate=%s\&completionDate=%s\&maxRecords=500\&productType=%s\&sensorMode=%s' % (
                options.search_json_file, options.collection, query_geom, start_date, end_date, options.product_type, options.sensor_mode)

        os.system(search_catalog)
        time.sleep(2)

        prod, download_dict, storage_dict = parse_catalog(options.search_json_file)

        NbProdsToDownload = 0
        # download all products on disk
        for prod in list(download_dict.keys()):
            file_exists = os.path.exists(("%s/%s.SAFE") % (options.write_dir, prod)
                                         ) or os.path.exists(("%s/%s.zip") % (options.write_dir, prod))
            if (not(options.no_download) and not(file_exists)):
                if storage_dict[prod] == "disk":
                    tmticks = time.time()
                    tmpfile = ("%s/tmp_%s.tmp") % (options.write_dir, tmticks)
                    print("\nDownload of product : %s" % prod)
                    get_product = 'curl -o %s -k -u %s:%s https://peps.cnes.fr/resto/collections/%s/%s/download/?issuerId=peps' % (
                        tmpfile, email, passwd, options.collection, download_dict[prod])
                    print(get_product)
                    os.system(get_product)
                    # check binary product, rename tmp file
                    if not os.path.exists(("%s/tmp_%s.tmp") % (options.write_dir, tmticks)):
                        NbProdsToDownload += 1
                    else:
                        check_rename(tmpfile, options)

            elif file_exists:
                print("%s already exists" % prod)

        # download all products on tape
        for prod in list(download_dict.keys()):
            file_exists = os.path.exists(("%s/%s.SAFE") % (options.write_dir, prod)
                                         ) or os.path.exists(("%s/%s.zip") % (options.write_dir, prod))
            if (not(options.no_download) and not(file_exists)):
                if storage_dict[prod] == "tape":
                    tmticks = time.time()
                    tmpfile = ("%s/tmp_%s.tmp") % (options.write_dir, tmticks)
                    print("\nDownload of product : %s" % prod)
                    get_product = 'curl -o %s -k -u %s:%s https://peps.cnes.fr/resto/collections/%s/%s/download/?issuerId=peps' % (
                        tmpfile, email, passwd, options.collection, download_dict[prod])
                    print(get_product)
                    os.system(get_product)
                    if not os.path.exists(("%s/tmp_%s.tmp") % (options.write_dir, tmticks)):
                        NbProdsToDownload += 1
                    else:
                        check_rename(tmpfile, options)

        if NbProdsToDownload > 0:
            print("##############################################################################")
            print("%d remaining products are on tape, lets's wait 2 minutes before trying again" % NbProdsToDownload)
            print("##############################################################################")
            time.sleep(120)
