import numpy as np

def jacobi(A, b, eps, maxIterations):
  size = len(A)
  x = np.zeros(size)

  D = np.diag(A)
  R = A - np.diagflat(D)

  for i in range(maxIterations):
    for j in range(size):
      x = (b - np.dot(R,x)) / D

    print(f"{i}-th iteration:")
    print(x)
    if np.linalg.norm(np.dot(A, x) - b) <= eps * np.linalg.norm(b):
      print("^^^^^^^^^^^^^^")
      print("Solution found")
      return

  print("Number of iterations exceeded")
