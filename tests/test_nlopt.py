import nlopt

f = lambda x, grad = []: x ** 2 - 5

opt = nlopt.opt(nlopt.GN_ISRES, 1)

opt.set_lower_bounds([-10])
opt.set_upper_bounds([10])
opt.set_ftol_rel(0.1)
opt.set_min_objective(f)
opt.optimize([0])