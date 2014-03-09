#!/usr/bin/env python
# -*- coding, utf-8 -*-

# Соединение с базой данных
# Connection to database
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

# Requirements: PostgreSQL server, Python 3 (works with 3.3), psycopg2


# Data
conn_params = {
	'host':     'grv87.ftp.sh',
	'port':     5433,
	'user':     'thesis',
	'password': r'',
	'dbname':   'thesis',
}


# Code
import psycopg2 as _psycopg2

def connect():
	print('Establishing connection to database...')
	conn = _psycopg2.connect(**conn_params)
	print('Connection established.')
	return conn

def analyze(conn, tableNames):
	print('Analyzing tables...')
	conn.set_isolation_level(_psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
	cursor = conn.cursor()
	for tableName in tableNames:
		cursor.execute('VACUUM ANALYZE "'+tableName+'"')
