import numpy as np

def jacobi(A, b, eps, maxIterations):
  size = len(A)
  x = np.zeros(size)

  D = np.diag(A)
  R = A - np.diagflat(D)

  ind = 0
  while True:
    xPrev = np.copy(x)
    for i in range(size):
      x = (b - np.dot(R,x)) / D

    ind += 1
    print(f"{ind}-th iteration:")
    print(x)
    if max(abs(x - xPrev)) < eps:
      print("^^^^^^^^^^^^^^")
      print("Solution found")
      break
    if ind > maxIterations:
      print("Number of iterations exceeded")
      break
