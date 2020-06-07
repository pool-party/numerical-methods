import numpy as np

def jacobi(A, b, eps):
  size = len(A)
  x = np.zeros(size)

  D = np.diag(A)
  R = A - np.diagflat(D)

  while True:
    xPrev = x
    for i in range(size):
      x = (b - np.dot(R,x)) / D
    if max(abs(x - xPrev)) < eps:
      return x
  return -1


