#!/usr/bin/env python
# -*- coding, utf-8 -*-

# Импорт данных Московской биржи
# Import of MICEX data
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
# along with this code for my bachelor's thesis.  If not, see
# <http://www.gnu.org/licenses/>.

# Requirements: Python 3 (works with 3.3)


# Data
inFileName = 'MICEX.CSV'
tableNames = {
	'SBER':  'MICEX_SBER',
	'GAZP':  'MICEX_GAZP',
	'LKOH':  'MICEX_LKOH',
	'ROSN':  'MICEX_ROSN',
	'GMKN':  'MICEX_GMKN',
	'VTBR':  'MICEX_VTBR',
	'SNGS':  'MICEX_SNGS',
	'SBERP': 'MICEX_SBERP',
}
timezone = 'Europe/Moscow'


# Code
from common.connect import connect, analyze
conn = connect()
cursor = conn.cursor()

print('Creating tables...')
for tableName in tableNames.values():
	cursor.callproc('create_table', (tableName,))

print('Importing data...')
from csv import reader
with open(inFileName, 'r', newline = '') as infile:
	csvreader = reader(infile, delimiter = ',')
	for row in csvreader:
		# TODO: Use preparing cursors
		if row[0] in tableNames:
			cursor.execute('INSERT INTO "'+tableNames[row[0]]+'" (moment, price, volume) VALUES (%s, %s, %s)', (row[2][0:8] + 'T' + row[2][8:14] + '.' + row[2][14:] + ' ' + timezone, row[4], row[5]))
del cursor
conn.commit()
print('Transaction committed.')

analyze(conn, tableNames.values())

print('Done.')
del conn
