#!/usr/bin/env python3
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

# Requirements: Python 3 (works with 3.3), MatPlotLib, Pandas


# Data
tableName = 'MICEX_SBER';


# Code
outFileName = tableName + '.count_of_transactions.CSV'
from common.connect import connect
conn = connect()

import matplotlib.pyplot as plt
import pandas as pd

print('Getting data...')
df = pd.read_sql('''
	SELECT
		day,
		hour,
		COUNT(id) AS "'''+tableName+'''"
	FROM
		(
			SELECT
				day::date,
				hour
			FROM
				generate_series((SELECT min(date_trunc('day', moment)) FROM "MICEX_SBER"), (SELECT max(date_trunc('day', moment)) FROM "MICEX_SBER"), '1 day'::interval) AS days(day),
				generate_series(0, 23) AS hours(hour)
		) AS intervals
		LEFT JOIN "'''+tableName+'''" AS data
		ON
		intervals.day = date_trunc('day', data.moment)
		AND intervals.hour = extract(HOUR FROM data.moment)
	GROUP BY
		day, hour
	ORDER BY
		day, hour
''', conn)
df = df.pivot(index = 'hour', columns = 'day', values = tableName)

print('Writing output to `{:s}`...'.format(outFileName))
df.to_csv(outFileName, sep = ';')

print('Done.')
del conn
