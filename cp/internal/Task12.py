from Solution import *

Pa = 100000
R = 8.314

Delta_G = {
    'Al' : {
        1 : lambda T : 2 * G0('Al', T) + 2 * G0('HCl', T) - 2 * G0('AlCl', T) - G0('H2', T),
        2 : lambda T : G0('Al', T) + 2 * G0('HCl', T) - G0('AlCl2', T) - G0('H2', T),
        3 : lambda T : 2 * G0('Al', T) + 6 * G0('HCl', T) - 2 * G0('AlCl3', T) - 3 * G0('H2', T)
    },
    'Ga' : {
        1 : lambda T : 2 * G0('Ga', T) + 2 * G0('HCl', T) - 2 * G0('GaCl', T) - G0('H2', T),
        2 : lambda T : G0('Ga', T) + 2 * G0('HCl', T) - G0('GaCl2', T) - G0('H2', T),
        3 : lambda T : 2 * G0('Ga', T) + 6 * G0('HCl', T) - 2 * G0('GaCl3', T) - 3 * G0('H2', T)
    }
}

K = {
    'Al' : {
        1 : lambda T : math.exp(-1 * Delta_G['Al'][1](T) / (R * T)) / Pa,
        2 : lambda T : math.exp(-1 * Delta_G['Al'][2](T) / (R * T)),
        3 : lambda T : math.exp(-1 * Delta_G['Al'][3](T) / (R * T)) * Pa
    },
    'Ga' : {
        1 : lambda T : math.exp(-1 * Delta_G['Ga'][1](T) / (R * T)) / Pa,
        2 : lambda T : math.exp(-1 * Delta_G['Ga'][2](T) / (R * T)),
        3 : lambda T : math.exp(-1 * Delta_G['Ga'][3](T) / (R * T)) * Pa
    }
}

Pg = {
    f'AlCl' : 0,
    f'AlCl2': 0,
    f'AlCl3': 0,
    f'GaCl' : 0,
    f'GaCl2': 0,
    f'GaCl3': 0,
    'H2'    : 0,
    'HCl'   : 10000,
    'N2'    : 90000
}

def findPe(T, El):
    Pe_ElCl  = sy.symbols(f'P^e_{El}Cl')
    D_ElCl   = D(f'{El}Cl', T)
    D_ElCl2  = D(f'{El}Cl2', T)
    D_ElCl3  = D(f'{El}Cl3', T)
    D_H2     = D('H2', T)
    D_HCl    = D('HCl', T)
    Pg_ElCl  = Pg[f'{El}Cl']
    Pg_ElCl2 = Pg[f'{El}Cl2']
    Pg_ElCl3 = Pg[f'{El}Cl3']
    Pg_H2    = Pg['H2']
    Pg_HCl   = Pg['HCl']

    Pe_ElCl2 = K[El][1](T) * Pe_ElCl**2 / K[El][2](T)
    Pe_ElCl3 = Pe_ElCl**3 * K[El][1](T)**(3/2) * K[El][3](T)**(-1/2)

    S = D_ElCl * (Pg_ElCl - Pe_ElCl) + 2*D_ElCl2*(Pg_ElCl2 - Pe_ElCl2) + 3*D_ElCl3*(Pg_ElCl3 - Pe_ElCl3)

    equation = sy.Matrix([(Pg_HCl + S / D_HCl)**2 - K[El][1](T) * Pe_ElCl**2 * (Pg_H2 - S / (2*D_H2))])
    ans = newton_method(equation * (10 ** 50), [Pe_ElCl], [100])

    return {
        f'{El}Cl' : ans[0],
        f'{El}Cl2': Pe_ElCl2.subs(Pe_ElCl, ans[0]),
        f'{El}Cl3': Pe_ElCl3.subs(Pe_ElCl, ans[0])
    }


def getGV(El):
    def GV(T):
        Pe = findPe(T, El)
        G_ElCl  = G(f'{El}Cl', T, Pg, Pe)
        G_ElCl2 = G(f'{El}Cl2', T, Pg, Pe)
        G_ElCl3 = G(f'{El}Cl3', T, Pg, Pe)
        V = (G_ElCl + G_ElCl2 + G_ElCl3) * bank_td[El]['mu'] * 1e9 / bank_td[El]['ro']
        return [G_ElCl, G_ElCl2, G_ElCl3, V]
    return GV

