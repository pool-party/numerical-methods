from Matrices import *
import numpy as np


def gauss(A, b):
  Ab = np.hstack([A, b.reshape(-1, 1)])

  n = len(b)

  for i in range(n):
    a = Ab[i]

    for j in range(i + 1, n):
      b = Ab[j]
      m = a[i] / b[i]
      Ab[j] = a - m * b

  for i in range(n - 1, -1, -1):
    Ab[i] = Ab[i] / Ab[i, i]
    a = Ab[i]

    for j in range(i - 1, -1, -1):
      b = Ab[j]
      m = a[i] / b[i]
      Ab[j] = a - m * b

  x = Ab[:, 12]
  print(x)
