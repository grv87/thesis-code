#!/usr/bin/env python
# -*- coding, utf-8 -*-

# Перечисление тикеров, представленных в данных Московской биржи
# Enumeration of tickers presented in MICEX data
# Copyright © 2014  Василий Горохов-Апельсинов

# This file is part of code for my bachelor's thesis.
#
# Code for my bachelor's thesis is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Code for my bachelor's thesis is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with code for my bachelor's thesis.  If not, see
# <http://www.gnu.org/licenses/>.

# Requirements: Python 3 (works with 3.3), NumPy, Pandas


# Data
inFileName = 'MICEX.CSV'


# Code
from os import path
outFileName = path.splitext(inFileName)[0] + '.tickers.CSV'
import numpy as np
import pandas as pd
tickersCounts = pd.Series(dtype = np.dtype(int))

from csv import reader
with open(inFileName, 'r', newline = '') as infile:
	csvreader = reader(infile, delimiter = ',')
	for row in csvreader:
		try:
			tickersCounts[row[0]] += 1
		except KeyError:
			tickersCounts[row[0]] = 1

print('Writing output to `{:s}`...'.format(outFileName))
tickersCounts.to_csv(outFileName, sep = ';')

print('Done.')