def findPe1(T, El):
    HCl, Pe_ElCl, H2, Pe_ElCl2, Pe_ElCl3 = sy.symbols(f'P^e_HCl P^e_{El}Cl P^e_H2 P^e_{El}Cl2 P^e_{El}Cl3')
#     Pe_ElCl  = sy.symbols(f'P^e_{El}Cl')
    D_ElCl   = D(f'{El}Cl', T)
    D_ElCl2  = D(f'{El}Cl2', T)
    D_ElCl3  = D(f'{El}Cl3', T)
    D_H2     = D('H2', T)
    D_HCl    = D('HCl', T)
    Pg_ElCl  = Pg[f'{El}Cl']
    Pg_ElCl2 = Pg[f'{El}Cl2']
    Pg_ElCl3 = Pg[f'{El}Cl3']
    Pg_H2    = Pg['H2']
    Pg_HCl   = Pg['HCl']
    K_El_1 = K[El][1](T)
    K_El_2 = K[El][2](T)
    K_El_3 = K[El][3](T)

    X = sy.Matrix([
        HCl**2 - K_El_1 * Pe_ElCl**2 * H2,
        HCl**2 - K_El_2 * Pe_ElCl2 * H2,
        HCl**6 - K_El_3 * Pe_ElCl3**2 * H2**3,
        D_HCl * (Pg_HCl - HCl) + 2 * D_H2 * (Pg_H2 - H2),
        D_ElCl * (Pg_ElCl - Pe_ElCl) + 2 * D_ElCl2 * (Pg_ElCl2 - Pe_ElCl2) + \
            3 * D_ElCl3 * (Pg_ElCl3 - Pe_ElCl3) + D_HCl * (Pg_HCl - HCl)
    ])
    ans = newton_method(X * (10 ** 50), [Pe_ElCl, Pe_ElCl2, Pe_ElCl3, HCl, H2], [1, 1, 5970, 0.02, 1560], SHOW=True)
    print(ans)
    return {
        f'{El}Cl' : ans[0],
        f'{El}Cl2': ans[1],
        f'{El}Cl3': ans[2]
    }

import matplotlib.pyplot as plt

def arrheniusDiagram(Ts, res):
    return [math.log(abs(res[i])) for i in range(len(Ts))]

def drawGraphics(El, ts, tf, elems = 10):
    ABS_ZERO = -273.15
    Ts = np.linspace(ts - ABS_ZERO, tf - ABS_ZERO, num=elems)
    res_G_ElCl, res_G_ElCl2, res_G_ElCl3, res_V = list(map(list, zip(*map(getGV(El), Ts))))
#     print (res_G_ElCl, res_G_ElCl2, res_G_ElCl3, res_V)
#     print(Ts)
    arrheniusDiagram_G_ElCl  = arrheniusDiagram(Ts, res_G_ElCl)
    arrheniusDiagram_G_ElCl2 = arrheniusDiagram(Ts, res_G_ElCl2)
    arrheniusDiagram_G_ElCl3 = arrheniusDiagram(Ts, res_G_ElCl3)
    arrheniusDiagram_V       = arrheniusDiagram(Ts, res_V)
    Ts += ABS_ZERO
    Ts = 1 / Ts
    print(f"Диаграммы Аррениуса для межфазных мольных потоков {El}-содержащих компонент:")
    plt.figure(figsize=(15,5))
    plt.plot(Ts, arrheniusDiagram_G_ElCl)
    plt.plot(Ts, arrheniusDiagram_G_ElCl2)
    plt.plot(Ts, arrheniusDiagram_G_ElCl3)
    plt.legend(['$G_{'+El+'Cl}$', '$G_{'+El+'Cl_2}$', '$G_{'+El+'Cl_3}$'], fontsize=15)
    plt.xlabel('1/Температура, 1/C°')
    plt.ylabel('ln(G_i), ln(кмоль/м^2*сек)')
    plt.show()
    print(f"Диаграмма Аррениуса для скорости испарения источника {El}:")
    plt.figure(figsize=(15,5))
    plt.plot(Ts, arrheniusDiagram_V)
    plt.xlabel('1/Температура, 1/C°')
    plt.ylabel('ln(V), ln(нм/сек)')
    plt.show()


drawGraphics("Al", 350, 650)

drawGraphics("Ga", 650, 950)
