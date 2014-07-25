from mailer import *
from leaderboard import *
from random import shuffle
from subprocess import Popen, PIPE
import operator
import os
import re
import sys


def main(argv):
  if len(argv)!=3:
    print "Usage: python getMail.py emailtag answerkey"
    return
  ws,cs,theme = printHeader()
  PICS = "./PokePics/"
  if theme == 2:
    PICS = "./DogPics/"
  mkdir("code")
  choice = 'u'
  oldMIds = {}
  sendIds = {}
  nns = {}
  scores = {}
  mailer = Mailer(argv[1])
  if theme != 3:
    lb = Leaderboard()
    lb.selectTheme(theme,PICS)
    lb.printBlankBoard()
  names = getNames(PICS)
  while choice != 'Q' and choice != 'q':
    mailer.getMessages()
    for msg in mailer.mids:
      if msg not in oldMIds:
        sender = mailer.getSender(msg)
        if sender not in sendIds:
          sendIds[sender] = getNickname(scores,names)
        name = sendIds[sender]
        filename = mailer.getAttachment(msg,name)
        if mailer.hasCurrent():
          print "Got email from "+name
          corr,tim,mem = assess("./code/"+name+"_"+filename,argv[2],ws,cs)
          #print corr, tim, mem
          mailer.reply(name,corr,tim,mem)
          scores[name] = [corr,tim,mem]
        oldMIds[msg] = name
    if len(scores)>0 and theme != 3:
      lb.updateBoard(topTen(scores), len(scores))
    choice = raw_input("Enter Q to quit, anything else to update: ")
  #cleanup
  rmdir("./code")
  rm("answerDiff.txt")
  rm("timeData.txt")
  rm("gProfResults.txt")
  rm("gmon.out")
  rm("gprofiler")
  rm("results.txt")
  rm("compilerErrors.txt")

def mkdir(name):
  if not os.path.exists(name):
    os.system("mkdir "+name)

def rm(name):
  if os.path.exists(name):
    os.system("rm -f "+name)

def rmdir(name):
  if os.path.exists(name):
    os.system("rm -rf "+name)

def printHeader():
  print "EECS 183 Assistive Discussion Leaderboard"
  print "Created by Reed Coke, Steve Merritt, and Grace Kendall"
  print "University of Michigan, EECS Department\n"
  response = raw_input("Enable whitespace sensitive output differentiation? (y/n): ")

  while response != 'y' and response != 'n':
    response = raw_input("Please enter 'y' or 'n': ")

  if response == "y":
    print "Whitespace is enabled"
  elif response == "n":
    print "Whitespace is disabled"

  response2 = raw_input("Enable case sensitive output differentiation? (y/n): ")
  while response2 != 'y' and response2 != 'n':
    response2 = raw_input("Please enter 'y' or 'n': ")

  if response2 == "y":
    print "Case checking is enabled"
  elif response2 == "n":
    print "Case checking is disabled"
  
  response3 = raw_input("Select your theme:\n   1) Pokemon\n   2) Dogs\n   3) None\n")
  response3 = int(response3)
  while response3 != 1 and response3 != 2 and response3 != 3:
    response3 = raw_input("Please enter '1', '2', or '3': ")
    response3 = int(response3)
  if response3 != 3:
    print "Launching leaderboard..."
  return response=="y",response2=="y", response3

def topTen(scores):
  sorted_x = sorted(scores.items(), key=lambda e: (-1*e[1][0],e[1][1],e[1][2]))
  num = 10
  if len(sorted_x)<10:
    num = len(sorted_x)
  return [[item[0],item[1][0],item[1][1],item[1][2]] for item in sorted_x[:num]]

def getNames(PICS):
  nicks = []
  for f in os.listdir(PICS):
    if not f.startswith("."):
      nicks.append(f[:f.find(".")])
  shuffle(nicks)
  return nicks

def getNickname(nns,names):
  for name in names:
    if name not in nns:
      nns[name]=[]
      return name
  return "Error: Out of Nicknames"

def assess(filename,answerFile,ws,cs):
  #compile
  #os.system("g++ -Wall -Werror -pg -o gprofiler " + filename)
  if unsafe(filename):
    return -2,0.0,0
  os.system("g++ -Wall -pg -o gprofiler "+filename+" 2> compilerErrors.txt")
  if not os.path.exists("./gprofiler"):
    print "Did not compile"
    return -1,0.0,0
  os.system("./gprofiler > results.txt")
  print "Reran output"
  correct = diff(answerFile,ws,cs)
  #profile
  """
  os.system("./gprofiler > /dev/null")
  os.system("gprof ./gprofiler > gProfResults.txt")
  fil = open("gProfResults.txt", 'r')
  contents = fil.read()
  begin = contents.find("index % time")
  end = contents.find("This table")
  gProfContents = re.sub("\n","</p><p>",contents[begin:end])
  """
  #time
  times = [timer() for i in range(5)]
  times.sort()
  time = times[2]
  #s += "</p><p></p><p></p>"
  #s += "<p>Detailed time information: </p><p>"
  #s += gProfContents[:-3]
  print "compiled"
  os.system("rm ./gprofiler")
  return correct,float(time),1

def unsafe(filename):
  F = open(filename,"r")
  text = F.read()
  F.close()
  pattern = re.compile("system")
  match = re.search(pattern,text)
  return bool(match)
"""
def findMainBrace(filename){
  F = open(filename,"r")
  text = F.read()
  F.close()
  pattern = re.compile("int main\s?()\s?{")
  start = pattern.search(text)
  chara = text[start]
  started = False
  count = 0
  while not started or count != 0:
    start += 1
    if start == "{":
      count += 1
      started = True
    elif start == "}":
      count -= 1
  part1 = text[:start]
  part2 = text[start:]
  F = open(filename+"_copy","w")
  F.write(memHead()+part1+memFn()+part2)
  F.close()
}


def memFn():
  s = "sysinfo memInfo;\n"
  s += "sysinfo(&memInfo);\n"
  s += "long long totalVirtualMem = memInfo.totalram;\n"
  s += "totalVirtualMem += memInfo.totalswap;\n"
  s += "totalVirtualMem *= memInfo.mem_unit;\n"
  return s

def memHead():
  return '#define _XOPEN_SOURCE_EXTENDED 1\n#include "sys/resources.h"\n'
"""
def timer():
  os.system("{ time ./gprofiler > /dev/null; } 2> timeData.txt")
  timeFile = open("timeData.txt")
  timeContents = timeFile.read()
  start = timeContents.find("real")
  #s = "<p>Total time: </p><p>"
  time = timeContents[start:timeContents.find("user",start)]
  time = time[5:-2]
  time = time.split("m")
  time = int(time[0])*60 + float(time[1])
  return time

def diffStr(t1,t2):
  print "t1: " + t1
  print "t2: " + t2
  return t1==t2


def diff(answerFile,ws,cs):
  answerTxt = diffLoad(answerFile,ws,cs)
  submission = diffLoad("results.txt",ws,cs)
  return int(diffStr(answerTxt,submission))

def diffLoad(fil,ws,cs):
  F = open(fil,"r")
  answerTxt = F.read()
  F.close()
  if not ws:
    answerTxt = re.sub("\s","",answerTxt)
  if not cs:
    answerTxt.lower()
  return answerTxt

if __name__=='__main__':
  msg = main(sys.argv)
