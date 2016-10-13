import threading
import logging

logging.basicConfig( level=logging.DEBUG,
    format='[%(levelname)s] - %(threadName)-10s : %(message)s')

class MatrixProduct(threading.Thread):
	def __init__(self, row, mat, row_id):
		super(MatrixProduct, self).__init__()
		self.row = row
		self.mat = mat
		self.row_id = row_id
		self.result = [0] * len(row)

	def run(self):
		n = len(self.row)
		for i in xrange(n):
			acum = 0
			for j in xrange(n):
				acum += self.row[j] * self.mat[j][i]
			self.result[i] = acum
		logging.debug("result for {}: {}".format(self.row_id, self.result))
def main():
	A = [[1,2], [4, 5]]
	B = [[4,2], [7, 1]]
	threads = []
	N_threads = len(A)
	for i in xrange(N_threads):
		t = MatrixProduct(A[i], B, i)
		threads.append(t)
		t.start()

	for t in threads:
		t.join()
	ans = [0] * len(A)
	for t in threads:
		ans[t.row_id] = t.result
	print ans

if __name__ == '__main__':
	main()
