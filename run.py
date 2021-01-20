from collections import deque
from random import randint
from itertools import islice
from threading import Thread
from itertools import product
import time
import queue

startArray = time.time()
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
        lengths = [2*10**i for i in range(2)]
        f.writelines(['Length  One_time  Multi_time  Ratio\r\n'])
        for length in lengths:
            print ('----------------------------')
            lst = [randint(0, 10) for i in range(0,9)]
            print ('Input List: ' + str(lst))
            print ('List length : ' + str(len(lst)))
            print ('ONE THREAD')
            start = time.perf_counter()
            res = sort(lst)
            one_time = time.perf_counter() - start
            print ('Sorting time (s) : ' + str(one_time))
            # print ('Sort checking : ' + str(check_sorted(res)))
            print ('Output List: '+ str(sort(lst)) +'\n')
            print('App: ArraySorting')

            print ('MULTIPLE THREAD')
            start = time.perf_counter()
            res = multi_sort(lst)
            multi_time = time.perf_counter() - start
            print ('Sorting time (s) : ' + str(multi_time))
            # print ('Sort checking : ' + str(check_sorted(res)))
            print ('Output List: '+ str(multi_sort(lst)) +'\n')
            print('App: ArraySorting')
            
            print ('Time ratio multi/one : ' + str(multi_time/one_time) + '\n')
            f.writelines([str(length)+'  '+
                          str(one_time)+'  '+
                          str(multi_time)+'  '+
                          str(multi_time/one_time)+'\r\n'
                          ])
endArray = time.time()

# ----------------------------------------------------- #

startSudoku = time.time()
DIGITS = set(range(1, 10)) # 1-9

def check_grid_size(grid):
    """Check that the grid is 9x9."""
    well_formed = len(grid) == 9 and all(len(row) == 9 for row in grid)
    return well_formed or None

def check_rows(grid, q):
    """Check that each number appears exactly once per row."""
    q.put(all(set(row) == DIGITS for row in grid))

def check_columns(grid, q):
    """Check that each number appears exactly once per column."""
    columns = [[row[c] for row in grid] for c in range(9)]
    q.put(all(set(col) == DIGITS for col in columns))

def check_3x3_grid(grid, q):
    """Check that each number appears exactly once per 3x3 grid."""
    threes = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    for row_block, col_block in product(threes, threes):
        block = [grid[r][c] for r, c in product(row_block, col_block)]
        if set(block) != DIGITS:
            q.put(False)
            return
    q.put(True)

def check_sudoku(grid):
    # Capture program start time
    start_time = time.perf_counter()

    assert isinstance(grid, list)
    q = queue.Queue()
    if not check_grid_size(grid):
        return None

    row_thread = Thread(target=check_rows, args=(grid, q))
    row_thread.start()

    columns_thread = Thread(target=check_columns, args=(grid, q))
    columns_thread.start()

    grid_threads = []
    for _ in range(9):
        t = Thread(target=check_3x3_grid, args=(grid, q))
        t.start()
        grid_threads.append(t)
        print(f'Thread Number: {len(grid_threads)}, Thread Time: {round(time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID), 5)}, App: Sudoku')

    row_thread.join()
    columns_thread.join()
    
    [t.join() for t in grid_threads]
    # Capture program execution time
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f'Execution time: {round(execution_time, 5)} sec')

    results = []
    while not q.empty():
        results.append(q.get())
    return all(results)

def main():
    will_formed = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                  [6, 7, 2, 1, 9, 5, 3, 4, 8],
                  [1, 9, 8, 3, 4, 2, 5, 6, 7],
                  [8, 5, 9, 7, 6, 1, 4, 2, 3],
                  [4, 2, 6, 8, 5, 3, 7, 9],  # <---
                  [7, 1, 3, 9, 2, 4, 8, 5, 6],
                  [9, 6, 1, 5, 3, 7, 2, 8, 4],
                  [2, 8, 7, 4, 1, 9, 6, 3, 5],
                  [3, 4, 5, 2, 8, 6, 1, 7, 9]]

    # check_sudoku should return True
    valid = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
             [6, 7, 2, 1, 9, 5, 3, 4, 8],
             [1, 9, 8, 3, 4, 2, 5, 6, 7],
             [8, 5, 9, 7, 6, 1, 4, 2, 3],
             [4, 2, 6, 8, 5, 3, 7, 9, 1],
             [7, 1, 3, 9, 2, 4, 8, 5, 6],
             [9, 6, 1, 5, 3, 7, 2, 8, 4],
             [2, 8, 7, 4, 1, 9, 6, 3, 5],
             [3, 4, 5, 2, 8, 6, 1, 7, 9]]

    # check_sudoku should return False
    invalid = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
               [6, 7, 2, 1, 9, 5, 3, 4, 8],
               [1, 9, 8, 3, 8, 2, 5, 6, 7],
               [8, 5, 9, 7, 6, 1, 4, 2, 3],
               [4, 2, 6, 8, 5, 3, 7, 9, 1],
               [7, 1, 3, 9, 2, 4, 8, 5, 6],
               [9, 6, 1, 5, 3, 7, 2, 8, 4],
               [2, 8, 7, 4, 1, 9, 6, 3, 5],
               [3, 4, 5, 2, 8, 6, 1, 7, 9]]

    print(f'Valid: {check_sudoku(valid)}')
    print(f'InValid: {check_sudoku(invalid)}')
    print(f'will Formed: {check_sudoku(will_formed)}')

if __name__ == '__main__':
    main()
endSudoku = time.time()

totalSudoku = round((endSudoku-startSudoku), 5)
totalArray = round((endArray-startArray), 5)
totalBoth = totalSudoku + totalArray

print(f'\nTime to Run Sudoku: {totalSudoku} \nTime to Run ArraySorting: {totalArray} \nTotal Time To Run Files: {totalBoth}')

if totalSudoku < totalArray:
  print(f'Sudoku is Fast! with time: {(totalSudoku)}')
else:
  print(f'ArraySorting is Fast! with time:{(totalArray)}')
