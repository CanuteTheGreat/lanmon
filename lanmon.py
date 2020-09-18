#!/usr/bin/env python3

import argparse
from configparser import ConfigParser
import psycopg2
import scapy.all


# if a mac already exists, check that it has the same ip, if not alert 

debug = True

def dprint(var):
    if debug:
        print("\n\nDEBUGGING:")
        print(var)
        print(":DEBUGGING\n\n")

def lanmonsetup(conf):
    global lanmonversion 
    lanmonversion = "0.16"

    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + lanmonversion)
    parser.add_argument('-c', '--conf', '--config', action="store", dest="configfile", default='lanmon.conf')

    # parse the args
    args = parser.parse_args()
    filename = args.configfile 

    if conf == 'main':
        config = mainconfig(filename, 'main')
    elif conf == 'db':
        config = dbconfig(filename, 'database')
    return config

def mainconfig(filename, section):
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

def dbconfig(filename, section):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to main
    dbcfg = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            dbcfg[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return dbcfg

def netscanner(ip):
    request = scapy.all.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.all.ARP(pdst=ip)
    ans, unans = scapy.all.srp(request, timeout=2, retry=1)
    results = []
    for sent, received in ans:
        results.append({'IP': received.psrc, 'MAC': received.hwsrc})
    return(results)

def dbcompare(scan, dbconf):
    # FIXME: finish
    #dprint(scan)
    conn = None
    row = ""
    try:
        # read database configuration
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**dbconf)
        # create a cursor object for execution
        cur = conn.cursor()
        # another way to call a function
        cur.execute("select * from nodes;")
        # process the result set
        row = cur.fetchone()

        query = """INSERT into nodes (ip, mac) values (%s, %s)"""

        if row == None:
            print("database is empty, adding entries")
            for machine in scan:
                #print(machine['MAC'])
                cur.execute(query, (machine['IP'], machine['MAC']))
        else:
            print("database is not empty, comparing entries")
            for scanmachine in scan:
                for dbmachine in row:
                    # FIXME: see if it exists or not

        # commit the data to database
        conn.commit()
        # close the communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()    

def main():
    mainconf = lanmonsetup('main')
    dbconf = lanmonsetup('db')

    # scan network
    netscan = netscanner(mainconf['net']) 
    #dprint(netscan)

    #for mapping in netscan:
    #    print('{} ==> {}'.format(mapping['IP'], mapping['MAC']))


    # compare netscan with what is in the database
    dbcompare(netscan, dbconf)

if __name__ == "__main__":
    main()

