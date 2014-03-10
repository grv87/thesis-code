#!/usr/bin/env python
# -*- coding, utf-8 -*-

# Оценка параметров смеси гамма-распределений по ММП
# Estimation of parameters of mixture of gamma distributions
#  by ML method
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

# Requirements: Python 3 (works with 3.3), Python-dateutil, NumPy,
#  SciPy, OpenOpt, MatPlotLib


# Data
from dateutil.parser import parse
tableName = 'MICEX_SBER'
startDateTime = parse('2011-06-01T10:30')
# endDateTime = parse('2011-06-01T11:30')

n = 200 # Size of window
k = 2 # Number of components in mixture

precision = 3


# Code
from common.get_data import getData

pos_inf = float('+inf')
neg_inf = float('-inf')

import numpy as np
from math import log as _ln, exp, isfinite, isinf
def ln(x):
	if x == 0:
		return neg_inf
	elif isinf(x) and x > 0:
		return pos_inf
	else:
		try:
			return _ln(x)
		except:
			print(x)
			raise
from scipy.stats import gamma # Gamma distribution
# Digamma function
from scipy.special import psi as _psi
def psi(alpha):
	if alpha == 0:
		return neg_inf
	elif isinf(alpha) and alpha > 0:
		return pos_inf
	else:
		return _psi(alpha)
from scipy.optimize import minimize #, basinhopping
from openopt import GLP, NLP
from random import random
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('error')

x = None
f = lambda u, alpha, beta: gamma.pdf(u, alpha, scale = 1 / beta) if u > 0 and alpha != 0 and beta != 0 else 0

k_underline = range(k)
k_m_1_underline = range(k - 1)
n_underline = range(n)

# NLopt
# print(len(theta_tilde))
#opt = nlopt.opt(nlopt.GN_ORIG_DIRECT, len(theta_tilde))
#print(opt.get_algorithm_name())

# Make use constraint: sum(p_ast_m) == 1
# These functions get p_i, alpha_i and beta_i from given theta_tilde tuple
p = lambda theta_tilde, i: theta_tilde[i] if i <= k - 2 else (1 - sum(theta_tilde[0:k-1]))
alpha = lambda theta_tilde, i: theta_tilde[k - 1 + i]
beta = lambda theta_tilde, i: theta_tilde[k * 2 - 1 + i]

d = True
# Negative logarithm of likelihood function
def L_T_tilde(theta_tilde):
	# try:
		# TODO
		# return -sum([ln(sum([p(theta_tilde, i) * f(x[j], alpha(theta_tilde, i), beta(theta_tilde, i)) for i in k_underline])) for j in n_underline])
		Q = [[f(x[j], alpha(theta_tilde, i), beta(theta_tilde, i)) for j in n_underline] for i in k_underline]
		R = [[p(theta_tilde, i) * Q[i][j] for j in n_underline] for i in k_underline]
		S = [sum([R[i][j] for i in k_underline]) for j in n_underline]
		# global d
		# if d:
			# print(Q)
			# print(R)
			# print(S)
			# d = False
		return -sum([ln(S[j]) for j in n_underline])
	# except ValueError:
		# return pos_inf
def L_T_tildewithGrad(theta_tilde, grad):
	# try:
		Q = [[f(x[j], alpha(theta_tilde, i), beta(theta_tilde, i)) for j in n_underline] for i in k_underline]
		R = [[p(theta_tilde, i) * Q[i][j] for j in n_underline] for i in k_underline]
		S = [sum([R[i][j] for i in k_underline]) for j in n_underline]
		if grad.size > 0:
			grad[0:k-1] = [-sum([Q[i][j] / S[j] for j in n_underline]) for i in k_m_1_underline]
			grad[k-1:k*2-1] = [-sum([R[i][j] / S[j] * (ln(beta(theta_tilde, i)) + ln(x[j]) - psi(alpha(theta_tilde, i))) for j in n_underline]) for i in k_underline]
			grad[k*2-1:k*3-1] = [sum([R[i][j] / S[j] * alpha(theta_tilde, i) * x[j] / beta(theta_tilde, i) for j in n_underline]) for i in k_underline]
		return -sum([ln(S[j]) for j in n_underline])
	# except:
		# return pos_inf
def grad_L_T_tilde(theta_tilde):
	try:
		Q = [[f(x[j], alpha(theta_tilde, i), beta(theta_tilde, i)) for j in n_underline] for i in k_underline]
		R = [[p(theta_tilde, i) * Q[i][j] for j in n_underline] for i in k_underline]
		S = [sum([R[i][j] for i in k_underline]) for j in n_underline]
		return \
			[-sum([Q[i][j] / S[j] for j in n_underline]) for i in k_m_1_underline] + \
			[-sum([R[i][j] / S[j] * (ln(beta(theta_tilde, i)) + ln(x[j]) - psi(alpha(theta_tilde, i))) for j in n_underline]) for i in k_underline] + \
			[sum([R[i][j] / S[j] * alpha(theta_tilde, i) * x[j] / beta(theta_tilde, i) for j in n_underline]) for i in k_underline]
	except:
		print(theta_tilde)
		raise
