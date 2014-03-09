alpha = 9
beta = 2
from scipy.stats import gamma
f = gamma(alpha, scale = 1 / beta).pdf
import numpy as np
import matplotlib.pyplot as plt
xs = np.arange(0.01, 10, 0.01)
plt.plot(xs, [f(x) for x in xs])
plt.show()
