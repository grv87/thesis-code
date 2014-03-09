#!/usr/bin/env python
# -*- coding, utf-8 -*-

# Импорт данных Bloomberg
# Import of Bloomberg data
# Copyright © 2013–2014  Василий Горохов-Апельсинов

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

# Requirements: Python 3 (works with 3.3)


# Data
inFileTableNames = {
	'bloomberg1.CSV': 'bloomberg1',
	'bloomberg2.CSV': 'bloomberg2',
	'bloomberg3.CSV': 'bloomberg3',
}


# Code
from connect import connect, analyze
conn = connect()
cursor = conn.cursor()
cursor.execute("SET DateStyle = 'DMY'")

for (inFileName, tableName) in inFileTableNames.items():
	print('Importing data from `{:s}`...'.format(inFileName))
	cursor.callproc('create_table', (tableName,))
	from csv import reader
	with open(inFileName, 'r', newline = '') as infile:
		csvreader = reader(infile, delimiter = ';')
		for row in csvreader:
			# TODO: Use preparing cursor
			cursor.execute('INSERT INTO "'+tableName +'" (moment, price, volume) VALUES (%s, %s, %s)', (row[0], row[2], row[3]))
	conn.commit()
	print('Transaction committed.')
del cursor

analyze(conn, inFileTableNames.values())

print('Done.')
del conn
