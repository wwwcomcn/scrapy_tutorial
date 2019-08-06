from multiprocessing import Process, SimpleQueue
import time
import os


def f(q):
    while not q.empty():
        name = q.get()
        print(name)


if __name__ == '__main__':
    start = time.time()

    urls = [
        "http://www.shuquge.com/txt/343/",
        "http://www.shuquge.com/txt/9249/",
        "http://www.shuquge.com/txt/1894/",
        "http://www.shuquge.com/txt/350/",
        "http://www.shuquge.com/txt/74671/"
    ]
    queue = SimpleQueue()
    for url in urls:
        queue.put(url)

    cpu_count = os.cpu_count()
    ps = []
    for cpu in range(cpu_count):
        p = Process(target=f, args=(queue,))
        ps.append(p)
        p.start()
    for p in ps:
        p.join()

    end = time.time()
    print('total: {:.2f}'.format(end - start))
