from multiprocessing import Process

def f():
    for i in xrange(900000):
        str(i) + str(i)

p = Process(target=f)

p.start()
p.join(.5)

if p.is_alive():
    print 'terminated ..'
    p.terminate()


