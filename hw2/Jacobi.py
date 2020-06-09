import numpy as np

def jacobi(A, b, eps, maxIterations):
  size = len(A)
  x = np.zeros(size)

  D = np.diag(A)
  Dm = np.diagflat(D)
  Dneg = np.diagflat([1 / n for n in D])
  R = A - Dm

  w, v = np.linalg.eig(np.dot(Dneg, R))
  if max(abs(w)) > 1:
    print("Spectral radius of matrix is less than 1, aborting calculation")
    return

  for i in range(size):
    if sum(abs(R[i])) >= abs(D[i]):
      print("Warning: Matrix is not diagonally dominant")
      break

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
