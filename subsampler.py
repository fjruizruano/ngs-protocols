#!/usr/bin/env python
import random
import sys

if len(sys.argv) == 1:
  print "subsampler.py file number > output"
  sys.exit()
 
random.seed()
#name of the input file (fasta or fastq)
#assumes input file is standard fasta/fastq format
fileName = sys.argv[1]
#number of sequences to subsample
numSeq = int(sys.argv[2])
increment = 0
 
#if it's a fasta file
if (fileName.find(".fasta") != -1):
  increment = 2
#else if it's a fastq file
elif (fileName.find(".fastq") != -1):
  increment = 4
#quit if neither
else:
  sys.stdout.write("not a fasta/fastq file\n")
  sys.exit()
 
FILE = open(fileName, 'r')
totalReads = list()
index = 0
for line in FILE:
  if(index % increment == 0):
    totalReads.append(index/increment)
  index += 1
FILE.close()
if(len(totalReads) < numSeq):
  sys.stdout.write("You only have "+str(len(totalReads))+" reads!\n")
  sys.exit()
 
ttl = len(totalReads)
random.shuffle(totalReads)
totalReads = totalReads[0: numSeq]
totalReads.sort()
 
FILE = open(fileName, 'r')
listIndex = 0
 
for i in range(0, ttl):
  curRead = ""
  for j in range(0, increment):
    curRead += FILE.readline()
  if (i == totalReads[listIndex]):
    sys.stdout.write(curRead)
    listIndex += 1
    if(listIndex == numSeq):
      break
FILE.close()
