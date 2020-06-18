from Utils import *

Pg = [0 for i in range(10)] # Парциальное давление компонент
Pg[AlCl] = Pg[AlCl2] = Pg[AlCl3] = Pg[H2] = 0
Pg[HCl] = 10000
Pg[N2] = 90000
delta = 0.01
T0 = celsiusToKelvin(350)
Tn = celsiusToKelvin(650)
