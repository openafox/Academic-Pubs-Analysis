#!/usr/bin/env python
"""Converts Diffrac V4 debug format text files (converted from raw files with
RawFileConverter) to single CSV files with one 2theta column and a series of
counts columns. Assumes all scans in file have same 2theta range and increment.

To DO:
    - Create file checker to prevent errors if wrong file is selected
"""
# Copyright 2015 Austin Fox
# Program is distributed under the terms of the
# GNU General Public License see ./License for more information.

# Python 3 compatibility
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super,
         filter, map, zip)
# #######################

import sys
import numpy as np
import csv
from data_analysis import get_datafiles


def importfile(datafile, savefile):
    """doc string
    """
    with open(datafile, 'r') as f:
        table = []
        start = 0
        online = -1
        count = 1000
        addit = 1000
        cent_x = 0
        for i, line in enumerate(f):
            if i == 7:
                count = int(line)
                print(count)
            if 7 < i < count + 9:
                table.append([float(pt) for pt in line.split()])
            if i == count + 9:
                # ??? not sure on this
                cent_y = float(line)
                table = np.asarray(table)
                print(table)
                print(table.shape)
                table[:,1] = table[:,1] - cent_y
                print('cent_y', cent_y)
            if i == count + 10:
                cent_x = float(line)
                print('cent_x', cent_x)
            if i == count + 9 + 6:
                addit = int(line)
                print('add', addit)
            if i == count + 9 + 6 + addit + 17:
                area = float(line)
                print('area', area)
            if i == count + 9 + 6 + addit + 18:
                thick = float(line)
                print('thick', thick)
                print(table.shape)
                table[:,0] = table[:,0]/(thick*0.1)
                #table[:,0] = table[:,0] + cent_x

    savefile = savefile + ".csv"
    with open(savefile, 'wb') as f:
        print(table.shape)
        writer = csv.writer(f)
        writer.writerows(table[:,0:2])

    return [savefile]

def get_files():
    location = '~/_The_Universe/_Materials_Engr/_Mat_Systems/_BNT_BKT/_CSD/'
    files = get_datafiles(['*.dat'], location)
    return files

if __name__ == '__main__':
        files = get_files()
        for f in files:
            print(f)
            importfile(f, f[:-4])
