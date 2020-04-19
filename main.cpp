#include <iostream>
#include <cmath>
#include <iomanip>

long double f(long double x) { //возвращает значение функции f(x) = x^2-2
    return 3200 * x * x * x * x * x + 480 * x * x * x * x - 73624 * x * x * x - 10686 * x * x + 245645 * x - 59598;
}

long double df(long double x) { //возвращает значение производной
    return 16000 * x * x * x * x + 1920 * x * x * x - 220872 * x * x - 21372 * x + 245645;
}

long double d2f(long double x) { // значение второй производной
    return 64000 * x * x * x + 5760 * x * x - 441744 * x - 21372;
}

static const double EPS = 0.000001;


int main() {
    std::cout << std::fixed << std::setprecision(10);
    long double a, b;// границы отрезка и необходимая точность
    size_t i = 0;
    std::cout << "Please input [a;b]\n=>";
    std::cin >> a >> b; // вводим границы отрезка, на котором будем искать корень
    if (f(a) * f(b) > 0) { // если знаки функции на краях отрезка одинаковые, то здесь нет корня
        std::cout << "\nError! No roots in this interval\n";
    } else {
        long double x0 = f(a) * d2f(a) > 0 ? a : b; // для выбора начальной точки проверяем f(x0) * d2f(x0) > 0 ?
        long double xn = x0 - f(x0) / df(x0); // считаем первое приближение
        if (xn > b || xn < a) {
            x0 = x0 == a ? b : a;
        }
        std::cout << ++i << "-th iteration = " << xn << "\n";
        while (fabs(x0 - xn) > EPS) { // пока не достигнем необходимой точности, будет продолжать вычислять
            x0 = xn;
            xn = x0 - f(x0) / df(x0); // непосредственно формула Ньютона
            std::cout << ++i << "-th iteration = " << xn << "\n";
        }
        std::cout << "\nRoot = " << xn; // вывод вычисленного корня
    }
    return 0;
}