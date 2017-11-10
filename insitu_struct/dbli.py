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
from PyQt4 import QtCore, QtGui
import csv


def importfile(datafile, savefile):
    """doc string
    """

    # Set up empty dictionary of key terms
    datadict = {'SampleName': '', 'Table Num': 0, 'Area [mm2]': 0,
                'Thickness [nm]': 0, 'Hysteresis Frequency [Hz]': 0,
                'Hysteresis Amplitude [V]': 0, 'd33ls+ [nm/V]': 0,
                'd33ls- [nm/V]': 0, 'Prrel [uC/cm2]': 0}
    with open(datafile, 'r') as f:
        online = 0
        dat = 0
        for line in f:
            line = str(line)
            # print('line: ', line)

            if online > 0 and not line.strip():
                # end table collection
                online = 0
                # make the csv
                makecsv(datadict, table, savefile)

            if line.strip() and online > 0:
                # collect table
                data = line.split("\t")
                field = (float(data[1]) /
                         datadict['Thickness [nm]'] * 10000)

                strain = (float(data[10]) /
                          datadict['Thickness [nm]'] * 100)
                table.append([field, float(data[4]), strain,
                             float(data[10])])
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
                table = [['Field [kV/cm]', 'Polarization [uC/cm2]',
                          'Strain [%]', 'Strain [nm]', 'Item', 'data']]
        makecsv(datadict, table, savefile)


def makecsv(datadict, table, savefile):
    # add data to table

    order = ['SampleName', 'Table Num', 'Area [mm2]', 'Thickness [nm]',
             'Hysteresis Frequency [Hz]', 'Hysteresis Amplitude [V]',
             'd33ls+ [nm/V]', 'd33ls- [nm/V]', 'Prrel [uC/cm2]']
    for i, key in enumerate(order):
        table[1 + i].append(key)
        table[1 + i].append(datadict[key])
    # save table to file
    namelist = [
        savefile,
        "D33ls" + str(round(datadict['d33ls+ [nm/V]'] * 1000)),
        "V" + str(round(datadict['Hysteresis Amplitude [V]'])),
        "Hz" + str(round(datadict['Hysteresis Frequency [Hz]'])),
        "table" + str(datadict['Table Num']) + ".csv"]
    name = "_".join(namelist)
    print('name: ', name)
    with open(name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(table)
    print("done")


if __name__ == '__main__':
    exfiles = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
                                           os.pardir, 'examplefiles'))
    #list_supported_formats()
    #print_filetype_info("bruker_raw")
    datafile = os.path.join(exfiles, "DBLI_BBT_c017_19.dat")
    savefile = os.path.join(exfiles, "DBLI_BBT_c017_19")
    table = importfile(datafile, savefile)


    # Files are getting overwritten if d33 is same....
