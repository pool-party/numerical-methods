from Utils import *

Pg = [0 for _ in range(elements)] # Па. Парциальные давления компонент вне диффузионного пограничного слоя
Pe = [0 for _ in range(elements)] # Па. Термодинамические давления компонент
Pg[AlCl] = Pg[AlCl2] = Pg[AlCl3] = Pg[H2] = 0
Pg[HCl] = 10000
Pg[N2] = 90000
delta = 0.01 # м. Условная толщина диффузионного пограничного слоя
T0 = celsiusToKelvin(350) # Начальная температура
Tn = celsiusToKelvin(650) # Конечная температура
T = T0
R = 8314 # Дж/(кмоль * К). Универсальная газовая постоянная

def G(i):
  '''
  Межфазные мольные потоки активных компонент

  :param i:
  :return: кмоль/(м^2 * сек)
  '''
  return D(i, T) * (Pg[i] - Pe[i]) / (R * T * delta)

Ve_Al = (G(AlCl) + G(AlCl2) + G(AlCl3)) * (mu[Al] / ro[Al]) * 1000000000