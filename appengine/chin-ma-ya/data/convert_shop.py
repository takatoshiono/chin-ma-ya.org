#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def main():
    for line in sys.stdin:
        line = line.rstrip('\n')
        cols = line.split(',')
        cols[4:6] = ['"%s,%s"' % (cols[4], cols[5])]
        print ','.join(cols)

if __name__ == '__main__':
    main()

