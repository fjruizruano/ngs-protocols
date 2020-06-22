#!/usr/bin/python

ra = open("ref_alt3.txt").readlines()
var = open("toico4.txt").readlines()

header = var[0]
samples = header.split()
n_samples = len(samples)
n_samples = (n_samples-2)/6

w = open("out.txt","w")

ra_list = []

for i in range(0,len(ra)):

    ra_line = ra[i]
    ra_info = ra_line.split()
    r = int(ra_info[2])
    a = int(ra_info[3])

    var_line = var[i]
    var_info = var_line.split()
    res = []
    for j in range(0,n_samples):
        r_num = 2+(j*6)+r
        a_num = 2+(j*6)+a
        res.append(var_info[r_num])
        res.append(var_info[a_num])
    w.write("%s\t%s\n" % ("\t".join(ra_info[0:2]),"\t".join(res)))

w.close()
