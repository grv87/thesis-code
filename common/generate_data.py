#!/usr/bin/env python3
# -*- coding, utf-8 -*-

# Генерация выборки из смеси гамма-распределений
# Generation of sample from the mixture of gamma distributions
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

# Requirements: Python 3 (works with 3.3), NumPy, SciPy


# Code
import numpy as np
from numpy.random import choice
from scipy.stats import gamma

def getData(n, k, theta_tilde):
	assert len(theta_tilde) == 3 * k - 1
	
	k_underline = range(k)
	n_underline = range(n)
	
	x = np.zeros(n)
	p = theta_tilde[0:k-1] + [1 - sum(theta_tilde[0:k-1])]
	components = []
	for i in k_underline:
		components += [gamma(theta_tilde[k - 1 + i], scale = 1 / theta_tilde[k * 2 - 1 + i], loc = 0)]
		
	for j in n_underline:
		y = choice(k_underline, p = p)
		x[j] = components[y].rvs()
	
	return x
