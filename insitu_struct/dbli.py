#!/usr/bin/env python
"""Converts ASCII output from DBLI to individual formated csv files for each
scan.

To DO:
    - Create file checker to prevent errors if wrong file is selected
"""
# Copyright 2016 Austin Fox
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
import csv
from data_analysis import csv_append_col
from datasetmetta import get_name_data


def importfile(datafile, savedir, savename=None):
    """doc string
    """

    # Set up empty dictionary of key terms
    datadict = {'SampleName': '', 'Table Num': 0, 'Area [mm2]': 0,
                'Thickness [nm]': 0, 'Composition': 0,
                'Hysteresis Frequency [Hz]': 0,
                'Hysteresis Amplitude [V]': 0,
                'd33ls+ [nm/V]': 0, 'd33ls- [nm/V]': 0, 'Prrel [uC/cm2]': 0}
    with open(datafile, 'r') as f:
        online = 0
        dat = 0
        [comp, thick, num, volt] = get_name_data(os.path.basename(datafile))
        datadict['Composition'] = comp

        for line in f:
            line = str(line)
            # print('line: ', line)

            if online > 0 and not line.strip():
                # end table collection
                online = 0
                # make the csv
                makecsv(datadict, table, savedir, savename)
                return

            if line.strip() and online > 0:
                # collect table
                data = line.split("\t")
                field = (float(data[1]) /
                         datadict['Thickness [nm]'] * 10000)

                strain = (float(data[10]) /
                          datadict['Thickness [nm]'] * 100)
                table.append(['', field, float(data[4]), strain])
                             # float(data[10])])
                online += 1

            if dat == 1:
                # collect data
                if 'Time' in line:
                    online = 1
                    dat = 0
                for key in datadict:
                    if key in line:
                        if key == 'SampleName':
                            datadict[key] = line.strip(key + ":").strip()
                        else:
                            datadict[key] = float(line.strip(key + ":").strip())

            if 'TableVersion' in line:
                # start data search
                dat = 1
                datadict['Table Num'] += 1
                # Set up table
                table = [['', 'Field [kV/cm]', 'Polarization [uC/cm2]',
                          'Strain [%]']]
        makecsv(datadict, table, savedir, savename)


def makecsv(datadict, table, savedir, savename=None):
    # add data to table

    order = ['SampleName', 'Table Num', 'Area [mm2]', 'Composition',
             'Thickness [nm]', 'Hysteresis Frequency [Hz]',
             'Hysteresis Amplitude [V]', 'd33ls+ [nm/V]', 'd33ls- [nm/V]',
             'Prrel [uC/cm2]']
    for i, key in enumerate(order):
        table[0 + 2*i][0] = key
        table[1 + 2*i][0] = datadict[key]
    # save table to file
    if not savename:
        name = os.path.join(savedir, "DBLI.csv")
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
        # savedir = os.path.abspath(os.path.join(basename, os.pardir))
        savedir = os.path.abspath(basename)
        importfile(f, savedir)
    print('Done')
