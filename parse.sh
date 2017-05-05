#!/bin/bash
#set -x

rootpath='/.../emt_data/04282017/'

filepath[0]='single/01/'
filepath[1]='single/02/'
filepath[2]='single/03/'
filepath[3]='single/04/'
filepath[4]='single/05/'
filepath[5]='single/06/'
filepath[6]='dual/01/'
filepath[7]='dual/02/'
filepath[8]='dual/03/'

fp_suffix[0]='left/'
fp_suffix[1]='right/'

outname[0]='single_1_'
outname[1]='single_2_'
outname[2]='single_3_'
outname[3]='single_4_'
outname[4]='single_5_'
outname[5]='single_6_'
outname[6]='dual_1_'
outname[7]='dual_2_'
outname[8]='dual_3_'

out_suffix[0]='l.pickle'
out_suffix[1]='r.pickle'

# Here are the start numbers of JPG files
# Please check the record.txt of your sequence
num_l[0]=0222
num_l[1]=0195
num_l[2]=0177
num_l[3]=0174
num_l[4]=0178
num_l[5]=0123
num_l[6]=0216
num_l[7]=0164
num_l[8]=0157

num_r[0]=0221
num_r[1]=0203
num_r[2]=0193
num_r[3]=0170
num_r[4]=0185
num_r[5]=0136
num_r[6]=0221
num_r[7]=0152
num_r[8]=0164

for i in {0..8}; do
	#left camera
	arg1=${rootpath}${filepath[$i]}${fp_suffix[0]}irb/
	arg2=${outname[$i]}
	arg3=${num_l[$i]}
	arg4=${rootpath}${filepath[$i]}${fp_suffix[0]}${outname[$i]}${out_suffix[0]}
	
	echo "${arg1} ${arg2} ${arg3} ${arg4}"
	# python irbparser.py $arg1 $arg2 $arg3 $arg4
	
	#right camera
	arg1=${rootpath}${filepath[$i]}${fp_suffix[1]}irb/
	arg2=${outname[$i]}
	arg3=${num_r[$i]}
	arg4=${rootpath}${filepath[$i]}${fp_suffix[1]}${outname[$i]}${out_suffix[1]}
	
	echo "${arg1} ${arg2} ${arg3} ${arg4}"
	# python irbparser.py $arg1 $arg2 $arg3 $arg4
done

