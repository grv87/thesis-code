#!/usr/bin/env python3
# -*- coding, utf-8 -*-

# Байесовский информационнй критерий
# Bayesian Information Criterion
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

# Requirements: Python 3 (works with 3.3)


# Code
from math import log as ln
ln_L = lambda f_X, x: sum([ln(f_X(x[j])) for j in range(len(x))])

def BIC(f_X, x, k):
	n = len(x)
	return 2 * ln_L(f_X, x) - (3 * k - 1) * ln(n)
