#!/usr/bin/env python3
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

# Requirements: Python 3 (works with 3.3), Python-dateutil, NumPy,
#   SciPy


# Data
from dateutil.parser import parse
tableName = 'MICEX_SBER'
startDateTime = parse('2011-06-01T10:30')
# endDateTime = parse('2011-06-01T11:30')

n = 200 # Size of window
k = 2 # Number of components in mixture
delta_F = 0.001
delta_theta = 0.001

# imageIndex = 0
precision = 3


# Code
from common.get_data import getData

import numpy as np
from math import exp, log as ln
from random import random
from scipy.stats import gamma # Gamma distribution
from scipy.special import psi # Digamma function

from scipy.optimize import fsolve
from scipy.spatial.distance import euclidean

x = None
f = lambda u, alpha, beta: gamma.pdf(u, alpha, scale = 1 / beta)

k_underline = range(k)
n_underline = range(n)

p = lambda theta, i: theta[i]
alpha = lambda theta, i: theta[k + i]
beta = lambda theta, i: theta[k * 2 + i]

import warnings
warnings.filterwarnings('error')

f_X_Y = lambda u, i, theta: p(theta, i) * f(u, alpha(theta, i), beta(theta, i))
f_X = lambda u, theta: sum([f_X_Y(u, i, theta) for i in k_underline])
f_Y_cond_X = lambda i, u, theta: f_X_Y(u, i, theta) / f_X(u, theta)

cursor = getData(tableName, startDateTime, n, precision)

for row in cursor:
	moment = row[1]
	print(moment)
	x = np.array(row[2])
	assert len(x) == n # Make sure we have exactly n values
	# print(x)
	print(x.mean(),  x.var())
	
	m = 0 # Number of current step
	print('m', m)
	
	# Initial values TODO
	p_m = [0.9, 0.1] # [1 / k for i in k_underline]
	alpha_m =[0.2,  0.3]
	beta_m = [0.0002,  0.0001]

	print('p_m', p_m)
	print('alpha_m', alpha_m)
	print('beta_m', beta_m)

	# Initial values TODO
	s, loc, t = gamma.fit(x, loc = 0)
	alpha_est = s
	beta_est = 1 / t
	print(alpha_est, loc, beta_est)
	p_m = [0.4, 0.6]
	alpha_m = [alpha_est ** (random() * 2) for i in k_underline]
	beta_m = [beta_est ** (random() * 2) for i in k_underline]
	theta_m = p_m + alpha_m + beta_m
	print('p_m', p_m)
	print('alpha_m', alpha_m)
	print('beta_m', beta_m)
	
	while True:
		# Prepare for next step
		m += 1
		print('m', m)
		p_m_1 = p_m
		alpha_m_1 = alpha_m
		beta_m_1 = beta_m
		theta_m_1 = theta_m
		
		for i in k_underline:
			Z_i = [f_Y_cond_X(i, x[j], theta_m_1) for j in n_underline]
			A_i = sum(Z_i)
			B_i = sum([Z_i[j] * x[j] for j in n_underline])
			C_i = sum([Z_i[j] * ln(x[j]) for j in n_underline])
			D_i = ln(A_i / B_i) + C_i / A_i
			p_m[i] = 1 / n * A_i
			assert D_i < 0
			solve_res, full_output, ier, mesg = fsolve(lambda alpha: ln(alpha) - psi(alpha) + D_i, alpha_m_1[i], full_output = True)
			assert ier == 1
			alpha_m[i] = solve_res[0]
			beta_m[i] = alpha_m[i] * A_i / B_i
		
		theta_m = p_m + alpha_m + beta_m
		print('p_m', p_m)
		print('alpha_m', alpha_m)
		print('beta_m', beta_m)
		
#		# TODO
#		d = euclidean(p_m + alpha_m + beta_m, p_m_1 + alpha_m_1 + beta_m_1)
#		print('d', d)
#		if d < delta_theta:
#			break
		
		d = euclidean(theta_m, theta_m_1)
		print('d', d)
		if d < delta_theta:
			break
