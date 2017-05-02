#!/usr/bin/env python

import os
import sys
import requests
import getpass
import argparse

def ghtraffic(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--org",
                        help="Name of the github organization",
                        default="AMReX-Codes")
    parser.add_argument("--repo",
                        help="name of the repo",
                        default="amrex")
    parser.add_argument("--user",
                        help="User name",
                        default="WeiqunZhang")

    args = parser.parse_args()

    clone_records = {}

    # read previously saved record
    fname = args.repo.strip()+"-traffic.org"
    if os.path.isfile(fname):
        f = open(fname, 'r')
        for i in range(3): # skip first three lines
            f.readline()
        for line in f.readlines():
            words = line[:-1].split('|')
            if len(words) < 4:
                break
            ts = words[1].strip()
            ct = int(words[2])
            uq = int(words[3])
            if len(ts) == 10 and ts[0:2] == '20' and ts[4] == '-':
                clone_records[ts] = (ct,uq)
            else:
                break
                
        f.close()

    pw = getpass.getpass(args.user + "'s github password:")

    ghurl = 'https://api.github.com/repos/'+args.org.strip()+'/'+args.repo.strip()+'/traffic/clones'
    response = requests.get(ghurl, auth=(args.user.strip(),pw))
    response = response.json()

    if response.get('message'):
        print(ghurl+": " + response['message'])
        sys.exit(1)

    clones = response['clones']
    for lst in clones:
        clone_records[lst['timestamp'][0:10]] = (lst['count'], lst['uniques'])

    f = open(fname, 'w')
    f.write(args.repo+'\n')
    f.write('|       Time |   Count | Uniques |\n')
    f.write('|------------+---------+---------|\n')
    totcnt = 0
    totunq = 0
    for k, v in sorted(clone_records.items()):
        f.write('| {0:10s} | {1:7d} | {2:7d} |\n'.format(k,v[0],v[1]))
        totcnt += v[0]
        totunq += v[1]
    f.write('|------------+---------+---------|\n')
    f.write('| {0:10s} | {1:7d} | {2:7d} |\n'.format('Total',totcnt,totunq))
    f.close()

if __name__ == "__main__":
    ghtraffic(sys.argv)