#opt.set_min_objective(L_T_tildewithGrad)

# Constraints		
# constraints = \
	# [{
		# 'type': 'ineq',
		# 'fun':  lambda theta_tilde, i = i: p(theta_tilde, i)
	# } for i in k_underline] + \
	# [{
		# 'type': 'ineq',
		# 'fun':  lambda theta_tilde, i = i: alpha(theta_tilde, i)
	# } for i in k_underline] + \
	# [{
		# 'type': 'ineq',
		# 'fun':  lambda theta_tilde, i = i: beta(theta_tilde, i)
	# } for i in k_underline]
#bounds = [(0, 1) for i in range(k - 1)] + [(0, None) for i in range(k)] + [(0, None) for i in range(k)]
# For NLopt
# for constraint in constraints:
	# if constraint['type'] == 'eq':
		# opt.add_equality_constraint(constraint['fun'])
	# elif constraint['type'] == 'ineq':
		# opt.add_inequality_constraint(constraint['fun'])
# opt.set_lower_bounds([0 for i in range(len(theta_tilde))])
# opt.add_inequality_constraint(lambda theta_tilde, grad: p(theta_tilde, k - 1))
# For OpenOpt
#opt_c = [lambda theta_tilde: -p(theta_tilde, k - 1) <= 0]
#opt_dc = [lambda theta_tilde: [1 for i in k_m_1_underline] + [0 for i in k_underline] +  + [0 for i in k_underline]]
opt_A = np.zeros((3 * k, 3 * k - 1))
np.fill_diagonal(opt_A, -1)
opt_A[3 * k - 1] = np.ones(3 * k - 1)
# print(opt_A)
opt_b = [0 for i in range(3 * k - 1)] + [1]
# print(opt_b)
opt_lb = [0 for i in range(3 * k - 1)]
opt_ub = [1 for i in range(3 * k - 1)]


# opt.set_ftol_abs(0.001)
# opt.set_initial_step(0.1)

# def L_T_tildeconstrained(theta_tilde):
	# for constraint in constraints:
		# if constraint['fun'](theta_tilde) <= 0:
			# return pos_inf
	# return L_T_tilde(theta_tilde)

cursor = getData(tableName, startDateTime, n, precision)

for row in cursor:
	moment = row[1]
	print(moment)
	x = np.array(row[2])
	assert len(x) == n # Make sure we have exactly n values
	plt.hist(x, bins = 50)
	# plt.show()
	# print(x.mean(),  x.var())
	
	# Initial values TODO
	s, loc, t = gamma.fit(x, loc = 0)
	alpha_est = s
	beta_est = 1 / t
	print(alpha_est, loc, beta_est)
	theta_tilde = np.array(
		[0.5] +                             # p_tilde
		[alpha_est for i in k_underline] + # alpha
		[beta_est for i in k_underline]    # beta
	)
	print(L_T_tilde(theta_tilde))
	theta_tilde = np.array(
		[0.4] + # TODO                                        # p_tilde
		[alpha_est ** (random() * 2) for i in k_underline] + # alpha
		[beta_est ** (random() * 2) for i in k_underline]    # beta
	)
	print(theta_tilde, L_T_tilde(theta_tilde))
	
	# print('COBYLA')
	# print(L_T_tilde(theta_tilde))
	# res = minimize(L_T_tilde, theta_tilde, method = 'COBYLA', constraints = constraints)
	# print(res)
	# assert isfinite(res.fun)
	# theta_tilde = res.x
	# print('p', [p(theta_tilde, i) for i in k_underline])
	# print('alpha', [alpha(theta_tilde, i) for i in k_underline])
	# print('beta', [beta(theta_tilde, i) for i in k_underline])
	
	# # NLopt
	# theta_tilde = opt.optimize(theta_tilde)
	# L_T_tilde_ast = opt.last_optimum_value()
	# print(L_T_tilde_ast)
	# result = opt.last_optimize_result()
	# print(result)
	
	# OpenOpt
	opt_p = GLP(L_T_tilde, theta_tilde, df = grad_L_T_tilde, A = opt_A, b = opt_b, lb = opt_lb, ub = opt_ub)
	res = opt_p.solve('de', maxNonSuccess = 32) # maxNonSuccess = round(exp(len(theta_tilde)))
	print(res.xf, res.ff)
	
	# print('Basin-Hopping')
	# print(L_T_tildeconstrained(theta_tilde))
	# res = basinhopping(L_T_tildeconstrained, theta_tilde)
	# print(res)
	# assert isfinite(res.fun)
	# theta_tilde = res.x
	# print('p', [p(theta_tilde, i) for i in k_underline])
	# print('alpha', [alpha(theta_tilde, i) for i in k_underline])
	# print('beta', [beta(theta_tilde, i) for i in k_underline])
