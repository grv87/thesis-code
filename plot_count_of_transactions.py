﻿#!/usr/bin/env python3
# -*- coding, utf-8 -*-

# TODO
# TODO
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

# Requirements: Python 3 (works with 3.3), Python-dateutil, MatPlotLib,
#  Pandas, XeLaTeX, GhostScript


# Data
from dateutil.parser import parse
tableName = 'MICEX_SBER'
startDateTime = parse('2011-06-01T10:00')
endDateTime = parse('2011-06-01T14:00')
period = 'minute'
plotSuptitle = 'Количество сделок в минуту'
plotTitle = 'Тикер SBER, с 10:00 до 14:00 1 июня 2011 года'

# Code
from common.connect import connect
conn = connect()

import matplotlib as mpl
mpl.use('pgf')
mpl.rcParams.update({
	'pgf.texsystem': 'xelatex',
	'pgf.preamble': [r'\usepackage{unicode-math}'],
	'text.usetex': True,
	'text.latex.unicode': True,
	'font.family': 'PT Serif',
	'font.size': 14,
})
import matplotlib.pyplot as plt
imageName = '{:s}.count_of_transactions.png'.format(tableName)
import pandas as pd

print('Getting data...')
df = pd.read_sql('''
	SELECT
		interval,
		COUNT(id) AS "'''+tableName+'''"
	FROM
		generate_series(%s, %s, ('1 '||%s)::interval) AS intervals(interval)
		LEFT JOIN
		"'''+tableName+'''" AS data
		ON intervals.interval = date_trunc(%s, data.moment)
	GROUP BY
		interval
	ORDER BY
		interval
''', conn, params = (startDateTime, endDateTime, period, period), index_col = 'interval')
# df = df.to_period(pd.Period)
# idx = pd.period_range(min(df.index), max(df.index), freq = 'H')
# df = df.reindex(idx, fill_value = 0)

# plt.clf()
print('Plotting...')
df.plot(legend = False) # kind = 'bar'
plt.xlabel('')
plt.ylabel('')
plt.suptitle(plotSuptitle, fontsize = 14, fontweight = 'bold')
plt.title(plotTitle, fontsize = 14, fontweight = 'bold')
plt.savefig(imageName)
print('Plot has been saved to {:s}.'.format(imageName))

print('Done.')
del conn
