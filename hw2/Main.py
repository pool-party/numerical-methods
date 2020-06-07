import numpy as np
import random
import math

from Jacobi import jacobi
from Seidel import seidelIterations
from Matrices import diag_A, diag_b, random_A, random_b, hilbert_A, hilbert_b

EPS = 0.000001

print("Diagonal matrix:")
print("Jacobi solution:")
print(jacobi(diag_A, diag_b, EPS))
print("Seidel solution:")
seidelIterations(diag_A, diag_b, EPS)

# Division exception in Jacobi
# print("Random matrix:")
# print("Jacobi solution:")
# print(jacobi(random_A, random_b, EPS))
# print("Seidel solution:")
# seidelIterations(random_A, random_b, EPS)

# Division exception in Jacobi
# print("Hilbert matrix:")
# print("Jacobi solution:")
# print(jacobi(hilbert_A, hilbert_b, EPS))
# print("Seidel solution:")
# seidelIterations(hilbert_A, hilbert_b, EPS)
