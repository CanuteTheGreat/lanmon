#!/usr/bin/env python3

import argparse

# get args
# need network ip range (i.e. 10.0.0.0/24)
# need output file
# ??

 
# output file will be:
# mac|ip|first seen|last seen

# if a mac already exists, check that it has the same ip, if not alert 

def readargs():
    parser = argparse.ArgumentParser()
    parser.parse_args()
    return("10.0.0.1/24") # FIXME: test

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

