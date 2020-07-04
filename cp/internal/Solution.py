import math
import sympy as sy
from scipy.optimize import fmin
import numpy as np

from Data import bank_td
from Gauss import gaussMethod

Pa = 100000

def gibbs_energy_i(i_name, T):
    x_t = T / 10000
    data = bank_td[i_name]
    phi = data['f1'] + data['f2'] * math.log(x_t) + data['f3'] / (x_t ** 2) + data['f4'] / x_t \
        + data['f5'] * x_t + data['f6'] * x_t ** 2 + data['f7'] * x_t ** 3
    gibbs = data['H'] - phi * T
    return gibbs

def G0(name, T):
    return gibbs_energy_i(name, T)

def G(name, T, PG, P, R=8314, delta=0.01):
    return D(name, T) * (PG[name] - P[name]) / (R * T * delta)

def eps(name):
    return math.sqrt(bank_td[name]['epsil'] * bank_td['N2']['epsil'])

def mu(name):
    return 2 * bank_td[name]['mu'] * bank_td['N2']['mu'] / (bank_td[name]['mu'] + bank_td['N2']['mu'])

def omega(name, T):
    return 1.074 * ((T / eps(name)) ** (-0.1604))

def sigma(name):
    return (bank_td[name]['sigma'] + bank_td['N2']['sigma']) / 2

def D(name, T):
    bott = Pa * sigma(name) * omega(name, T) * math.sqrt(mu(name))
    return 0.02628 * (T ** 1.5) / bott

def new_zip(x, y):
    return list(zip(x, y))

def equalVector(a, b, eps):
    return sum([(a[i] - b[i])**2 for i in range(len(a))]) < eps

def mul_and_add(a, b, c):
    return [a[i] + b[i] * c for i in range(len(a))]

def minimumF(Funcs, Vars, xk, pk):
    sumFuncs = sy.sympify(0)
    for func in Funcs:
        sumFuncs += func ** 2
    sumFuncs = sy.lambdify(Vars, sumFuncs)
    xk = np.array(xk)
    pk = np.array(pk)
    return lambda a : sumFuncs(*(xk + pk * a))

def localMin(func, start, h, eps):
    tmp = start
    f = func(tmp)
    while True:
        tmp = tmp + h
        f, f1 = func(tmp), f
        if f > f1:
            h /= -3

        if abs(h) < eps:
            return tmp

def newton_method(funcs, var, x0, eps=1e-20, ITER=400, SHOW=False):
    j = funcs.jacobian(var)
    xk1 = sy.zeros(len(x0), 1)
    xk = x0
    iterations = 0
    while not equalVector(xk, xk1, eps) and iterations < ITER:
        xx = new_zip(var, xk)
        jk = j.subs(xx)
        fk = funcs.subs(xx)
        dk = gaussMethod(jk.tolist(), (fk.T * -1.0).tolist()[0])
#         alpha = fmin(minimumF(funcs, var, xk, dk), [0], disp=False)[0]
        alpha = localMin(minimumF(funcs, var, xk, dk), -10, 10, 1e-5)
        xk1 = mul_and_add(xk, dk, alpha)

        xk, xk1 = xk1, xk
        iterations += 1
    if SHOW:
        print(iterations)
    return xk
