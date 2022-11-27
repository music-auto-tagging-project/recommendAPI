import numpy as np

def softmax(x):
  if not isinstance(x,np.ndarray):
    x = np.array(x)
  f_x = np.exp(x) / (np.sum(np.exp(x)) + 1e-9)
  return f_x