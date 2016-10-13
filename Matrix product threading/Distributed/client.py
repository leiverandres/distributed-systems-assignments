import threading
import xmlrpclib
import time

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
    def __init__(self, row, col, proxy):
        super(MatrixProduct, self).__init__()
        self.row = row
        self.col = col
        self.proxy = proxy

    def run(self):
        global n, A, B, C
        row = A[self.row]
        col = zip(*B)[self.col]
        C[self.row][self.col] = self.proxy.mult(row, col)


def main():
    global n, A, B, C
    threads = []
    binds = [('192.168.11.19', '8000')]
    proxys = [
        xmlrpclib.ServerProxy('http://{0}:{1}/'.format(ip, port))
        for ip, port in binds
    ]

    for i in xrange(n):
        for j in xrange(n):
            t = MatrixProduct(i, j, proxys[0])
            threads.append(t)
            t.start()
            time.sleep(0.009)
    for t in threads:
        t.join()

    for i, (ai, bi, ci) in enumerate(zip(A, B, C)):
        if i == n / 2:
            print '{} {} = {}'.format(ai, bi, ci)
        else:
            print '{} {}   {}'.format(ai, bi, ci)

if __name__ == '__main__':
    main()
