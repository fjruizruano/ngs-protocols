#!/usr/bin/python

import sys

try:
    members = sys.argv[1]
except:
    members = raw_input("Introduce clusterMembership file: ")

try:
    file = sys.argv[2]
except:
    file = raw_input("Introduce index.tab file: ")

# load index.tab file
def load_index(file):
    dictio = {}
    for line in file:
        line = line.split()
        num = line[1]
        dictio[line[1][2:]] = line[0]
    return dictio

def load_members(members):
    lis = []
    for line in members:
        line = line.split()
        lis.append(line[0])
    return lis

# open files
members = open(members).readlines()
file = open(file).readlines()

# load data
index = load_index(file)
membs = load_members(members)

final_set = set()

for memb in membs:
    if memb in index:
        final_set.add(index[memb][3:-2])

w = open("member_reads.txt","w")
w.write("\n".join(final_set))
w.close()
