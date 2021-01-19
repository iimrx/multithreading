import subprocess
import time

start1 = time.time()
subprocess.run("python3 sudoku.py & python3 arraySorting.py", shell=True)
end1 = time.time()

start2 = time.time()
subprocess.run("time python3 sudoku.py", shell=True)
end2 = time.time()

start3 = time.time()
subprocess.run("time python3 arraySorting.py", shell=True)
end3 = time.time()

print(f'\nTotal Time To Run Files: {round((end1-start1), 5)} sec')
print(f'Time to Run Sudoku: {round((end2-start2), 5)} sec')
print(f'Time to Run ArraySorting: {round((end3-start3), 5)} sec')

endSudoku = round((end1-start1), 5)
endArraySorting = round((end2-start2), 5)

if endSudoku > endArraySorting:
  print(f'Sudoku is Fast! with time: {(endSudoku)}')
else:
  print(f'ArraySorting is Fast! with time:{(endArraySorting)}')
