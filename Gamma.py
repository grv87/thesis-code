#!/usr/bin/env python3
# -*- coding, utf-8 -*-

# Оценка параметров гамма-распределения методом МП
# Estimation of gamma distributions by ML method
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

# Requirements: Python 3 (works with 3.3), Python-dateutil, NumPy,
#   SciPy, MatPlotLib


# Data
from dateutil.parser import parse
tableName = 'MICEX_SBER'
startDateTime = parse('2011-06-01T10:30')
# endDateTime = parse('2011-06-01T11:30')

n = 200 # Size of window
k = 2 # Number of components in mixture
delta_F = 0.001
delta_theta = 0.001

precision = 3

# imageIndex = 0
binWidth = 100

signLevel = 0.05


# Code
from common.get_data import getData

import numpy as np
from math import log as ln
from scipy.stats import gamma # Gamma distribution
from scipy.special import psi # Digamma function

from scipy.optimize import fsolve

x = None
f = lambda u, alpha, beta: gamma.pdf(u, alpha, scale = 1 / beta)
f_X = lambda u: f(u, alpha, beta)
cdf = lambda u, alpha, beta: gamma.cdf(u, alpha, scale = 1 / beta)

k_underline = range(k)
n_underline = range(n)

import warnings
warnings.filterwarnings('error')

from common.tests import *
from common.BIC import BIC

import matplotlib.pyplot as plt

cursor = getData(tableName, startDateTime, n, precision)

for row in cursor:
	moment = row[1]
	print(moment)
	x = np.array(row[2])
	assert len(x) == n # Make sure we have exactly n values
	x_max = int(x.max())
	bins = range(0, x_max + binWidth, binWidth)
	plt.hist(x, bins = bins, facecolor = 'white')
	# plt.show()
	
	x_mean = x.mean()
	x_var = x.var()
	print(x_mean,  x_var)
	
	print('Method of moments')
	alpha = x_mean ** 2 / x_var
	beta = x_mean / x_var
	print(alpha, beta)
	plt.hist(x, bins = bins, facecolor = 'white')
	x_for_plot = np.zeros(len(bins) - 1)
	y_for_plot = np.zeros(len(bins) - 1)
	for i in range(len(bins) - 1):
		x_for_plot[i] = (bins[i] + bins[i + 1]) / 2
		y_for_plot[i] = (cdf(bins[i + 1], alpha, beta) - cdf(bins[i], alpha, beta)) * n
	plt.plot(x_for_plot, y_for_plot, linewidth = 2)
	# plt.show()
	print('BIC', BIC(f_X, x, 1))
	
	print('ML method')
	D = -ln(x_mean) + 1 / n * sum([ln(x[j]) for j in n_underline])
	solve_res, full_output, ier, mesg = fsolve(lambda alpha: ln(alpha) - psi(alpha) + D, alpha, full_output = True)
	assert ier == 1
	alpha = solve_res[0]
	beta = alpha * n / (alpha * n - 1) * alpha / x_mean
	print(alpha, beta)
	plt.hist(x, bins = bins, facecolor = 'white')
	x_for_plot = np.zeros(len(bins) - 1)
	y_for_plot = np.zeros(len(bins) - 1)
	for i in range(len(bins) - 1):
		x_for_plot[i] = (bins[i] + bins[i + 1]) / 2
		y_for_plot[i] = (cdf(bins[i + 1], alpha, beta) - cdf(bins[i], alpha, beta)) * n
	plt.plot(x_for_plot, y_for_plot, linewidth = 2)
	# plt.show()
	
	x.sort()
	cdf = lambda u: gamma.cdf(u, alpha, loc = 0, scale = 1 / beta)
	print('Kolmogorov Test', KolmogorovTest(x, cdf))
	print('Original critical value', KolmogorovOriginalCriticalValues[signLevel](alpha))
	print('Corrected critical value', KolmogorovCorrectedCriticalValues[signLevel](alpha))
	print('Smirnov Test', SmirnovTest(x, cdf))
	print('Critical value', SmirnovCriticalValues[signLevel](alpha))
	print('Kramer-Mises-Smirnov Test', KramerMisesSmirnovTest(x, cdf))
	print('Original critical value', KramerMisesSmirnovOriginalCriticalValues[signLevel](alpha))
	print('Corrected critical value', KramerMisesSmirnovCorrectedCriticalValues[signLevel](alpha))
	print('Anderson-Darling Test', AndersonDarlingTest(x, cdf))
	print('Original critical value', AndersonDarlingOriginalCriticalValues[signLevel](alpha))
	print('Corrected critical value', AndersonDarlingCorrectedCriticalValues[signLevel](alpha))
	print('BIC', BIC(f_X, x, 1))
