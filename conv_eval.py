from scipy import signal
import numpy as np

# Good patterns
filter1a = np.array([[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]]) # \
filter2a = np.array([[0,0,0,0,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[1,0,0,0,0]]) # /
filter3a = np.array([[0,0,0,0,0],[0,0,0,0,0],[1,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0]]) # -
filter4a = np.array([[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]]) # |

filter1b = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]) # \
filter2b = np.array([[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]) # /
filter3b = np.array([[0,0,0,0],[0,0,0,0],[1,1,1,1],[0,0,0,0]]) # -
filter4b = np.array([[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]]) # |

filter1c = np.array([[1,0,0],[0,1,0],[0,0,1]]) # \
filter2c = np.array([[0,0,1],[0,1,0],[1,0,0]]) # /
filter3c = np.array([[0,0,0],[1,1,1],[0,0,0]]) # -
filter4c = np.array([[0,1,0],[0,1,0],[0,1,0]]) # |

filter1d = np.array([[1,0],[0,1]]) # \
filter2d = np.array([[0,1],[1,0]]) # /
filter3d = np.array([[0,0],[1,1]]) # -
filter4d = np.array([[0,1],[0,1]]) # d

# Bad patterns
filter1e = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,-1]]) # \
filter1E = np.array([[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]) # \
filter2e = np.array([[0,0,0,-1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]) # /
filter2E = np.array([[0,0,0,1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]]) # /
filter3e = np.array([[0,0,0,0],[0,0,0,0],[-1,1,1,1],[0,0,0,0]]) # -
filter3E = np.array([[0,0,0,0],[0,0,0,0],[1,1,1,-1],[0,0,0,0]]) # -
filter4e = np.array([[0,-1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]]) # |
filter4E = np.array([[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,-1,0,0]]) # |


def count(B, level):
	MAX = np.max(B)
	if MAX == level:
		counter = 0
		for x in range(15):
			for y in range(15):
				if B[x][y] == MAX:
					counter += 1
		return counter
	else:
		return 0 # pattern not found



def evaluate(board, x, y):
	B = np.array(board)
	if B[x][y] != 0:
		return -1
	else:
		if x != -1 and y != -1:
			B[x][y] = 1
		value = 0
		# Good Patterns
		value += 99999*count(signal.convolve2d(B, filter1a),5)
		value += 99999*count(signal.convolve2d(B, filter2a),5)
		value += 99999*count(signal.convolve2d(B, filter3a),5)
		value += 99999*count(signal.convolve2d(B, filter4a),5)
		value += 5000*count(signal.convolve2d(B, filter1b),4)
		value += 5000*count(signal.convolve2d(B, filter2b),4)
		value += 5000*count(signal.convolve2d(B, filter3b),4)
		value += 5000*count(signal.convolve2d(B, filter4b),4)
		value += 1000*count(signal.convolve2d(B, filter1c),3)
		value += 1000*count(signal.convolve2d(B, filter2c),3)
		value += 1000*count(signal.convolve2d(B, filter3c),3)
		value += 1000*count(signal.convolve2d(B, filter4c),3)
		value += 10*count(signal.convolve2d(B, filter1d),2)
		value += 10*count(signal.convolve2d(B, filter2d),2)
		value += 10*count(signal.convolve2d(B, filter3d),2)
		value += 10*count(signal.convolve2d(B, filter4d),2)
		# Bad Patterns
		value -= 2500*count(signal.convolve2d(B, filter1e),4)
		value -= 2500*count(signal.convolve2d(B, filter1E),4)
		value -= 2500*count(signal.convolve2d(B, filter2e),4)
		value -= 2500*count(signal.convolve2d(B, filter2E),4)
		value -= 2500*count(signal.convolve2d(B, filter3e),4)
		value -= 2500*count(signal.convolve2d(B, filter3E),4)
		value -= 2500*count(signal.convolve2d(B, filter4e),4)
		value -= 2500*count(signal.convolve2d(B, filter4E),4)
		
		return value

			