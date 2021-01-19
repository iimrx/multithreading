from collections import deque
from random import randint
from itertools import islice
from threading import Thread
import time

sort_dict = dict()

def merge(da, db):
    res = deque()
    a = da.popleft()
    b = db.popleft()
    while True:
        if a < b:
            res.append(a)
            try:
                a = da.popleft()
            except IndexError:
                res.append(b)
                res.extend(db)
                break
        else:
            res.append(b)
            try:
                b = db.popleft()
            except IndexError:
                res.append(a)
                res.extend(da)
                break
    return res

def sort(d, put_in_global = False, nb = 0):
    l = len(d)
    if l <= 1:
        return d
    else:
        da = deque(islice(d, 0, int(l/2)))
        db = deque(islice(d, int(l/2), int(l)))
        sda = sort(da)
        sdb = sort(db)
        if put_in_global:
            sort_dict[nb] = merge(sda, sdb)
        else:
            return merge(sda, sdb)

def multi_sort(d):
    l = len(d)
    if l <= 1:
        return d
    else:
        da = deque(islice(d, 0, int(l/2)))
        db = deque(islice(d, int(l/2), int(l)))
        sda = Thread(target=sort, args=(da, True, 1))
        sdb = Thread(target=sort, args=(db, True, 2))
        sda.start()
        sdb.start()
        sda.join()
        sdb.join() 
        return merge(sort_dict[1], sort_dict[2])

def check_sorted(d):
    if d:
        s = d.popleft()
    while True:
        try:
            f = s
            s = d.popleft()
            if f > s:
                return False
        except IndexError:
            return True

if __name__=='__main__':
    with open('results.txt', 'w') as f:
        lengths = [2*10**i for i in range(1, 7)]
        f.writelines(['Length  One_time  Multi_time  Ratio\r\n'])
        for length in lengths:
            print ('----------------------------')
            print ('List length : ' + str(length))
            lst = [randint(0, 10) for i in range(0,9)]
            print ('List : ' + str(lst))
            print ('ONE THREAD')
            start = time.perf_counter()
            res = sort(lst)
            one_time = time.perf_counter() - start
            print ('Sorting time (s) : ' + str(one_time))
            print ('Sort checking : ' + str(check_sorted(res)))
            print ('MULTIPLE THREAD')
            start = time.perf_counter()
            res = multi_sort(lst)
            multi_time = time.perf_counter() - start
            print ('Sorting time (s) : ' + str(multi_time))
            print ('Sort checking : ' + str(check_sorted(res)))
            print ('CONCLUSION')
            print ('Time ratio multi/one : ' + str(multi_time/one_time))
            f.writelines([str(length)+'  '+
                          str(one_time)+'  '+
                          str(multi_time)+'  '+
                          str(multi_time/one_time)+'\r\n'
                          ])
