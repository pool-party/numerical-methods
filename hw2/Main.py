import numpy as np
import random
import math

from Jacobi import jacobi
from Seidel import seidelIterations
from Matrices import *

EPS = 0.000001
MAX_ITERATIONS = 50

print("Diagonal matrix:")
print("Jacobi solution:")
jacobi(diag_A, diag_b, EPS, MAX_ITERATIONS)
print("Seidel solution:")
seidelIterations(diag_A, diag_b, EPS, MAX_ITERATIONS)

print("Random matrix:")
# print("Jacobi solution:")
# jacobi(random_A, random_b, EPS, MAX_ITERATIONS)
print("Seidel solution:")
seidelIterations(*symmetric(random_A, random_b), EPS, MAX_ITERATIONS)

print("Hilbert matrix:")
# print("Jacobi solution:")
# jacobi(hilbert_A, hilbert_b, EPS, MAX_ITERATIONS)
print("Seidel solution:")
seidelIterations(*symmetric(hilbert_A, hilbert_b), EPS, MAX_ITERATIONS)
