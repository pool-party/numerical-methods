# Моделирование роста монокристаллического твердого раствора $Al_xGa_{1-x}N$ методом хлоридной эпитаксии

Изначальные реакции при подаче $HCl$:
$$
2Al(solid) + 2HCl \Leftrightarrow 2AlCl + H_2
$$
$$
Al(solid) + 2HCl \Leftrightarrow AlCl_2 + H_2
$$
$$
2Al(solid) + 6HCl \Leftrightarrow 2AlCl_3 + 3H_2
$$


$$
2Ga(liquid) + 2HCl \Leftrightarrow 2GaCl + H_2
$$
$$
Ga(liquid) + 2HCl \Leftrightarrow GaCl_2 + H_2
$$
$$
2Ga(liquid) + 6HCl \Leftrightarrow 2GaCl_3 + 3H_2
$$

Поверхностные реакции при росте алгана:
$$
AlCl + NH_3 \Leftrightarrow AlN(solid) + HCl + H_2
$$
$$
2AlCl_2 + 2NH_3 \Leftrightarrow 2AlN(solid) + 4HCl + H_2
$$
$$
AlCl_3 + NH_3 + \Leftrightarrow AlN(solid) + 3HCl
$$

$$
GaCl + NH_3 \Leftrightarrow GaN(solid) + HCl + H_2
$$
$$
2GaCl_2 + 2NH_3 \Leftrightarrow 2GaN(solid) + 4HCl + H_2
$$
$$
GaCl_3 + NH_3 \Leftrightarrow GaN(solid) + 3HCl
$$





## Часть 1. Моделирование конверсии **HCl в хлориды алюминия** 

Для нахождения межфазных потоков $G_i$ воспользуемся следующей формулой:

$$
G_i = D_i {(P^g_i - P^e_i)\over R T \delta}
$$
Для ее применения нам необходимо найти термодинамические давления $P_i^e$. Выразим температурно-зависимые константы равновесия реакций $K_j(T)$ для формул $(1)-(3)$ из законов действующих масс:
$$
𝐾_1={(𝑃^{\ e}_{𝐻𝐶𝑙})^2\over(𝑃^{\ e}_{Al𝐶𝑙})^2𝑃^{\ e}_{𝐻_2}}
$$
$$
𝐾_2={(𝑃^{\ e}_{𝐻𝐶𝑙})^2\over𝑃^{\ e}_{Al𝐶𝑙_2}𝑃^{\ e}_{𝐻_2}}
$$
$$
𝐾_3={(𝑃^{\ e}_{𝐻𝐶𝑙})^6\over(𝑃^{\ e}_{Al𝐶𝑙_3})^2(𝑃^{\ e}_{𝐻_2})^3}
$$
Дополнив уравнения $(14)-(16)$ стехиометрическими соотношениями:
$$
D_{HCl}(P^g_{HCl}-P^e_{HCl})+2D_{H_2}(P^g_{H_2}-P^e_{H_2})=0
$$
$$
D_{AlCl}(P^g_{AlCl} - P^e_{AlCl}) + 2D_{AlCl_2}(P^g_{AlCl_2} - P^e_{AlCl_2}) + 3D_{AlCl_3}(P^g_{AlCl_3} - P^e_{AlCl_3}) + D_{HCl}(P^g_{HCl} - P^e_{HCl}) = 0
$$
получим систему для нахождения термодинамических давлений для $AlCl, AlCl_2, AlCl_3, HCl, H_2$.

Далее, с помощью полученных данных и нижеприведенной формулы, можно вычислить скорость испарения алюминиевого источника:
$$
V^e_{Al} = (G_{AlCl} + G_{AlCl_2} + G_{AlCl_3})({\mu_{Al}\over\rho_{Al}})*10^9
$$

Взяв за основу следующие значения:
$P_{AlCL}^g=P_{AlCL_2}^g=P_{AlCL_3}^g=P_{H_2}^g=0$, $P_{HCl}^g=10000$ Па, $P_{N_2}^g=190000$ Па, $P=P_{HCl}^g+P_{N_2}^g=100000$ Па, 
$\delta=0.01$м, $T=350...650^\circ C$




![cp-task1-a](../assets/cp-task1-a.png)

![cp-task1-a](../assets/cp-task1-b.png)

## **Часть 2. Моделирование конверсии** **HCl в хлориды галлия** 

$$
𝐾_1={(𝑃^{\ e}_{𝐻𝐶𝑙})^2\over(𝑃^{\ e}_{Ga𝐶𝑙})^2𝑃^{\ e}_{𝐻_2}}
$$
$$
𝐾_2={(𝑃^{\ e}_{𝐻𝐶𝑙})^2\over𝑃^{\ e}_{Ga𝐶𝑙_2}𝑃^{\ e}_{𝐻_2}}
$$
$$
𝐾_3={(𝑃^{\ e}_{𝐻𝐶𝑙})^6\over(𝑃^{\ e}_{Ga𝐶𝑙_3})^2(𝑃^{\ e}_{𝐻_2})^3}
$$
$$
D_{HCl}(P^g_{HCl}-P^e_{HCl})+2D_{H_2}(P^g_{H_2}-P^e_{H_2})=0
$$
$$
D_{GaCl}(P^g_{GaCl} - P^e_{GaCl}) + 2D_{GaCl_2}(P^g_{GaCl_2} - P^e_{GaCl_2}) + 3D_{GaCl_3}(P^g_{GaCl_3} - P^e_{GaCl_3}) + D_{HCl}(P^g_{HCl} - P^e_{HCl}) = 0
$$
$$
V^e_{Ga} = (G_{GaCl} + G_{GaCl_2} + G_{GaCl_3})({\mu_{Ga}\over\rho_{Ga}})*10^9
$$

![cp-task1-a](../assets/cp-task2-a.png)

![cp-task1-a](../assets/cp-task2-b.png)

