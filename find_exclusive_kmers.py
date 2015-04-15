#!/usr/bin/python

import operator
import sys
from subprocess import call

print "Usage: find_exclusive_kmers.py query(cov=50) subject(cov=1)"

#interest C=50
query = sys.argv[1]
#database C=1
sbjct = sys.argv[2]

#interest kmer-counting
call("jellyfish count -m 25 -s 100M -t 10 -C %s" % (query), shell=True)
call("jellyfish dump -L 50 -c mer_counts.jf > %s" % (query+".50.txt"), shell=True)

#database kmer-counting
call("jellyfish count -m 25 -s 100M -t 10 -C %s" % (sbjct), shell=True)
call("jellyfish dump -L 1 -c mer_counts.jf > %s" % (sbjct+".50.txt"), shell=True)
call("rm mer_counts.jf", shell=True)

dict_q = {}
dict_s = {}
select = {}

list_q = open(query+".50.txt").readlines()
list_s = open(sbjct+".50.txt").readlines()

for x in list_q:
    x = x.split()
    dict_q[x[0]] = int(x[1])

for x in list_s:
    x = x.split()
    dict_s[x[0]] = int(x[1])

for el in dict_q:
    look = el in dict_s
    if look == False:
        select[el] = dict_q[el]

select_sorted = sorted(select.iteritems(), key=operator.itemgetter(1))

select_sorted.reverse()

w = open(query+".excl.txt", "w")
ww = open(query+".excl.fas", "w")

i = 0

for el in select_sorted:
    i += 1
    w.write("%s\t%s\n" % (el[0], str(el[1])))
    ww.write(">%s\n%s\n" % (str(i), el[0]))

w.close()
ww.close()
