#Copyright: Steve Merritt
#Style grading software for EECS 183

import os, sys, time, re, glob

def is_number(val):
  try:
    float(val)
    return True
  except ValueError:
    return False

def main():
  os.system('python cpplint.py badcode.cpp &> lint_results.txt')
  
  sum = 0.0
  count = 0
  with open('lint_results.txt', 'r') as lint_results:
    results = lint_results.readlines()
    for line in results:
      value = line[-3]
      if is_number(value):
        sum += int(value)
        count += 1
  
  print('Code score: %d' % sum)
  print('There were a total of %d errors' % count)

if __name__ == '__main__':
  main()
