import numpy as np

def seidel(A, b, x):
  size = len(A)
  for j in range(size):
    d = b[j]

    for i in range(size):
      if j != i:
        d -= A[j][i] * x[i]
    x[j] = d / A[j][j]
  return x

def seidelIterations(A, b, eps, maxIterations):
  size = len(A)
  x = np.zeros(size)

  for i in range(maxIterations):
    xPrev = np.copy(x)
    x = seidel(A, b, x)

    print(f"{i}-th iteration:")
    print(x)
    if max(abs(x - xPrev)) < eps:
      print("^^^^^^^^^^^^^^")
      print("Solution found")
      break

  print("Number of iterations exceeded")
