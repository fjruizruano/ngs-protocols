#!/usr/bin/python

import sys
#####Authors: Team Ladner-Barshis-Tepolt
######Usage########
######This script takes a set of separate quality trimmed paired end .fastq files
######and pairs the reads that still have a mate and combined the solitary reads
######into a single file of orphans for input into denovo assembly software (e.g. CLC Genomics).
print "Command line usage: fastqcombinepairedend.py \042the delimiter\042 \042the seqheader text\042 infiledirection1.fastq infiledirection2.fastq"
print "Command line usage: fastqcombinepairedend.py \042@HWI\042 \042 \042 infiledirection1.fastq infiledirection2.fastq"


seqheader=sys.argv[1]
paireddelim=sys.argv[2]
in1=sys.argv[3]
in2=sys.argv[4]

###This line had to be added 15Oct2012 for script to work properly
setoffiles=[in1, in2]

#filecount=0
#pairedlist=[]
#for file in infilelist:
    #if filecount==0:
        #firstname=file
        #filecount+=1
    #else:
        #secondname=file
        #filecount=0
        #pairedlist.append((firstname,secondname))

#Opens an infile specified by the user. 
IN1 = open(sys.argv[3], 'r')
IN2 = open(sys.argv[4], 'r')

#Opens an output text file as specified by user
SIN = open('%s_trimmed_clipped_singles.fastq'%(sys.argv[3][:-23]), 'w') #Unpaired reads from both directions for CLC
PAIR1 = open('%s_trimmed_clipped_stillpaired.fastq'%(sys.argv[3][:-6]), 'w') #Read one of paired reads for CLC
PAIR2 = open('%s_trimmed_clipped_stillpaired.fastq'%(sys.argv[4][:-6]), 'w') #Read two of paired reads for CLC


names1=[]
names2=[]
seqs1={}
seqs2={}
quals1={}
quals2={}
linenum1=0

#Starts a for loop to read through the infile line by line
for line in IN1:

	line = line.rstrip()
	linenum1+=1
	
	#sets count to 1 when it finds the header before a sequence
	if line[0:4]==seqheader:
		line=line.split(paireddelim)
		name=line[0][1:]
		names1.append(name)
		count = 0
	else:
		if count==1:
			seqs1[name]=line
		if count==3:
			quals1[name]=line
	
	count=count+1
#        print linenum1
print 'finished reading in: %s' %(setoffiles[0])

for line in IN2:

#        print 2 #commented out 15oct2012 just produces a long list of 2's in stout

	line = line.rstrip()
	
	#sets count to 1 when it finds the header before a sequence
	if line[0:4]==seqheader:
		line=line.split(paireddelim)
		name=line[0][1:]
		names2.append(name)
		count = 0
	else:	
		if count==1:
			seqs2[name]=line
		if count==3:
			quals2[name]=line
	
	count=count+1
#	print linenum1
#    print 'here'
print 'finished reading in: %s'%(setoffiles[1])
            
paired = list(set(names1) & set(names2))
#print paired
#    print len(paired)
print 'number of paired reads: %d'%(len(paired))
single = list(set(names1) ^ set(names2))
#    print len(single)
single1 = list(set(single) & set(names1))
#    print len(single1)
print 'number of single reads left from %s: %d'%(setoffiles[0],len(single1))
single2 = list(set(single) & set(names2))
#    print len(single2)
print 'number of single reads left from %s: %d'%(setoffiles[1],len(single2))    

#     for label in paired:
#         PAIR.write('@' + str(label) + '1\n' + str(seqs1[label]) + '\n+' + str(label) + '1\n' + str(quals1[label]) + '\n@' + str(label) + '2\n' + str(seqs2[label]) + '\n+' + str(label) + '2\n' + str(quals2[label]) + '\n')
	
for label in single1:
	SIN.write('@' + str(label) + '1\n' + str(seqs1[label]) + '\n+' + str(label) + '1\n' + str(quals1[label]) + '\n')
	
for label in single2:
	SIN.write('@' + str(label) + '2\n' + str(seqs2[label]) + '\n+' + str(label) + '2\n' + str(quals2[label]) + '\n')
	
for label in paired:
	PAIR1.write('@' + str(label) + '1\n' + str(seqs1[label]) + '\n+' + str(label) + '1\n' + str(quals1[label]) + '\n')
	PAIR2.write('@' + str(label) + '2\n' + str(seqs2[label]) + '\n+' + str(label) + '2\n' + str(quals2[label]) + '\n')

IN1.close()
IN2.close()
SIN.close()
PAIR1.close()
PAIR2.close()

