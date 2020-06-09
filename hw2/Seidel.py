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
    if np.linalg.norm(np.dot(A, x) - b) <= eps * np.linalg.norm(b):
      print("^^^^^^^^^^^^^^")
      print("Solution found")
      return

  print("Number of iterations exceeded")
