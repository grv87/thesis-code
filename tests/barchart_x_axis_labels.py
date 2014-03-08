from random import randint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
idx = pd.period_range('2011-05-31T19:00', '2011-06-30T18:45', freq = 'H')
print(repr(idx))
df = pd.DataFrame([randint(0, 100) for i in range(len(idx))], index = idx, dtype = np.dtype(int))
print(repr(df))
df.plot(kind = 'bar')
plt.show()