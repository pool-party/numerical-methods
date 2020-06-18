import math

# TODO: read coefficents from Bank_TD_Fragment.dat
H = [] # Энергии образования. H(298)
phiCoefs = [[]] # Коэффициенты аппроксимации. f1 - f7
P = 10000 # Атмосферное давлениеы
sigma = []
eps = []
mu = [] # Молярные массы

# indexes
AlCl  = 0
AlCl2 = 1
AlCl3 = 2
HCl   = 3
H2    = 4
N2    = 5

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

def G(i, T):
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
