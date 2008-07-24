#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib
import getopt

def main(file, host):
    post_url = 'http://%s/admin/delete/shop' % host
    f = open(file, 'r')
    for line in f:
        cols = line.split(',')
        params = urllib.urlencode({
            'id': cols[0],
            'name': cols[2],
        })
        res = urllib.urlopen(post_url, params)
        print res.read()
    f.close()

def usage():
    print """
Usage: ./delete_shop.py [options]

    --host    remote host(e.g.example.com)
    --file    csv file
"""

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['host=', 'file='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    host = 'localhost:8080'
    file = None
    for o,a in opts:
        if o in ('--host'):
            host = a
        elif o in ('--file'):
            file = a

    if file:
        main(file, host)
    else:
        usage()
        sys.exit(2)

