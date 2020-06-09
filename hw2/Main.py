import numpy as np
import random
import math

from Jacobi import jacobi
from Matrices import *
from Seidel import seidelIterations
from Relaxation import relaxation
from Gradient import gradient


EPS = 0.000001
MAX_ITERATIONS = 100
OMEGA = 0.5

print("Diagonal matrix:")
print("Exact solution:")
print(np.linalg.solve(diag_A, diag_b))
print("Jacobi solution:")
jacobi(diag_A, diag_b, EPS, MAX_ITERATIONS)
print("Seidel solution:")
seidelIterations(diag_A, diag_b, EPS, MAX_ITERATIONS)
print("Relaxation solution:")
relaxation(diag_A, diag_b, OMEGA, EPS, MAX_ITERATIONS)
print("Gradient solution:")
gradient(*symmetric(diag_A, diag_b), EPS, MAX_ITERATIONS)

print("Random matrix:")
print("Exact solution:")
print(np.linalg.solve(random_A, random_b))
print("Jacobi solution:")
jacobi(*symmetric(random_A, random_b), EPS, MAX_ITERATIONS)
print("Seidel solution:")
seidelIterations(*symmetric(random_A, random_b), EPS, MAX_ITERATIONS)
print("Relaxation solution:")
relaxation(*symmetric(random_A, random_b), OMEGA, EPS, MAX_ITERATIONS)
print("Gradient solution:")
gradient(*symmetric(random_A, random_b), EPS, MAX_ITERATIONS)

print("Hilbert matrix:")
print("Exact solution:")
print(np.linalg.solve(hilbert_A, hilbert_b))
print("Jacobi solution:")
jacobi(*symmetric(hilbert_A, hilbert_b), EPS, MAX_ITERATIONS)
print("Seidel solution:")
seidelIterations(*symmetric(hilbert_A, hilbert_b), EPS, MAX_ITERATIONS)
print("Relaxation solution:")
relaxation(*symmetric(hilbert_A, hilbert_b), OMEGA, EPS, MAX_ITERATIONS)
print("Gradient solution:")
gradient(*symmetric(hilbert_A, hilbert_b), EPS, MAX_ITERATIONS)
