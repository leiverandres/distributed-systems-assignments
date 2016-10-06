import xmlrpclib
import threading
import os

total_sum = 0

def get_sum(i, j, bind):
    global total_sum
    ip, port = bind
    proxy = xmlrpclib.ServerProxy('http://{0}:{1}/'.format(ip, port))
    result = proxy.sum(i, j)
    total_sum += result

def main():
    global total_sum
    lim = 100
    port = 8000
    binds = [("192.168.11.113", port), ("192.168.11.7", port)]
    n_threads = len(binds)
    size = lim / n_threads
    offset = lim % n_threads
    threads = []
    for i, b in enumerate(binds):
        left = i * size + 1
        right = left + size
        th = threading.Thread(target=get_sum, args=(left, right, b))
        threads.append(th)
        th.start()

    if offset:
        left = n_threads * size + 1
        right = left + offset
        th = threading.Thread(target=get_sum, args=(left, right, binds[0]))
        threads.append(th)
        th.start()

    for t in threads:
        t.join()

    print "Suma total: {}".format(total_sum)

if __name__ == "__main__":
    main()
