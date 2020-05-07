#!/usr/bin/env python

import os
import sys
import requests
import getpass
import datetime

def ghtraffic():

#    f = open('mypwd.txt')
#    line = f.readline()
#    credentials=line.split(':')
#    usr=credentials[0]
#    pwd=credentials[1]
##    pwd = getpass.getpass()
#    usrpwd = (usr,pwd)

    f = open('mytoken.txt')
    line = f.readline()
    tokens=line.split(':')
    mytoken=tokens[0]
    today=f"{datetime.datetime.now():%Y-%m-%d}"
    year=int(today[0:4])
    month=int(today[5:7])
    if(month>=10):
        FY=year+1
    else:
        FY=year
    repos = [{'org':'liuyangzhuan', 'repo':'ButterflyPACK'},
            {'org':'pghysels', 'repo':'STRUMPACK'},
            {'org':'xiaoyeli', 'repo':'GPTune'},
            {'org':'xiaoyeli', 'repo':'superlu_dist'},
            {'org':'xiaoyeli', 'repo':'superlu'}]

    for repo in repos:
        clone_records = {}

        # read previously saved record
        fname = repo['repo']+"-traffic.org"
        fname1 = "FY"+str(FY)+"_"+repo['repo']+"-traffic.org"
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

        ghurl = 'https://api.github.com/repos/'+repo['org']+'/'+repo['repo']+'/traffic/clones'
#        response = requests.get(ghurl, auth=usrpwd)
        response = requests.get(ghurl, headers={'Authorization':mytoken})

        response = response.json()

        if response.get('message'):
            print(ghurl+": " + response['message'])
        else:
            clones = response['clones']
            for lst in clones:
                k = lst['timestamp'][0:10]
                c = lst['count']
                u = lst['uniques']
                if k in clone_records:
                    c = max(c, clone_records[k][0])
                    u = max(u, clone_records[k][1])
                clone_records[k] = (c,u)

            f = open(fname, 'w')
            f.write('* '+repo['repo']+' clones\n')
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


            f = open(fname1, 'w')
            f.write('* '+repo['repo']+' clones\n')
            f.write('|       Time |   Count | Uniques |\n')
            f.write('|------------+---------+---------|\n')
            totcnt = 0
            totunq = 0
            for k, v in sorted(clone_records.items()):
                year=int(k[0:4])
                month=int(k[5:7])
                if((year==FY and month<10) or (year==FY-1 and month>=10)):
                    f.write('| {0:10s} | {1:7d} | {2:7d} |\n'.format(k,v[0],v[1]))
                    totcnt += v[0]
                    totunq += v[1]
            f.write('|------------+---------+---------|\n')
            f.write('| {0:10s} | {1:7d} | {2:7d} |\n'.format('Total',totcnt,totunq))
            f.close()


if __name__ == "__main__":
    ghtraffic()
