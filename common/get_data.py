#!/usr/bin/env python
# -*- coding, utf-8 -*-

# Чтение данных из базы данных
# Reading data from DB
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


# Code
from .connect import connect

def getData(tableName, startDateTime, windowSize, precision):
	conn = connect()

	print('Getting data...')
	cursor = conn.cursor()
	cursor.execute('''
		SELECT
			id,
			moment,
			array_agg("Δt") OVER (ROWS %s PRECEDING) AS x
		FROM
			(
				SELECT
					id,
					moment,
					trunc(EXTRACT(epoch FROM "Δt") * 10 ^ %s) AS "Δt",
					ln_growth_rate(price, lag(price, 1) OVER (ORDER BY moment, id)) AS "ln_growth_rate(price)"
				FROM
					( -- Выкидываем нули
						SELECT
							id,
							moment,
							"Δt",
							price
						FROM
							( -- Подсчитываем промежутки между сделками
								SELECT
									id,
									moment,
									change(moment, lag(moment, 1) OVER (ORDER BY moment, id)) AS "Δt",
									price
								FROM
-- 									( -- Выбираем только сделки
-- 										SELECT
-- 											id,
-- 											moment,
-- 											price /*,
-- 											change(price, lag(price, 1) OVER (ORDER BY moment,  id)) AS "change(price)"*/
-- 										FROM
											"'''+tableName+'''"
-- 										WHERE
-- 											type = 'TRADE'
-- 									) AS t
								WHERE
									moment >= %s
							) AS t
						WHERE
							"Δt" > '0 second'::interval
					) AS t
--					"Δt" < '8 hour'::interval -- Выкидываем время между торговыми сессиями
			) AS t
		LIMIT 1 OFFSET %s - 1 -- TODO
	''', (windowSize, precision, startDateTime, windowSize))
	# del conn
	return cursor
