import math
import json
import numpy as np

elements = 14

# TODO: read coefficents from Bank_TD_Fragment.dat
H = [0 for _ in range(elements)] # Энергии образования. H(298)
phiCoefs = [[] for _ in range(elements)] # Коэффициенты аппроксимации. f1 - f7
P = 100000 # Атмосферное давлениеы
sigma = [0 for _ in range(elements)]
eps = [0 for _ in range(elements)]
ro = [0 for _ in range(elements)] # Плотности
mu = [0 for _ in range(elements)] # Молярные массы

# indexes
AlCl  = 0
AlCl2 = 1
AlCl3 = 2
GaCl  = 3
GaCl2 = 4
GaCl3 = 5
NH3   = 6
H2    = 7
HCl   = 8
N2    = 9
Al    = 10
Ga    = 11
AlN   = 12
GaN   = 13

ro[Al]  = 2690
ro[Ga]  = 5900
ro[AlN] = 3200
ro[GaN] = 6150

def readData():
  dataFile = open("Data.json", "r")
  data = json.load(dataFile)
  for i in data:
    elemData = data[i]
    index = int(i)
    H[index] = elemData.get("H(298)")
    phiCoefs[index] = elemData.get("f")
    sigma[index] = elemData.get("sigma")
    eps[index] = elemData.get("epsil")
    mu[index] = elemData.get("mu")

def x(T):
  return T / 10000

def PHI(i, T):
  '''
  Приведенная энергия Гиббса i-ой компоненты, задаваемая аппроксимацией

  :param i:
  :param T:
  :return:
  '''
  xT = x(T)
  return phiCoefs[i][1] + phiCoefs[i][2] * math.log(xT) + phiCoefs[i][3] / (xT ** 2) + phiCoefs[i][4] / xT + phiCoefs[i][5] * xT + phiCoefs[i][6] * (xT ** 2) + phiCoefs[i][7] * (xT ** 3)

def Gibbs(i, T):
  '''
  Энергия Гиббса i-ой компоненты как функция температуры

  :param i:
  :param T:
  :return:
  '''
  return H[i] - PHI(i, T) * T

def sigmaN2(i):
  '''
  Сечение столкновений молекул i-ой компоненты и N2 (ангстремы)

  :param i:
  :return:
  '''
  return (sigma[i] + sigma[N2]) / 2

def epsN2(i):
  '''
  Глубина потенциальной ямы энергии взаимодействия молекул (К)

  :param i:
  :return:
  '''
  return (eps[i] * eps[N2]) ** (1/2)

def omega(T, i):
  '''
  Аппроксимация интеграла столкновений для переноса массы

  :param T:
  :param i:
  :return:
  '''
  return 1.074 * ((T / epsN2(i)) ** (-0.1604))

def muN2(i):
  '''
  Средняя молярная масса молекул (кг/кмоль)

  :param i:
  :return:
  '''
  return 2 * mu[i] * mu[N2] / (mu[i] + mu[N2])

def D(i, T):
  '''
  Коэффициент диффузии i-ой газообразной компоненты

  :param i:
  :param T:
  :return:
  '''
  return (2.628 * (T ** (3 / 2))) / (100 * P * sigmaN2(i) * omega(T, i) * (muN2(i) ** (1 / 2)))

def celsiusToKelvin(C):
  return C + 273.15

readData()

def jacobian(f, x):
  h = 1.0e-4
  n = len(x)
  Jac = np.zeros([n, n])
  f0 = f(x)
  for i in np.arange(0, n, 1):
    tt = x[i]
    x[i] = tt + h
    f1 = f(x)
    x[i] = tt
    Jac[:, i] = (f1 - f0) / h
  return Jac, f0

def newton(f, x, tol=1.0e-9):
  iterMax = 50
  for i in range(iterMax):
    Jac, fO = jacobian(f, x)
    if np.sqrt(np.dot(fO, fO) / len(x)) < tol:
      return x, i
    dx = np.linalg.solve(Jac, fO)
    x = x - dx
  print("Too many iterations for the Newton method")
