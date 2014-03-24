#!/usr/bin/env python3
# -*- coding, utf-8 -*-

# Непараметрические критерии для сложных гипотез о гамма-распределении
#  с ОМП обоих параметров
# Non-parametric tests for composite hypotheses about gamma distribution
#  with ML estimation of both parameters
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

# Источники:
# Оригинальные критические значения:
# 	1. Рекомендации по стандартизации Р 50.1.037-2002. Прикладная
# 	   статистика. Правила проверки согласия опытного распределения с
# 	   теоретическим. Часть II. Непараметрические критерии. М.,
# 	   Госстандарт России.
# Скорректированные критические значения:
# 	2. Лемешко Б. Ю., Лемешко С. Б. Модели распределений статистик
# 	   непараметрических критериев согласия при проверке сложных гипотез
# 	   с использованием оценок максимального правдоподобия. Часть II //
# 	   Измерительная техника. 2009. №8. С. 17–26.
# 	3. Лемешко Б. Ю. [и др.] Статистический анализ данных, моделирование
# 	   и исследование вероятностных закономерностей. Компьютерный
# 	   подход. Новосибирск, Изд-во НГТУ, 2011. 888 с.
# 	   ISBN 978-5-7782-1590-0


# Data
_maxShape = 10

# Code
#from numpy import polyval as _polyval
#from numpy.ma import polyfit as _polyfit
from scipy import interpolate

# Initialization
print('Interpolation of critical values by polynomials')
_Shapes = [0.3, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0]

def _InitCriticalValues(_CriticalValues):
	res = dict()
	for (signLevel, CriticalValues) in _CriticalValues.items():
		res[signLevel] = interpolate.UnivariateSpline(_Shapes, CriticalValues, bbox = [0, _maxShape], k = 1, s = 0)
	return res

print('Kolmogorov original critical values')
KolmogorovOriginalCriticalValues = _InitCriticalValues({
	0.150: [0.8702, 0.8503, 0.8283, 0.8168, 0.8144, 0.8146, 0.8098],
	0.100: [0.9343, 0.9081, 0.8862, 0.8738, 0.8704, 0.8711, 0.8659],
	0.050: [1.0424, 1.0040, 0.9836, 0.9703, 0.9650, 0.9659, 0.9608],
	0.025: [1.1508, 1.0984, 1.0813, 1.0674, 1.0598, 1.0606, 1.0565],
	0.010: [1.2970, 1.2233, 1.2128, 1.1989, 1.1879, 1.1877, 1.1865]
})

print('Smirnov critical values')
SmirnovCriticalValues = _InitCriticalValues({
	0.150: [2.2246, 2.2406, 2.1738, 2.1292, 2.1092, 2.0978, 2.0833],
	0.100: [2.6511, 2.6348, 2.5483, 2.4951, 2.4613, 2.4463, 2.4276],
	0.050: [3.4520, 3.3620, 3.2393, 3.1737, 3.1083, 3.0847, 3.0613],
	0.025: [4.3543, 4.1659, 4.0035, 3.9281, 3.8204, 3.7850, 3.7602],
	0.010: [5.7217, 5.3609, 5.1400, 5.0563, 4.8743, 4.8178, 4.7972]
})

print('Kramer-Mises-Smirnov original critical values')
KramerMisesSmirnovOriginalCriticalValues = _InitCriticalValues({
	0.150: [0.1163, 0.1085, 0.1017, 0.1007, 0.1000, 0.0993, 0.0970],
	0.100: [0.1405, 0.1295, 0.1220, 0.1209, 0.1196, 0.1189, 0.1162],
	0.050: [0.1885, 0.1702, 0.1623, 0.1609, 0.1584, 0.1576, 0.1546],
	0.025: [0.2458, 0.2179, 0.2107, 0.2088, 0.2047, 0.2038, 0.2008],
	0.010: [0.3381, 0.2932, 0.2888, 0.2859, 0.2790, 0.2781, 0.2759]
})

print('Anderson-Darling original critical values')
AndersonDarlingOriginalCriticalValues = _InitCriticalValues({
	0.150: [0.6279, 0.5987, 0.5771, 0.5641, 0.5611, 0.5590, 0.5557],
	0.100: [0.7195, 0.6822, 0.6547, 0.6401, 0.6345, 0.6324, 0.6281],
	0.050: [0.8852, 0.8322, 0.7931, 0.7760, 0.7648, 0.7622, 0.7558],
	0.025: [1.0645, 0.9932, 0.9405, 0.9214, 0.9030, 0.8993, 0.8905],
	0.010: [1.3251, 1.2257, 1.1515, 1.1302, 1.1001, 1.0938, 1.0813]
})

print('Kolmogorov corrected critical values')
KolmogorovCorrectedCriticalValues = _InitCriticalValues({
	0.10: [0.905, 0.884, 0.862, 0.849, 0.845, 0.843, 0.842],
	0.05: [0.990, 0.965, 0.940, 0.924, 0.919, 0.916, 0.915],
	0.01: [1.162, 1.131, 1.097, 1.077, 1.070, 1.066, 1.063]
})

print('Kramer-Mises-Smirnov corrected critical values')
KramerMisesSmirnovCorrectedCriticalValues = _InitCriticalValues({
	0.10: [0.127, 0.119, 0.111, 0.107, 0.106, 0.105, 0.105],
	0.05: [0.158, 0.146, 0.136, 0.131, 0.129, 0.128, 0.128],
	0.01: [0.233, 0.212, 0.194, 0.185, 0.182, 0.180, 0.179]
})

print('Anderson-Darling corrected critical values')
AndersonDarlingCorrectedCriticalValues = _InitCriticalValues({
	0.10: [0.718, 0.684, 0.657, 0.643, 0.639, 0.637, 0.636],
	0.05: [0.870, 0.824, 0.785, 0.766, 0.761, 0.758, 0.757],
	0.01: [1.233, 1.145, 1.084, 1.051, 1.043, 1.039, 1.037]
})

# All tests assume that x is sorted!!

def KolmogorovTest(x, cdf):
	n = len(x)
	n_underline = range(n)
	D_plus = max([abs((i + 1) / n - cdf(x[i])) for i in n_underline])
	D_minus = max([abs(cdf(x[i]) - i / n) for i in n_underline])
	D = max(D_plus, D_minus)
	return (6 * n * D + 1) / (6 * n ** 0.5)

def SmirnovTest(x, cdf):
	n = len(x)
	n_underline = range(n)
	D_plus = max([abs((i + 1) / n - cdf(x[i])) for i in n_underline])
	return (6 * n * D_plus + 1) ** 2 / (9 * n)

def KramerMisesSmirnovTest(x, cdf):
	n = len(x)
	n_underline = range(n)
	return 1 / (12 * n) + sum([(cdf(x[i]) - (2 * i + 1) / (2 * n)) ** 2 for i in n_underline])

from math import log as ln

def AndersonDarlingTest(x, cdf):
	n = len(x)
	n_underline = range(n)
	return -n - 2 * sum([(2 * i + 1) / (2 * n) * ln(cdf(x[i])) + (1 - (2 * i + 1) / (2 * n)) * ln(1 - cdf(x[i])) for i in n_underline])
