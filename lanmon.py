#!/usr/bin/env python3

import argparse
from configparser import ConfigParser
import psycopg2

# get args
# need network ip range (i.e. 10.0.0.0/24)
# need output file
# ??

 
# output file will be:
# mac|ip|first seen|last seen

# if a mac already exists, check that it has the same ip, if not alert 

lanmonversion = "0.16"

def readargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + lanmonversion)
    parser.add_argument('-c', '--conf', '--config', action="store", dest="configfile", default='lanmon.conf')

    # parse the args
    args = parser.parse_args()
    filename = args.configfile 

    conf = lanmonconfig(filename, 'main')

    print(conf)


    quit()
    return("10.0.0.1/24") # FIXME: test

def lanmonconfig(filename, section):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to main
    lanmoncfg = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            lanmoncfg[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return lanmoncfg


def netscan(ip):
    # FIXME: finish
    print("test")

def main():
    # FIXME: finish
    ip = readargs()
    print("ip:", ip)
    #netscan(ip) 

if __name__ == "__main__":
    main()

