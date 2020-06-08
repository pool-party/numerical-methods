import numpy as np

def jacobi(A, b, eps, maxIterations):
  size = len(A)
  x = np.zeros(size)

  D = np.diag(A)
  R = A - np.diagflat(D)

  for i in range(maxIterations):
    xPrev = np.copy(x)
    for j in range(size):
      x = (b - np.dot(R,x)) / D

    print(f"{i}-th iteration:")
    print(x)
    if max(abs(x - xPrev)) < eps:
      print("^^^^^^^^^^^^^^")
      print("Solution found")
      return

  print("Number of iterations exceeded")
