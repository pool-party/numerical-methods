import numpy as np

def seidel(A, b, x):
  size = len(A)
  for j in range(0, size):
    d = b[j]

    for i in range(0, size):
      if(j != i):
        d -= A[j][i] * x[i]
    x[j] = d / A[j][j]
  return x

def seidelIterations(A, b, eps, maxIterations):
  size = len(A)
  x = np.zeros(size)

  ind = 0
  while True:
    xPrev = np.copy(x)
    x = seidel(A, b, x)

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
