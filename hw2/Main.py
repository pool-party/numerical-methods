import numpy as np
import random
import math

from Jacobi import jacobi
from Matrices import *
from Seidel import seidelIterations
from Relaxation import relaxation


EPS = 0.000001
MAX_ITERATIONS = 10000
OMEGA = 0.5

# Everything works fast
print("Diagonal matrix:")
print("Jacobi solution:")
jacobi(diag_A, diag_b, EPS, MAX_ITERATIONS)
print("Seidel solution:")
seidelIterations(diag_A, diag_b, EPS, MAX_ITERATIONS)
print("Relaxation solution:")
relaxation(diag_A, diag_b, OMEGA, EPS, MAX_ITERATIONS)

print("Random matrix:")
# print("Jacobi solution:")
# Division overflow
# jacobi(random_A, random_b, EPS, MAX_ITERATIONS)
print("Seidel solution:")
# Works only on symmetric, ~5k iterations
seidelIterations(*symmetric(random_A, random_b), EPS, MAX_ITERATIONS)
print("Relaxation solution:")
# Works only on symmetric, >10k iterations
relaxation(*symmetric(random_A, random_b), OMEGA, EPS, MAX_ITERATIONS)

print("Hilbert matrix:")
# print("Jacobi solution:")
# Division overflow
# jacobi(hilbert_A, hilbert_b, EPS, MAX_ITERATIONS)
print("Seidel solution:")
# More than 10k iterations, goes to 10k even w/o symmetric
seidelIterations(hilbert_A, hilbert_b, EPS, MAX_ITERATIONS)
print("Relaxation solution:")
# More than 10k iterations, goes to 10k even w/o symmetric
relaxation(hilbert_A, hilbert_b, OMEGA, EPS, MAX_ITERATIONS)
