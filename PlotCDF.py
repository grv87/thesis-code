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
#   SciPy, StatsModels, MatPlotLib, XeLaTeX, GhostScript


# Data
from dateutil.parser import parse
tableName = 'MICEX_SBER'
startDateTime = parse('2011-06-01T10:30')
# endDateTime = parse('2011-06-01T11:30')
plotTitle = 'Сравнение функций распределения'
imageName = 'PlotCDF.png'

n = 200 # Size of window

precision = 3

# imageIndex = 0

# Code
from common.get_data import getData

import numpy as np
from scipy.stats import gamma # Gamma distribution
from statsmodels.distributions import ECDF

cdf = lambda u, p, alpha, beta: sum(p[i] * gamma.cdf(u, alpha[i], scale = 1 / beta[i]) for i in range(len(p)))

import warnings
warnings.filterwarnings('error')

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

cursor = getData(tableName, startDateTime, n, precision)

for row in cursor:
	moment = row[1]
	print(moment)
	x = np.array(row[2])
	assert len(x) == n # Make sure we have exactly n values
	
	print('Plotting...')
	x_max = 3000 # int(x.max())
	bins = range(0, x_max + 1, 10)
	ecdf = ECDF(x)
	plt.plot(bins, [ecdf(bins[i]) for i in range(len(bins))], 'k-', linewidth = 3, label = 'Эмпирические данные')
	
	p = [1.0]
	alpha = [0.2233]
	beta = [0.0001473]
	plt.plot(bins, [cdf(bins[i], p, alpha, beta) for i in range(len(bins))], 'k-', linewidth = 2, label = '$k = 1$, метод моментов')
	
	p = [1.0]
	alpha = [0.3149]
	beta = [0.0002112]
	plt.plot(bins, [cdf(bins[i], p, alpha, beta) for i in range(len(bins))], 'k-.', label = '$k = 1$, метод МП')
	
	p = [0.8371, 0.1629]
	alpha = [0.4131, 48.8275]
	beta = [0.0002283, 14.2616]
	plt.plot(bins, [cdf(bins[i], p, alpha, beta) for i in range(len(bins))], 'k-', label = '$k = 2$, вариант 1')
	
	p = [0.7860, 0.2140]
	alpha = [0.4642, 10.5978]
	beta = [0.0002409, 2.5544]
	plt.plot(bins, [cdf(bins[i], p, alpha, beta) for i in range(len(bins))], 'k--', label = '$k = 2$, вариант 2')
	
	p = [0.3859, 0.2349, 0.3792]
	alpha = [0.7092, 9.7036, 1.4479]
	beta = [0.0001942, 2.2856, 0.0052378]
	plt.plot(bins, [cdf(bins[i], p, alpha, beta) for i in range(len(bins))], 'k:', label = '$k = 3$')
	
	plt.title(plotTitle, fontsize = 14, fontweight = 'bold')
	plt.legend(loc = 'lower right')
	plt.savefig(imageName)
	print('Plot has been saved to {:s}.'.format(imageName))

print('Done.')
