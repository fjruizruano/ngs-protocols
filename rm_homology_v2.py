#!/usr/bin/python

import sys
from Bio import SeqIO
from subprocess import call

print "Usage: rm_homology.py FastaFile"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce FASTA file: ")

data = SeqIO.parse(open(file), "fasta")
seq_dict = {}
seq_list = []

for s in data:
    seq_dict[str(s.id)] = str(s.seq)
    seq_list.append(str(s.id))

#w = open(file+"homology", "w")
#w.close()

matches = []
m = -1

for seq in seq_list:
    m += 1
    matches.append([seq])
    tmp_list = [x for x in seq_list if x != seq]

    for group in matches:
        if seq in group:
            for el in group:
                if seq != el:
                    tmp_list.remove(el)

    tmp_out = "EMPTY"

#    w = open("output", "a")
#    w.write(seq+":\n")
#    w.close()

    while tmp_out[0] != "There were no repetitive sequences detected in tmp_query.fas\n":
        tmp_query = open("tmp_query.fas", "w")
        tmp_db = open("tmp_db.fas", "w")
        tmp_query.write(">%s\n%s\n" % (seq, seq_dict[seq]))
        tmp_query.close()

        for tmp in tmp_list:
            tmp_db.write(">%s\n%s\n" % (tmp, seq_dict[tmp])) 
        tmp_db.close()

        call("RepeatMasker -nolow -no_is -s -engine crossmatch -lib tmp_db.fas tmp_query.fas", shell=True)
        
        tmp_out = open("tmp_query.fas.out").readlines()
        print tmp_out
        call("rm -r tmp_query.fas.*", shell=True)
        if len(tmp_out) > 1:
            for line in tmp_out[3:]:
                info = line.split()
                name = "%s#%s" % (info[9],info[10])
                print name
#                w = open("output", "a")
#                w.write("--"+name+"\n")
#                w.close()
                try:
                    tmp_list.remove(name)
                except:
                    pass
                matches[m].append(name)
        print matches

call("rm tmp_query.fas",shell=True)
call("rm tmp_db.fas",shell=True)

matches = sorted([sorted(x) for x in matches]) #Sorts lists in place so you dont miss things. Trust me, needs to be done.

resultslist = [] #Create the empty result list.

if len(matches) >= 1: # If your list is empty then you dont need to do anything.
    resultlist = [matches[0]] #Add the first item to your resultset
    if len(matches) > 1: #If there is only one list in your list then you dont need to do anything.
        for l in matches[1:]: #Loop through lists starting at list 1
            matcheset = set(l) #Turn you list into a set
            merged = False #Trigger
            for index in range(len(resultlist)): #Use indexes of the list for speed.
                rset = set(resultlist[index]) #Get list from you resultset as a set
                if len(matcheset & rset) != 0: #If listset and rset have a common value then the len will be greater than 1
                    resultlist[index] = list(matcheset | rset) #Update the resultlist with the updated union of listset and rset
                    merged = True #Turn trigger to True
                    break #Because you found a match there is no need to continue the for loop.
            if not merged: #If there was no match then add the list to the resultset, so it doesnt get left out.
                resultlist.append(l)
print resultlist

num = 0

for group in resultlist:
    num += 1
    numstr = str(num)
    while len(numstr) <= 2:
        numstr = "0"+numstr
    print "Group %s: %s" % (numstr, ", ".join(group))
    query = open("group"+numstr+".fas", "w")
    for s in group:
        query.write(">%s\n%s\n" % (s, seq_dict[s]))
    query.close()
