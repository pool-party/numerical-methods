import numpy as np

def relaxation(A, b, omega, eps, maxIterations):
  size = len(A)
  x = np.zeros(size)

  for k in range(maxIterations):
    for j in range(size):
      d = b[j]

      for i in range(size):
        if j != i:
          d -= A[j][i] * x[i]
      x[j] = (1 - omega) * x[j] + (omega / A[j][j]) * d

    print(f"{k}-th iteration:")
    print(x)
    if np.linalg.norm(np.dot(A, x) - b) <= eps * np.linalg.norm(b):
      print("^^^^^^^^^^^^^^")
      print("Solution found")
      return

  print("Number of iterations exceeded")
