import threading
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] - %(threadName)-10s : %(message)s')
total_sum = 0


def sum(l, r):
    global total_sum
    suma = 0
    for i in xrange(l, r):
        suma += i
    total_sum += suma
    logging.debug("from {0} to {1}: sums {2}".format(l, r, suma))

if __name__ == "__main__":
    threads = list()
    lim = int(raw_input('Ingrese hasta donde sumar: '))
    n_threads = int(raw_input('Ingrese el numero de hilos a usar: '))
    size = lim / n_threads
    offset = lim % n_threads
    for i in xrange(n_threads):
        left = i * size + 1
        right = left + size
        th = threading.Thread(target=sum, args=(left, right))
        threads.append(th)
        th.start()

    if offset:
        left = n_threads * size + 1
        right = left + offset
        th = threading.Thread(target=sum, args=(left, right))
        threads.append(th)
        th.start()

    for t in threads:
        t.join()

    print "Suma total: {0}".format(total_sum)
