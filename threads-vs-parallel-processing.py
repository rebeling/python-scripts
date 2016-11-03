"""
Test threads vs processes and looking after the GIL.

"""

def wer(r, h):
    """https://martin-thoma.com/word-error-rate-calculation/#python"""
    import numpy
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8)
    d = d.reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitution = d[i-1][j-1] + 1
                insertion    = d[i][j-1] + 1
                deletion     = d[i-1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)
    return d[len(r)][len(h)]


def heavycalculation(r):
    worderrorrate = wer(' '.join(get_sentences(300)).split(),
                        ' '.join(get_sentences(300)).split())
    return r


def do_something(r, q, sleep):
    now = time.time()
    if sleep:
        # sleep for a second
        time.sleep(1)
    else:
        # calculate
        r = heavycalculation(r)
    result = (r, now, time.time()-now)
    if q:
        q.put(result)
    return result


if __name__ == '__main__':
    """One task lasts one second."""

    def print_result(result):
        for r, now, timed in result:
            print r, "Finished", now, timed, "sec"

    # Loop
    # sleep = 10.2 s
    # wer =   28.1 s
    # result = []
    # for r in xrange(0, 10):
    #     result.append(do_something(r, None))
    # print_result(result)

    # # threads
    # # 1.4s sleep
    # # 28.6s wer > GIL!
    # from Queue import Queue
    # from threading import Thread
    # q = Queue()
    # arg_tups = [(i, q) for i in xrange(10)]
    # threads = [Thread(target=do_something, args=arg_tup)
    #            for arg_tup in arg_tups]
    # _ = [t.start() for t in threads]
    # _ = [t.join() for t in threads]
    # results = [q.get() for _ in xrange(len(threads))]
    # print_result(results)

    # # coroutine
    # # 1.4s sleep
    # # 100 sentences 15.2s wer 10 worker (14.4s 4, 13.9s 2)
    # # 300 sentences 142.6s wer 10 worker
    # # 300 sentences 153.4s wer 20 worker
    # # 300 sentences 137.9s wer 4 worker < guess thread management vs cores
    # from concurrent.futures import ProcessPoolExecutor
    # pool = ProcessPoolExecutor(max_workers=4)
    # futures = [pool.submit(do_something, r, None) for r in range(10)]
    # result = []
    # for future in futures:
    #     result.append(future.result())
    # print_result(result)

    # # joblib (uses Pool from multiprocessing.pool)
    # # 1.5s sleep
    # # 100 sentences 15.7s wer 10 (15.3s 4, 14.3s 2,15.2 -1)
    # # 300 sentences 141.1s wer 10
    # # 300 sentences 154.7s wer 20
    # from joblib import Parallel, delayed, effective_n_jobs
    # print effective_n_jobs()
    # result = Parallel(n_jobs=20)(delayed(do_something)(r, None)
    #                              for r in xrange(0, 10))
    # print_result(result)
