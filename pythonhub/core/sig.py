from multiprocessing import Process, Queue
from code import CodinError


class OutofTimeError(Exception):
    pass

def limited_run(target, time=0.5,  *args):
    done_queue = Queue()
    args = list(args)
    args.append(done_queue)
    print args
    p = Process(target=target, args=args)
    p.start()
    p.join(time)
    if p.is_alive():
        p.terminate()
        raise OutofTimeError
    else:
        print 'successfully run'
    if done_queue.qsize():
        res_sus = done_queue.get()
        res = done_queue.get()
        if not res_sus:
            raise CodinError(res)
        return res


if __name__ == '__main__':
    def code(out):
        print 'get arg:', out
        for i in xrange(9000):
            str(i) + str(i)
        out.put("end")

    print 'res:', limited_run(code, 0.5)

