import numpy as np

def gradient(A, b, eps, maxIterations):
  m = len(A)
  xk = np.random.rand(m)
  rk = b - np.dot(A, xk)
  zk = rk

  for k in range(maxIterations):
    print(f"{k}-th iteration:")
    print(xk)
    if np.linalg.norm(A @ xk - b) <= eps * np.linalg.norm(b):
      print("^^^^^^^^^^^^^^")
      print("Solution found")
      return
    a = np.dot(rk, rk) / np.dot(A @ zk, zk)
    x = xk + a * zk
    r = rk - a * np.dot(A, zk)
    beta = np.dot(r, r) / np.dot(rk, rk)
    z = r + zk * beta
    xk, rk, zk = x, r, z

  print("Number of iterations exceeded")
