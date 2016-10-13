import threading

n = 3
A = [
	[1, 2, 3],
	[4, 5, 6],
	[7, 8, 9]
]
B = [
	[9, 8, 7],
	[6, 5, 4],
	[3, 2, 1]
]
C = [[0] * n for __ in xrange(n)]


class MatrixProduct(threading.Thread):
	def __init__(self, row, col):
		super(MatrixProduct, self).__init__()
		self.row = row
		self.col = col
	
	def run(self):
		global n, A, B, C
		acc = 0
		for k in xrange(n):
			acc += A[self.row][k] * B[k][self.col]
		C[self.row][self.col] = acc


def main():
	global n, A, B, C
	threads = []

	for i in xrange(n):
		for j in xrange(n):
			t = MatrixProduct(i, j)
			threads.append(t)
			t.start()
	for t in threads:
		t.join()

	for i, (ai, bi, ci) in enumerate(zip(A, B, C)):
		if i == n / 2:
			print '{} {} = {}'.format(ai, bi, ci)
		else:
			print '{} {}   {}'.format(ai, bi, ci)

if __name__ == '__main__':
	main()
