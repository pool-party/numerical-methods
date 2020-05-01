#include <iostream>
#include <iomanip>

#include <cmath>


static const double EPS = 0.000001;

long double P_x(long double x) { // polynom.
    return 3200 * pow(x, 5) + 480 * pow(x, 4) - 73624 * pow(x, 3) 
        - 10686 * pow(x, 2) + 245645 * x - 59598;
}

long double dP_x(long double x) { // first derivative.
    return 16000 * pow(x, 4) + 1920 * pow(x, 3) - 220872 * pow(x, 2) 
        - 21372 * x + 245645;
}

long double d2P_x(long double x) { // second derivative.
    return 64000 * pow(x, 3) + 5760 * pow(x, 2) - 441744 * x - 21372;
}


int main() {
    std::cout << std::fixed << std::setprecision(10);
    long double a, b; // segment borders.
    std::cout << "Please input [a;b]\n=>";
    std::cin >> a >> b;

    if (P_x(a) * P_x(b) > 0) { // check signs on the segment borders.
        std::cout << "\nError! No roots in this interval\n";
    } else {
        long double x0 = P_x(a) * d2P_x(a) > 0 ? a : b; // first x.
        long double xn = x0 - P_x(x0) / dP_x(x0); // first approximination.
        if (xn > b || xn < a) {
            x0 = x0 == a ? b : a;
            xn = x0 - P_x(x0) / dP_x(x0);
        }

        size_t i = 0;
        std::cout << ++i << "-th iteration = " << xn << "\n";
        while (fabs(x0 - xn) > EPS) { // calculate untill in EPS-neighborhood.
            x0 = xn;
            xn = x0 - P_x(x0) / dP_x(x0); // Neuton formula.
            std::cout << ++i << "-th iteration = " << xn << "\n";
        }

        std::cout << "\nRoot = " << xn; // root output.
    }

    return 0;
}