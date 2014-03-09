#!/usr/bin/env python
# -*- coding, utf-8 -*-

# Оценка параметров смеси гамма-распределений по EM-алгоритму
# Estimation of parameters of mixture of gamma distributions
#  by EM algorithm
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

# Requirements: Python 3 (works with 3.3), Python-dateutil, NumPy, SciPy


# Data
from dateutil.parser import parse
tableName = 'MICEX_SBER'
startDateTime = parse('2011-06-01T10:30')
# endDateTime = parse('2011-06-01T11:30')

n = 200 # Size of window
k = 2 # Number of components in mixture
delta_F = 0.001
delta_theta = 0.001

imageIndex = 0
precision = 3


# Code
from common.get_data import getData

import numpy as np
from math import exp, log as ln
from scipy.stats import gamma # Gamma distribution
from scipy.special import psi # Digamma function

from scipy.spatial.distance import euclidean

x = None
eps = None
f = gamma.pdf

k_underline = range(k)
n_underline = range(n)

m = 0 # Number of current step
# Initial values TODO
p_ast_m = [0.9, 0.1] # [1 / k for i in k_underline]
alpha_ast_m =[0.2,  0.3]
beta_ast_m = [0.0002,  0.0001]

f_theta_m_x_i = lambda x, i: p_ast_m[i] * f(x, alpha_ast_m[i], scale = 1 / beta_ast_m[i])
# print(f_theta_m_x_i(1, 0))
# print(f_theta_m_x_i(1, 1))
f_X_theta_x = lambda x: sum([f_theta_m_x_i(x, i) for i in k_underline])
#f_theta_i_cond_x = lambda i, x: f_theta_m_x_i(x, i) / f_X_theta_x(x)
import warnings
warnings.filterwarnings('error')
def f_theta_i_cond_x(i, x):
	#print(i, x)
	#print(f_theta_m_x_i(x, i))
	#print(f_X_theta_x(x))
	try:
		return f_theta_m_x_i(x, i) / f_X_theta_x(x)
	except:
		print(x, i, f_theta_m_x_i(x, i),  f_X_theta_x(x))
		raise


cursor = getData(tableName, startDateTime, n, precision)

for row in cursor:
	moment = row[1]
	print(moment)
	x = np.array(row[2])
	assert len(x) == n # Make sure we have exactly n values
	# print(x)
	print(x.mean(),  x.var())
	
	m = 0
	print('m', m)
	print('p_ast_m', p_ast_m)
	print('alpha_ast_m', alpha_ast_m)
	print('beta_ast_m', beta_ast_m)

	while True:
		g = [[f_theta_i_cond_x(i, x[j]) for j in n_underline] for i in k_underline]
		g_sum = [sum([g[i][j] for j in n_underline]) for i in k_underline]
		
		p_ast_m1 = [1 / n * g_sum[i] for i in k_underline]
		print('p_ast_m1', p_ast_m1)
		alpha_ast_m1 = [sum([g[i][j] * x[j] for j in n_underline]) / g_sum[i] for i in k_underline]
		print('alpha_ast_m1', alpha_ast_m1)
#		i = 0
#		print(exp(psi(alpha_ast_m[i]) -  sum([g[i][j] * ln(x[j]) for j in n_underline]) / g_sum[i] ))
#		i = 1
#		print(exp(psi(alpha_ast_m[i]) -  sum([g[i][j] * ln(x[j]) for j in n_underline]) / g_sum[i] for i in k_underline))
		beta_ast_m1 = [exp(psi(alpha_ast_m[i]) -  sum([g[i][j] * ln(x[j]) for j in n_underline]) / g_sum[i]) for i in k_underline]

		print('beta_ast_m1', beta_ast_m1)
		
#		# TODO
#		d = euclidean(p_ast_m + alpha_ast_m1 + beta_ast_m1, p_ast_m1 + alpha_ast_m1 + beta_ast_m1)
#		print('d', d)
#		if d < delta_theta:
#			break
		
		d = euclidean(p_ast_m + alpha_ast_m1 + beta_ast_m1, p_ast_m1 + alpha_ast_m1 + beta_ast_m1)
		print('d', d)
		if d < delta_theta:
			break
		
		# Prepare for next step
		m += 1
		print()
		print('m', m)
		alpha_ast_m = alpha_ast_m1
		beta_ast_m = alpha_ast_m1
