#!/usr/bin/env python
"""Converts ASCII output from DBLI to individual formated csv files for each
scan.

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

import sys, os
import numpy as np
from data_analysis import get_datafiles
from data_analysis import csv_append_col
from datasetmetta import get_name_data
import csv


def importfile(datafile, savedir, savename=None):
    """doc string
    """

    name = os.path.basename(datafile)[:-4]
    table = []
    # https://softwarerecs.stackexchange.com/questions/7463/fastest-python-library-to-read-a-csv-file
    with open(datafile, 'r') as f:
        csvreader = csv.reader(f)
        table = [row for row in csvreader]
        # or list(csvreader) Need to do speed check sometime
    print(len(table), len(table[0]), type(table))

    #table = table.tolist()
    [comp, thick, num, volt] = get_name_data(name)
    table.insert(0, ["Time [s]", "Current [A]"])
    table.insert(0, [comp, thick])
    table.insert(0, [name, ''])

    # save table to file
    if not savename:
        name = os.path.join(savedir, "CRNT.csv")
    else:
        name = os.path.join(savedir, savename)

    csv_append_col(name, table)


if __name__ == '__main__':
    from data_analysis import get_datafiles
    location = '/Users/towel/_The_Universe/_Materials_Engr/_Mat_Systems/_BNT_BKT/_CSD/_Data/EAPSI'
    files = get_datafiles(['*.raw'], location)

    for f in files:
        name = os.path.basename(f)[:-4]
        basename = os.path.dirname(f)
        savedir = os.path.abspath(os.path.join(basename, os.pardir))
        importfile(f, savedir)
    print('Done')
