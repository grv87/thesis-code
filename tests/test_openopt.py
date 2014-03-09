from openopt import NLP
f = lambda x: x ** 2 - 5
df = lambda x: 2 * x
x0 = 8
opt = NLP(f, x0, df = df)
res = opt.solve('ralg')
print(res.xf, res.ff)
