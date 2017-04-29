#!/usr/bin/env python

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

    pw = getpass.getpass(args.user + "'s github password:")

    ghurl = 'https://api.github.com/repos/'+args.org.strip()+'/'+args.repo.strip()+'/traffic/clones'
    response = requests.get(ghurl, auth=(args.user.strip(),pw))
    response = response.json()

    if response.get('message'):
        print(ghurl+": " + response['message'])
        sys.exit(1)

    print("count:", response['count'])
    print("uniques:", response['uniques'])
    print("clones:", response['clones'])

if __name__ == "__main__":
    ghtraffic(sys.argv)
